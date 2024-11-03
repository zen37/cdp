import pytest
import yaml
import os

from main import Solution
from config_logging import configure_logging
from tests_load import load_test_cases

def load_config(config_filename="config_test.yaml"):
    with open(config_filename, "r") as f:
        return yaml.safe_load(f)

# Load configuration
config = load_config()
test_cases = load_test_cases(config["test_cases_file"])
failure_logger, summary_logger = configure_logging(config)

total_cases = len(test_cases)
failed_cases = 0

@pytest.mark.parametrize("case", test_cases)
def test_remove_duplicates(case):
    global failed_cases
    solution = Solution()
    k = solution.remove_duplicates(case["nums"])
    
    try:
        assert k == case["expected_k"], f"Expected unique count: {case['expected_k']}, got: {k}"
        assert case["nums"][:k] + ["_"] * (len(case["nums"]) - k) == case["expected_nums"], f"Expected modified array: {case['expected_nums']}, got: {case['nums'][:k] + ['_'] * (len(case['nums']) - k)}"
    except AssertionError:
        failed_cases += 1
        failure_logger.info(f"{os.path.basename(config['test_cases_file'])}|{case['id']}|{case['expected_k']}|{k}")
        raise

@pytest.fixture(scope="session", autouse=True)
def session_summary_logger():
    yield
    summary_logger.info(f"{os.path.basename(config['test_cases_file'])}|{total_cases}|{failed_cases}")
