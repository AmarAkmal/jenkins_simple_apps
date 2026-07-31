import urllib.request
import urllib.parse
import sys
import os
import re
import time

MAX_LEN = 4000

ICON = {
    "success": "\U0001f7e2",
    "failure": "\U0001f534",
    "unstable": "\U0001f7e1",
    "aborted": "\u26a0\ufe0f",
}


def send_message(text):
    token = os.environ.get("BOT_TOKEN", "")
    chat_id = os.environ.get("CHAT_ID", "")
    if not token or not chat_id:
        raise SystemExit("BOT_TOKEN and CHAT_ID env vars are required")
    data = urllib.parse.urlencode(
        {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": "true"}
    ).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data)


def html_escape(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


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


def fmt_duration(ms):
    try:
        ms = int(float(ms))
    except (TypeError, ValueError):
        return "?"
    s = ms / 1000
    if s < 60:
        return f"{s:.1f}s"
    return f"{int(s // 60)}m {int(s % 60)}s"


def main():
    status = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BUILD_STATUS", "success")
    status = status.lower() if status else "success"
    icon = ICON.get(status, "\U0001f7e2")

    job = os.environ.get("JOB_NAME", "?")
    build = os.environ.get("BUILD_NUMBER", "?")
    branch = os.environ.get("GIT_BRANCH", os.environ.get("BRANCH_NAME", "?"))
    commit = (os.environ.get("GIT_COMMIT") or "?")[:7]
    author = os.environ.get("GIT_AUTHOR_NAME", "?")
    url = os.environ.get("BUILD_URL", "")
    duration = fmt_duration(os.environ.get("BUILD_DURATION", ""))

    lines = [f"{icon} <b>CI {status.upper()}</b> {html_escape(job)} #{build}"]
    lines.append("")
    lines.append(f"Branch: <code>{html_escape(branch)}</code>")
    lines.append(f"Commit: <code>{html_escape(commit)}</code> by {html_escape(author)}")
    lines.append(f"Duration: {duration}")
    if url:
        lines.append(f"Logs: <a href=\"{html_escape(url)}\">Open Jenkins</a>")

    log_file = "build.log"
    if os.path.exists(log_file):
        passed, failed = parse_log(log_file)
        if passed or failed:
            lines.append("")
            lines.append(f"\U0001f4ca <b>Test results: {len(passed)} \u2705 / {len(failed)} \u274c</b>")
            for t in passed:
                lines.append(f"\u2705 {html_escape(t)}")
            for t in failed:
                lines.append(f"\u274c {html_escape(t)}")

    msg = "\n".join(lines)
    if len(msg) > MAX_LEN:
        msg = msg[:MAX_LEN] + "\n\u2026(truncated)"

    send_message(msg)


if __name__ == "__main__":
    main()
