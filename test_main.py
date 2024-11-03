import pytest
import yaml
import json
import logging
import os

from main import Solution

# Load the configuration file to get the test cases filename and log paths
def load_config(config_filename="test_config.yaml"):
    with open(config_filename, "r") as f:
        return yaml.safe_load(f)

# Load test cases from the file specified in the configuration
def load_test_cases(test_cases_file):
    with open(test_cases_file, "r") as f:
        return json.load(f)

# Check if the log files exist, and create them with headers if they don't
def initialize_log_file(log_file_path, header):
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Create the logs directory if it does not exist
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as f:
            f.write(header + "\n")  # Write the header line

# Configure logging for failures and summary statistics
def configure_logging(failure_log_path, summary_log_path, log_format, date_format):
    # Initialize log files with headers
    failure_header = config["log"]["failure"]["header"]
    summary_header = config["log"]["summary"]["header"]
    
    initialize_log_file(failure_log_path, failure_header)
    initialize_log_file(summary_log_path, summary_header)

    # Configure loggers
    logging.basicConfig(level=logging.INFO)  # Set the default logging level

    # Create loggers for failure and summary
    failure_logger = logging.getLogger("failure_logger")
    summary_logger = logging.getLogger("summary_logger")

    # Set the logging level for each logger
    failure_logger.setLevel(logging.INFO)
    summary_logger.setLevel(logging.INFO)

    # Set up handlers for each log file
    failure_handler = logging.FileHandler(failure_log_path, mode="a")
    summary_handler = logging.FileHandler(summary_log_path, mode="a")

    # Configure formatters using the format and date format from the config
    formatter = logging.Formatter(log_format, datefmt=date_format)
    failure_handler.setFormatter(formatter)
    summary_handler.setFormatter(formatter)

    # Add handlers to loggers
    failure_logger.addHandler(failure_handler)
    summary_logger.addHandler(summary_handler)

    return failure_logger, summary_logger

# Load configuration
config = load_config()

# Access logging settings from the nested structure
log_failure_path = config["log"]["failure"]["path"]
log_summary_path = config["log"]["summary"]["path"]
log_format = config["log"]["format"]
date_format = config["log"]["date_format"]

# Load test cases
test_cases = load_test_cases(config["test_cases_file"])

# Configure logging
failure_logger, summary_logger = configure_logging(
    log_failure_path, 
    log_summary_path, 
    log_format, 
    date_format
)

# Keep track of statistics
total_cases = len(test_cases)
failed_cases = 0

@pytest.mark.parametrize("case", test_cases)
def test_remove_duplicates(case):
    global failed_cases
    solution = Solution()
    k = solution.remove_duplicates(case["nums"])

    # Check results and log failures if any
    try:
        assert k == case["expected_k"], f"Expected unique count: {case['expected_k']}, got: {k}"
        assert case["nums"][:k] + ["_"] * (len(case["nums"]) - k) == case["expected_nums"], f"Expected modified array: {case['expected_nums']}, got: {case['nums'][:k] + ['_'] * (len(case['nums']) - k)}"
    except AssertionError:
        failed_cases += 1
        # Log using the specified format
        failure_logger.error(
            f"{os.path.basename(config['test_cases_file'])}|{case['id']}|{case['expected_k']}|{k}"
        )
        raise  # Re-raise the exception to let pytest know it failed

@pytest.fixture(scope="session", autouse=True)
def session_summary_logger():
    yield  # This allows all tests to run
    print("Session finished. Logging summary...")  # Debug output
    print(f"Total cases: {total_cases}, Failed cases: {failed_cases}")  # Debug output

    # Log summary using the logging framework
    try:
        summary_logger.info(f"{os.path.basename(config['test_cases_file'])}|{total_cases}|{failed_cases}")
        print("Logged summary using logger.")  # Confirm logging via logger
    except Exception as e:
        print(f"Error while logging summary: {e}")

    logging.shutdown()
    print("Logging shutdown.")  # Confirm shutdown
