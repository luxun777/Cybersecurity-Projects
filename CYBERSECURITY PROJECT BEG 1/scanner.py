import socket
import requests
import urllib3
from datetime import datetime
import json
import os

# Disable insecure request warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COMMON_PORTS = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    139: 'NetBIOS',
    143: 'IMAP',
    443: 'HTTPS',
    3306: 'MySQL',
    8080: 'HTTP Alternate'
}

SECURITY_HEADERS = [
    'Content-Security-Policy',
    'X-Frame-Options',
    'X-Content-Type-Options',
    'Strict-Transport-Security',
    'X-XSS-Protection'
]

class VulnerabilityScanner:
    def __init__(self, target):
        self.target = target
        self.ip = self._resolve_target(target)
        self.results = {
            'target': target,
            'ip': self.ip,
            'timestamp': datetime.now().isoformat(),
            'open_ports': [],
            'missing_headers': [],
            'weak_configs': [],
            'vulnerabilities': [],
            'score': 100
        }

    def _resolve_target(self, target):
        try:
            # Remove protocol if present
            if "://" in target:
                target = target.split("://")[1]
            if "/" in target:
                target = target.split("/")[0]
            return socket.gethostbyname(target)
        except socket.gaierror:
            return None

    def scan_ports(self):
        if not self.ip:
            return

        for port, service in COMMON_PORTS.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                result = sock.connect_ex((self.ip, port))
                if result == 0:
                    banner = self.grab_banner(sock)
                    port_info = {
                        'port': port,
                        'service': service,
                        'banner': banner
                    }
                    self.results['open_ports'].append(port_info)
                    self._analyze_port_vulnerability(port, service)
                sock.close()
            except Exception as e:
                pass

    def grab_banner(self, sock):
        try:
            sock.send(b'HEAD / HTTP/1.1\r\n\r\n')
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner[:100] if banner else "No banner"
        except:
            return "No banner"

    def check_security_headers(self):
        if not self.ip:
            return

        # Default to HTTPS, fall back to HTTP
        urls = [f"https://{self.target}", f"http://{self.target}"]
        if "://" in self.target:
            urls = [self.target]

        headers = {}
        successful_url = None

        for url in urls:
            try:
                response = requests.get(url, timeout=5, verify=False)
                headers = response.headers
                successful_url = url
                break
            except requests.exceptions.RequestException:
                continue

        if not successful_url:
            self.results['vulnerabilities'].append({
                'title': 'Target Unreachable',
                'description': 'Could not connect to the target over HTTP/HTTPS.',
                'severity': 'High'
            })
            return

        # Check for weak HTTP usage
        if successful_url.startswith("http://"):
            self.results['weak_configs'].append({
                'config': 'HTTP Usage',
                'description': 'Target is using unencrypted HTTP.'
            })
            self.results['vulnerabilities'].append({
                'title': 'Unencrypted Communications',
                'description': 'The application does not enforce HTTPS.',
                'severity': 'Medium'
            })

        for header in SECURITY_HEADERS:
            if header not in headers:
                self.results['missing_headers'].append(header)
                self.results['vulnerabilities'].append({
                    'title': f'Missing Header: {header}',
                    'description': f'The {header} security header is not set.',
                    'severity': 'Low'
                })

    def _analyze_port_vulnerability(self, port, service):
        if port == 21:
            self.results['weak_configs'].append({'config': 'FTP Exposure', 'description': 'FTP port 21 is open.'})
            self.results['vulnerabilities'].append({
                'title': 'Insecure Service: FTP',
                'description': 'FTP transmits data in cleartext.',
                'severity': 'Medium'
            })
        elif port == 23:
            self.results['weak_configs'].append({'config': 'Telnet Exposure', 'description': 'Telnet port 23 is open.'})
            self.results['vulnerabilities'].append({
                'title': 'Insecure Service: Telnet',
                'description': 'Telnet transmits data in cleartext and is highly insecure.',
                'severity': 'High'
            })
        elif port == 3306:
            self.results['weak_configs'].append({'config': 'Database Exposure', 'description': 'MySQL port 3306 is exposed to the network.'})
            self.results['vulnerabilities'].append({
                'title': 'Database Port Exposed',
                'description': 'Database services should not be directly exposed to the internet.',
                'severity': 'High'
            })

    def calculate_score(self):
        score = 100
        for vuln in self.results['vulnerabilities']:
            if vuln['severity'] == 'High':
                score -= 20
            elif vuln['severity'] == 'Medium':
                score -= 10
            elif vuln['severity'] == 'Low':
                score -= 5
        self.results['score'] = max(0, score)

    def generate_report(self):
        os.makedirs("reports", exist_ok=True)
        safe_target = self.target.replace("://", "_").replace("/", "_").replace(":", "_")
        filename = f"reports/scan_{safe_target}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        self.results['report_file'] = filename

    def run(self):
        if not self.ip:
            return {"error": "Could not resolve target IP."}
        
        self.scan_ports()
        self.check_security_headers()
        self.calculate_score()
        self.generate_report()
        return self.results
