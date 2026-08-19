from collections import Counter
import re


FAILED_LOGIN_THRESHOLD = 3


def analyze_log_file(file_path):
    failed_attempts = Counter()

    with open(file_path, "r", encoding="utf-8") as log_file:
        for line in log_file:
            if "Failed Login" not in line:
                continue

            ip_match = re.search(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                line
            )

            if ip_match:
                ip_address = ip_match.group()
                failed_attempts[ip_address] += 1

    suspicious_ips = {
        ip: count
        for ip, count in failed_attempts.items()
        if count >= FAILED_LOGIN_THRESHOLD
    }

    return {
        "failed_attempts": dict(failed_attempts),
        "suspicious_ips": suspicious_ips,
    }