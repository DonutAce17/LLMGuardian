#!/usr/bin/env python3
import hashlib
import argparse
import time
import re
import requests
import sys
import os

# ✅ Final fixed SHA256 hash of this exact file
EXPECTED_HASH = "6cf3a7a97e13d9cba734d06311a174992197999cc03872884261fc6e1abf1dc2"

# 🌐 LLM security patterns
INJECTION_PATTERNS = [
    r"(ignore|bypass|disable)\s+(safety|filter|alignment)",
    r"(pretend|act)\s+as\s+.*?jailbroken",
    r"(you are.*?not an ai|you are a human)",
    r"(repeat after me:|say exactly this:)",
    r"(simulate|impersonate|emulate).*?malicious",
]

def calculate_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def check_integrity():
    script_path = os.path.realpath(__file__)
    current_hash = calculate_sha256(script_path)
    if current_hash != EXPECTED_HASH:
        print("[LLM Guardian] ⚠ Integrity verification failed! Possible tampering detected.")
        sys.exit(1)
    print("[LLM Guardian] ✅ Code integrity verified.")

def detect_threats(input_text):
    threats = []
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, input_text, re.IGNORECASE):
            threats.append(pattern)
    return threats

def simulate_llm_response(input_text):
    # Dummy response simulation (replace with real model or API call)
    return f"LLM response to: {input_text}"

def secure_request(url, input_text):
    try:
        headers = {'User-Agent': 'LLMGuardian/1.0'}
        response = requests.post(url, json={'prompt': input_text}, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            return f"[!] Error from URL: {response.status_code}"
    except Exception as e:
        return f"[!] Request failed: {e}"

def main():
    parser = argparse.ArgumentParser(description="🛡️ LLM Guardian - AI Security Monitor")
    parser.add_argument("--input", required=True, help="Input prompt for LLM")
    parser.add_argument("--output", required=True, help="Output file to store response")
    parser.add_argument("--secure-mode", action="store_true", help="Enable integrity & jailbreak protection")
    parser.add_argument("--url", help="Optional LLM API endpoint for online testing")
    args = parser.parse_args()

    if args.secure_mode:
        print("[LLM Guardian] 🔒 Secure mode activated.")
        check_integrity()

    threats = detect_threats(args.input)
    if threats:
        print("[!] 🚨 Potential jailbreak or malicious prompt detected!")
        for t in threats:
            print(f" ⚠ Pattern matched: {t}")
        sys.exit(1)

    if args.url:
        print("[LLM Guardian] 🌐 Contacting external LLM API...")
        response = secure_request(args.url, args.input)
    else:
        response = simulate_llm_response(args.input)

    with open(args.output, "w") as f:
        f.write(response)

    print(f"[LLM Guardian] ✅ Response saved to: {args.output}")

if __name__ == "__main__":
    main()

