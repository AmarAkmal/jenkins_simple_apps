import urllib.request
import urllib.parse
import sys
import os
import re

MAX_LEN = 4000


def send_message(text):
    token = os.environ.get("BOT_TOKEN", "")
    chat_id = os.environ.get("CHAT_ID", "")
    if not token or not chat_id:
        raise SystemExit("BOT_TOKEN and CHAT_ID env vars are required")
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data)


def parse_log(path):
    passed = []
    failed = []
    with open(path) as f:
        for line in f:
            m = re.search(r"::(\w+) (PASSED|FAILED)", line)
            if m:
                name, result = m.group(1), m.group(2)
                if result == "PASSED":
                    passed.append(name)
                else:
                    failed.append(name)
    return passed, failed


def main():
    job = os.environ.get("JOB_NAME", "?")
    build = os.environ.get("BUILD_NUMBER", "?")

    lines = [f"\U0001f517 Jenkins: {job} #{build}\n"]

    log_file = "build.log"
    if os.path.exists(log_file):
        passed, failed = parse_log(log_file)
        for t in passed:
            lines.append(f"\u2705 {t}")
        for t in failed:
            lines.append(f"\u274c {t}")
        if passed or failed:
            lines.append(f"\nTotal: {len(passed)} passed, {len(failed)} failed")
    else:
        lines.append("No test results found")

    msg = "\n".join(lines)
    if len(msg) > MAX_LEN:
        msg = msg[:MAX_LEN] + "\n...(truncated)"

    send_message(msg)


if __name__ == "__main__":
    main()
