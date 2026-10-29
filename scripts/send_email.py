#!/usr/bin/env python3
"""E-mail the JSON test report. Credentials come from environment variables (GitHub Secrets)."""
import json
import os
import smtplib
import sys
from email.message import EmailMessage

REPORT_FILE = os.getenv("REPORT_FILE", "test-report.json")


def main() -> int:
    user = os.getenv("EMAIL_USER", "").strip()
    password = os.getenv("EMAIL_PASS", "").replace(" ", "").strip()  # Gmail shows app passwords with spaces
    to = os.getenv("EMAIL_TO", "").strip()
    if not (user and password and to):
        print("EMAIL_USER / EMAIL_PASS / EMAIL_TO must all be set.")
        return 1
    if not os.path.exists(REPORT_FILE):
        print(f"{REPORT_FILE} not found.")
        return 1

    with open(REPORT_FILE, encoding="utf-8") as f:
        report = json.load(f)

    summary = report.get("summary", {})
    status = str(summary.get("status", "UNKNOWN")).upper()
    repo = report.get("repository", "unknown")
    sha = str(report.get("commit_sha", "unknown"))

    lines = [
        f"Repository : {repo}",
        f"Branch     : {report.get('branch', 'unknown')}",
        f"Commit     : {sha}",
        f"Run ID     : {report.get('run_id', 'unknown')}",
        f"Time (UTC) : {report.get('timestamp', 'unknown')}",
        f"RESULT     : {status}",
        f"Total {summary.get('total', '?')} | Passed {summary.get('passed', '?')} | Failed {summary.get('failed', '?')}",
        "",
        "Individual tests:",
    ]
    for test in report.get("tests", []):
        lines.append(f"  [{str(test.get('result', '?')).upper()}] {test.get('name', '?')}")
        if test.get("failure_message"):
            lines.append(f"      {test['failure_message']}")

    msg = EmailMessage()
    msg["Subject"] = f"[{status}] {repo} @ {sha[:7]}"
    msg["From"] = user
    msg["To"] = to
    msg.set_content("\n".join(lines))
    msg.add_attachment(
        json.dumps(report, indent=2).encode("utf-8"),
        maintype="application",
        subtype="json",
        filename="test-report.json",
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
        server.login(user, password)
        server.send_message(msg)
    print(f"E-mail sent to {to}")
    return 0


if __name__ == "__main__":
    sys.exit(main())