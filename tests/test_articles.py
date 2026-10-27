"""The valid-article table and citation grammar (EV-4)."""

import json

import pytest

from conftest import ROOT
from lab.articles import article_number, is_valid, normalise


def test_table_matches_the_official_text_shape():
    table = json.loads((ROOT / "data" / "articles.json").read_text(encoding="utf-8"))
    assert table["source_url"].startswith("https://eur-lex.europa.eu/")
    assert table["checked_on"] == "2026-10-27"
    assert len(table["articles"]) == 119  # 113 plus 4a, 60a, 75a to 75d
    assert table["articles"]["6"][:4] == ["1", "1a", "1b", "1c"]
    assert "5" not in table["articles"]["10"]  # deleted by Regulation (EU) 2026/1744
    assert "4(a)" in table["annexes"]["III"]
    assert "XIV" in table["annexes"]


@pytest.mark.parametrize(
    "citation",
    [
        "Art. 6(2)",
        "Article 6(2)",
        "Art. 6",
        "Art. 5(1)(a)",
        "Art. 5(1)(h)(iii)",
        "Art. 50(1)",
        "Art. 6(1a)",
        "Art. 4a(1)",
        "Art. 113",
        "Annex III",
        "Annex III 4(a)",
        "Annex I 21",
        "Annex XIII (a)",
    ],
)
def test_real_citations_are_valid(citation):
    assert is_valid(citation)


@pytest.mark.parametrize(
    "citation",
    [
        "Art. 147",  # TC-EV-4-01: the Act has 113 articles
        "Article 147",
        "Art. 6(9)",
        "Art. 10(5)",  # deleted in 2026
        "Art. 113(1)",  # Article 113 has no numbered paragraphs
        "Annex XV",
        "Annex III 9(a)",
        "Annex I 1",  # deleted in 2026
        "Section 6",
        "",
        "Art.",
    ],
)
def test_tc_ev_4_01_invented_or_malformed_citations_are_invalid(citation):
    assert not is_valid(citation)


def test_realistic_spacing_and_case_variants():
    assert normalise("article 6 (2)") == "Art. 6(2)"
    assert normalise("  Art.6(2) ") == "Art. 6(2)"
    assert normalise("annex iii 4(a)") == "Annex III 4(a)"
    assert normalise("Annex III, point 4(a)") is None  # outside the grammar
    assert is_valid("article 6 (2)")


def test_article_number_for_overlap():
    assert article_number("Art. 6(2)") == article_number("Art. 6") == "6"
    assert article_number("Article 4a(1)") == "4a"
    assert article_number("Annex III 4(a)") is None
    assert article_number("nonsense") is None
