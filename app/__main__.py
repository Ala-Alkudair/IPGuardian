import sys

from app.log_parser import analyze_log_file


def main():
    log_path = sys.argv[1] if len(sys.argv) > 1 else "sample_logs/auth.log"

    result = analyze_log_file(log_path)

    for ip, count in result["failed_attempts"].items():
        status = "Suspicious" if ip in result["suspicious_ips"] else "Normal"
        print(f"{ip} -> {count} Failed Login -> {status}")


if __name__ == "__main__":
    main()
