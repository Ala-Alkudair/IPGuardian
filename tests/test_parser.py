from app.log_parser import analyze_log_file


def test_detect_suspicious_ip(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "2026-08-15 10:00:01 192.168.1.10 Failed Login\n"
        "2026-08-15 10:00:05 192.168.1.10 Failed Login\n"
        "2026-08-15 10:00:09 192.168.1.10 Failed Login\n",
        encoding="utf-8",
    )

    result = analyze_log_file(log_file)

    assert result["failed_attempts"]["192.168.1.10"] == 3
    assert result["suspicious_ips"]["192.168.1.10"] == 3


def test_ip_below_threshold_is_not_suspicious(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "2026-08-15 10:00:01 192.168.1.40 Failed Login\n"
        "2026-08-15 10:00:05 192.168.1.40 Failed Login\n",
        encoding="utf-8",
    )

    result = analyze_log_file(log_file)

    assert result["failed_attempts"]["192.168.1.40"] == 2
    assert "192.168.1.40" not in result["suspicious_ips"]


def test_successful_login_is_not_counted(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "2026-08-15 10:01:15 192.168.1.20 Successful Login\n",
        encoding="utf-8",
    )

    result = analyze_log_file(log_file)

    assert "192.168.1.20" not in result["failed_attempts"]
    assert "192.168.1.20" not in result["suspicious_ips"]


def test_sample_log_file_matches_expected_results():
    result = analyze_log_file("sample_logs/auth.log")

    assert result["failed_attempts"] == {
        "192.168.1.10": 3,
        "192.168.1.30": 4,
    }
    assert result["suspicious_ips"] == {
        "192.168.1.10": 3,
        "192.168.1.30": 4,
    }
    assert "192.168.1.20" not in result["failed_attempts"]