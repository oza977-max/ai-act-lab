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
    snapshot_files,
    verify_weights,
)

REGISTRY = textwrap.dedent(
    """
    [models."tiny"]
    repo = "org/tiny-4bit"
    revision = "0123456789abcdef0123456789abcdef01234567"
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
    [models."tiny".weights]
    "model.safetensors" = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    """
)


def write_registry(tmp_path, text=REGISTRY):
    path = tmp_path / "models.toml"
    path.write_text(text)
    return path


def test_registry_loads_entry_with_template(tmp_path):
    entry = load_registry(write_registry(tmp_path))["tiny"]
    assert entry.revision == "0123456789abcdef0123456789abcdef01234567"
    assert entry.weights == {"model.safetensors": "a" * 64}
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
    text = REGISTRY.replace(
        'revision = "0123456789abcdef0123456789abcdef01234567"\n', ""
    )
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
    outcome = run_child(
        child(
            "import json; print(json.dumps({'load_seconds': 1.0, 'answer_seconds': 0.5,"
            " 'peak_memory_gb': 1.2, 'raw': '{}'}))"
        )
    )
    assert outcome.ok and outcome.result["peak_memory_gb"] == 1.2


def test_child_over_memory_limit_is_excluded_with_peak():
    outcome = run_child(
        child(
            'import json, sys; print(json.dumps({"peak_memory_gb": 7.1})); sys.exit(3)'
        )
    )
    assert not outcome.ok
    assert "6.5" in outcome.reason and "7.1" in outcome.reason
    assert MEMORY_LIMIT_GB == 6.5


def test_child_crash_is_excluded_with_message():
    outcome = run_child(
        child('import sys; sys.stderr.write("boom: cannot load\\n"); sys.exit(1)')
    )
    assert not outcome.ok and "boom: cannot load" in outcome.reason


def test_realistic_child_killed_by_signal_is_excluded():
    outcome = run_child(
        child("import os, signal; os.kill(os.getpid(), signal.SIGKILL)")
    )
    assert not outcome.ok and "killed" in outcome.reason


def test_floating_revision_is_refused(tmp_path):
    text = REGISTRY.replace('"0123456789abcdef0123456789abcdef01234567"', '"main"')
    with pytest.raises(RegistryError, match=r"models.toml.*tiny.*revision"):
        load_registry(write_registry(tmp_path, text))


def test_malformed_weights_hash_is_refused(tmp_path):
    text = REGISTRY.replace('"' + "a" * 64 + '"', '"abc"')
    with pytest.raises(RegistryError, match=r"models.toml.*tiny.*weights"):
        load_registry(write_registry(tmp_path, text))


def test_missing_template_is_refused(tmp_path):
    text = REGISTRY.replace('[models."tiny".template]\nenable_thinking = false\n', "")
    with pytest.raises(RegistryError, match=r"models.toml.*tiny.*template"):
        load_registry(write_registry(tmp_path, text))


def test_unknown_slug_error_names_the_registry_file(tmp_path):
    registry = load_registry(write_registry(tmp_path))
    with pytest.raises(RegistryError, match=r"models.toml"):
        registry.get_entry("missing")


def make_snapshot(tmp_path, files):
    snap = tmp_path / "snap"
    for name, content in files.items():
        (snap / name).parent.mkdir(parents=True, exist_ok=True)
        (snap / name).write_bytes(content)
    return snap


def test_every_safetensors_file_must_match_its_registered_hash(tmp_path):
    import hashlib

    data = b"weights"
    snap = make_snapshot(tmp_path, {"model.safetensors": data})
    good = {"model.safetensors": hashlib.sha256(data).hexdigest()}
    verify_weights(snap, good)
    with pytest.raises(BuildCheckError, match="hash"):
        verify_weights(snap, {"model.safetensors": "b" * 64})


def test_realistic_sharded_build_with_unregistered_shard_is_refused(tmp_path):
    import hashlib

    snap = make_snapshot(
        tmp_path,
        {
            "model-00001-of-00002.safetensors": b"a",
            "model-00002-of-00002.safetensors": b"b",
        },
    )
    registered = {"model-00001-of-00002.safetensors": hashlib.sha256(b"a").hexdigest()}
    with pytest.raises(BuildCheckError, match="model-00002-of-00002"):
        verify_weights(snap, registered)


def test_realistic_code_file_in_subfolder_is_refused(tmp_path):
    snap = make_snapshot(
        tmp_path, {"model.safetensors": b"w", "extra/modeling.py": b"x"}
    )
    with pytest.raises(BuildCheckError, match="modeling.py"):
        check_build_files(snapshot_files(snap))


def test_child_success_without_measurements_is_not_ok():
    outcome = run_child(child("print('no json here')"))
    assert not outcome.ok and "no result" in outcome.reason


def test_child_interrupted_is_not_called_out_of_memory():
    outcome = run_child(
        child("import os, signal; os.kill(os.getpid(), signal.SIGTERM)")
    )
    assert not outcome.ok and "signal 15" in outcome.reason
    assert "memory" not in outcome.reason


def test_crash_reason_is_cleaned_of_control_characters():
    outcome = run_child(
        child('import sys; sys.stderr.write("bad \\x1b[31mred\\n"); sys.exit(1)')
    )
    assert "\x1b" not in outcome.reason


def test_weights_that_is_not_a_table_is_a_registry_error(tmp_path):
    text = REGISTRY.replace('[models."tiny".weights]\n', "").replace(
        '"model.safetensors" = "' + "a" * 64 + '"', ""
    )
    text = text.replace(
        'licence = "Apache-2.0"', 'licence = "Apache-2.0"\nweights = "abc"'
    )
    with pytest.raises(RegistryError, match=r"models.toml.*tiny.*weights"):
        load_registry(write_registry(tmp_path, text))


def test_template_cannot_override_reserved_arguments(tmp_path):
    text = REGISTRY.replace(
        "enable_thinking = false", "enable_thinking = false\ntokenize = true"
    )
    with pytest.raises(RegistryError, match=r"tiny.*template.*tokenize"):
        load_registry(write_registry(tmp_path, text))


@pytest.mark.parametrize("bad", ["w.ckpt", "w.npz", "lib.so", "lib.dylib", "m.gguf"])
def test_other_loadable_or_native_formats_are_refused(bad):
    with pytest.raises(BuildCheckError, match=bad):
        check_build_files(["model.safetensors", bad])


def test_invalid_utf8_in_child_errors_is_recorded_not_raised():
    outcome = run_child(
        child(
            'import sys; sys.stderr.buffer.write(b"bad \\xff\\xfe bytes\\n"); sys.exit(1)'
        )
    )
    assert not outcome.ok and "bad" in outcome.reason
