"""Bake-off runner pieces with a stub model (ADR-007, ADR-008, ADR-009)."""

import sys
import textwrap

import pytest

from lab.bakeoff import (
    MEMORY_LIMIT_GB,
    BuildCheckError,
    MlxGenerator,
    RegistryError,
    check_build_files,
    load_registry,
    run_child,
)

REGISTRY = textwrap.dedent(
    """
    [models."tiny"]
    repo = "org/tiny-4bit"
    revision = "abc123"
    weights_sha256 = "00"
    original_model = "org/tiny"
    card_url = "https://example.org"
    licence = "Apache-2.0"
    parameters = "0.1B"
    quantisation = "4-bit"
    developer = "Org"
    jurisdiction = "Nowhere"
    training_data_disclosure = "n/a"
    converted_with = "n/a"
    checked_on = "2026-10-26"
    [models."tiny".template]
    enable_thinking = false
    """
)


def write_registry(tmp_path, text=REGISTRY):
    path = tmp_path / "models.toml"
    path.write_text(text)
    return path


def test_registry_loads_entry_with_template(tmp_path):
    entry = load_registry(write_registry(tmp_path))["tiny"]
    assert entry.revision == "abc123"
    assert entry.template == {"enable_thinking": False}


def test_unknown_slug_is_refused(tmp_path):
    registry = load_registry(write_registry(tmp_path))
    with pytest.raises(RegistryError, match="not in"):
        registry.get_entry("missing")


def test_realistic_slug_with_path_characters_is_refused(tmp_path):
    text = REGISTRY.replace('models."tiny"', 'models."../x"')
    with pytest.raises(RegistryError, match=r"\.\./x"):
        load_registry(write_registry(tmp_path, text))


def test_missing_revision_is_refused_naming_file_and_key(tmp_path):
    text = REGISTRY.replace('revision = "abc123"\n', "")
    with pytest.raises(RegistryError, match=r"models.toml.*tiny.*revision"):
        load_registry(write_registry(tmp_path, text))


def test_safetensors_only_build_passes():
    check_build_files(["config.json", "model.safetensors", "tokenizer.json"])


@pytest.mark.parametrize("bad", ["modeling.py", "pytorch_model.bin", "w.pt", "x.pkl"])
def test_realistic_build_with_code_or_pickle_is_refused(bad):
    with pytest.raises(BuildCheckError, match=bad):
        check_build_files(["config.json", "model.safetensors", bad])


def test_build_without_weights_is_refused():
    with pytest.raises(BuildCheckError, match="safetensors"):
        check_build_files(["config.json", "tokenizer.json"])


class FakeTokenizer:
    def __init__(self):
        self.calls = []

    def apply_chat_template(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        return "<templated>"


def test_prompt_is_one_user_message_with_thinking_off():
    tokenizer = FakeTokenizer()
    gen = MlxGenerator.__new__(MlxGenerator)
    gen.tokenizer = tokenizer
    gen.template = {"enable_thinking": False}
    assert gen.render("classify this") == "<templated>"
    messages, kwargs = tokenizer.calls[0]
    assert messages == [{"role": "user", "content": "classify this"}]
    assert kwargs["enable_thinking"] is False
    assert kwargs["add_generation_prompt"] is True


def child(code):
    return [sys.executable, "-c", textwrap.dedent(code)]


def test_child_success_returns_its_result():
    outcome = run_child(child('import json; print(json.dumps({"seconds": 1.5, "peak_memory_gb": 1.2, "raw": "{}"}))'))
    assert outcome.ok and outcome.result["peak_memory_gb"] == 1.2


def test_child_over_memory_limit_is_excluded_with_peak():
    outcome = run_child(child('import json, sys; print(json.dumps({"peak_memory_gb": 7.1})); sys.exit(3)'))
    assert not outcome.ok
    assert "6.5" in outcome.reason and "7.1" in outcome.reason
    assert MEMORY_LIMIT_GB == 6.5


def test_child_crash_is_excluded_with_message():
    outcome = run_child(child('import sys; sys.stderr.write("boom: cannot load\\n"); sys.exit(1)'))
    assert not outcome.ok and "boom: cannot load" in outcome.reason


def test_realistic_child_killed_by_signal_is_excluded():
    outcome = run_child(child("import os, signal; os.kill(os.getpid(), signal.SIGKILL)"))
    assert not outcome.ok and "killed" in outcome.reason
