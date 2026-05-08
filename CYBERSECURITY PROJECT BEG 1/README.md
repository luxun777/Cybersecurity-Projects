# Vulnerability Scanner

A professional, beginner-friendly Vulnerability Scanner web application built with Python Flask, HTML, CSS, and JavaScript. This tool is designed to scan web applications or network targets for common vulnerabilities and weak configurations, presented in a sleek, modern cybersecurity dashboard.

## Features

- **Port Scanner:** Scans common TCP ports (e.g., 21, 22, 80, 443, 3306) to identify open services.
- **Banner Grabbing:** Attempts to detect service versions and software information from open ports.
- **Security Header Checker:** Analyzes HTTP headers to identify missing protections like `Content-Security-Policy`, `X-Frame-Options`, and `Strict-Transport-Security`.
- **Weak Configuration Detection:** Flags insecure practices such as open FTP/Telnet ports and unencrypted HTTP usage.
- **Vulnerability Scoring:** Calculates an overall security score based on the severity of discovered issues.
- **Professional Dashboard:** A responsive, dark-themed UI with glassmorphism effects, live scan animations, and interactive charts (using Chart.js).
- **Report Generation:** Automatically generates a detailed JSON report of the scan results for download.

## Project Structure

```text
VulnerabilityScanner/
│
├── app.py               # Flask application and API routes
├── scanner.py           # Core scanning logic (ports, headers, banners)
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
│
├── templates/
│   └── index.html       # Dashboard UI
│
├── static/
│   ├── style.css        # Dashboard styling and animations
│   └── script.js        # Frontend logic and API integration
│
├── reports/             # Generated scan reports
│
└── screenshots/         # (Optional) Place screenshots here
```

## Setup Instructions

### Prerequisites

Ensure you have Python 3.x installed on your system.

### Installation

1. Clone the repository or download the source code.
2. Open a terminal and navigate to the project directory.
3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000` or `http://127.0.0.1:5000`.

### Usage

1. Enter a target IP address (e.g., `192.168.1.1`) or a domain name (e.g., `scanme.nmap.org`) in the input field.
2. Click "Initiate Scan".
3. Wait for the scan to complete. The dashboard will automatically update with the results, displaying a security score, threat levels, open ports, and missing headers.
4. Click "Download Report" to save a JSON copy of the scan findings.

## Disclaimer

**Educational Purposes Only.** This tool is intended for educational purposes and for testing systems you own or have explicit permission to test. Do not use this scanner against unauthorized targets.

## Future Enhancements (Optional)

- PDF Report Export
- Real-time live terminal logs in the UI
- Advanced CVE lookup based on grabbed banners
- OS Fingerprinting
