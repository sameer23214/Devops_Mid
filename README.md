# CSC418 DevOps Lab Midterm - Assignment Submission Portal

## Overview
This repository contains the Assignment Submission Portal with automated CI testing and local report delivery for the CSC418 DevOps Lab Midterm.

## How to Run the Application Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the application server:
   ```bash
   python app/server.py
   ```
3. Open your browser at `http://localhost:5000`.

## How to Execute Automated Tests
Run the test runner script:
```bash
python scripts/run_tests_and_report.py
```

## How to Start the Local Report Receiver
1. Run the local receiver:
   ```bash
   python receiver/receiver.py
   ```
2. Expose via ngrok:
   ```bash
   ngrok http 5000
   ```
3. Add the public URL to GitHub Actions Secrets as `RECEIVER_URL`.
