import re
from typing import Optional

class ActionLogsParser:
    @staticmethod
    def count_failed_tests(log_content: str) -> Optional[int]:
        """
        Parses GitHub Action log content to find failed test counts.
        Example patterns:
        - "FAILED (failures=3)"
        - "3 failed, 10 passed"
        - "Tests failed: 5"
        """
        # Pytest pattern: "3 failed, 10 passed"
        pytest_match = re.search(r'(\d+) failed, \d+ passed', log_content)
        if pytest_match:
            return int(pytest_match.group(1))

        # Unittest pattern: "FAILED (failures=3)"
        unittest_match = re.search(r'FAILED \(failures=(\d+)\)', log_content)
        if unittest_match:
            return int(unittest_match.group(1))

        # Generic pattern
        generic_match = re.search(r'Tests failed: (\d+)', log_content, re.IGNORECASE)
        if generic_match:
            return int(generic_match.group(1))

        return None
