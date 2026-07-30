import urllib.request
import urllib.parse
import sys
import os

TOKEN = "8738868776:AAHbKTBfFItG7ATSEd5BuR5c_M3NJZSaO7w"
CHAT_ID = "1203641879"
MAX_MSG = 4000


def send(text):
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data)


def main():
    job = os.environ.get("JOB_NAME", "?")
    build = os.environ.get("BUILD_NUMBER", "?")
    status = sys.argv[1] if len(sys.argv) > 1 else "?"

    log_file = "build.log"
    log_text = ""
    if os.path.exists(log_file):
        with open(log_file) as f:
            log_text = f.read()

    if status == "success":
        summary = f"PASSED ({log_text.count('PASSED')} passed, {log_text.count('FAILED')} failed)"
    else:
        summary = "FAILED"

    msg = f"{'✅' if status == 'success' else '❌'} Jenkins: {job} #{build} {summary}\n\n"

    if log_text:
        log_lines = log_text.strip().split("\n")
        tail = [l for l in log_lines if "PASSED" in l or "FAILED" in l or "ERROR" in l or "error" in l]
        if tail:
            msg += "\n".join(tail[-10:])

    if len(msg) > MAX_MSG:
        msg = msg[:MAX_MSG] + "\n...(truncated)"

    send(msg)


if __name__ == "__main__":
    main()
