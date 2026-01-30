from app.parsers.readme_parser import ReadmeParser
from app.parsers.shield_parser import ShieldParser
from app.parsers.action_logs import ActionLogsParser

def test_extract_badges():
    content = """
    # My Project
    ![Build Status](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml)
    <img src="https://img.shields.io/badge/coverage-85%25-green">
    """
    badges = ReadmeParser.extract_badges(content)
    assert "https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml" in badges
    assert "https://img.shields.io/badge/coverage-85%25-green" in badges

def test_parse_shield_url():
    url = "https://img.shields.io/badge/coverage-80%25-green"
    data = ShieldParser.parse_badge_url(url)
    assert data["label"] == "coverage"
    assert data["message"] == "80%"

    coverage = ShieldParser.extract_coverage(url)
    assert coverage == 80.0

def test_count_failed_tests():
    log = "1 failed, 9 passed in 0.5s"
    count = ActionLogsParser.count_failed_tests(log)
    assert count == 1

    log2 = "FAILED (failures=5)"
    count2 = ActionLogsParser.count_failed_tests(log2)
    assert count2 == 5
