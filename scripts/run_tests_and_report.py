import unittest
import sys
import os
import json
import datetime
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_submissions import TestAssignmentValidation


class CustomTestResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.test_details = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_details.append({"name": str(test), "result": "PASS", "message": ""})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_details.append({"name": str(test), "result": "FAIL", "message": str(err[1])})

    def addError(self, test, err):
        super().addError(test, err)
        self.test_details.append({"name": str(test), "result": "ERROR", "message": str(err[1])})


def run_suite():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAssignmentValidation)
    result = CustomTestResult()
    suite.run(result)

    total = result.testsRun
    failed_count = len(result.failures) + len(result.errors)
    passed_count = total - failed_count
    overall_status = "PASS" if failed_count == 0 else "FAIL"

    report = {
        "repository": os.getenv("GITHUB_REPOSITORY", "local-dev-repo"),
        "branch": os.getenv("GITHUB_REF_NAME", "main"),
        "commit_sha": os.getenv("GITHUB_SHA", "local-commit-sha"),
        "run_id": os.getenv("GITHUB_RUN_ID", "local-run-001"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_tests": total,
        "passed_tests": passed_count,
        "failed_tests": failed_count,
        "overall_status": overall_status,
        "tests": result.test_details
    }

    os.makedirs("data", exist_ok=True)
    with open("test-report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print("Test Report Generated:")
    print(json.dumps(report, indent=4))

    receiver_url = os.getenv("RECEIVER_URL")
    if receiver_url:
        try:
            resp = requests.post(receiver_url, json=report, timeout=15)
            print(f"Report sent to receiver. Status Code: {resp.status_code} {resp.text[:200]}")
        except Exception as e:
            print(f"Failed to send report to receiver: {e}")

    if overall_status != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    run_suite()