import urllib.request
import urllib.parse
import sys
import os
import json
import uuid

TOKEN = "8738868776:AAHbKTBfFItG7ATSEd5BuR5c_M3NJZSaO7w"
CHAT_ID = "1203641879"


def send_message(text):
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data)


def send_document(file_path, caption=""):
    boundary = uuid.uuid4().hex
    parts = []

    def add_field(name, value):
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n")

    add_field("chat_id", CHAT_ID)
    if caption:
        add_field("caption", caption)

    with open(file_path, "rb") as f:
        content = f.read()
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"document\"; filename=\"build.log\"\r\nContent-Type: text/plain\r\n\r\n".encode())
    parts.append(content)
    parts.append(f"\r\n--{boundary}--\r\n".encode())

    body = b"".join(p.encode() if isinstance(p, str) else p for p in parts)

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/sendDocument",
        data=body,
    )
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def main():
    job = os.environ.get("JOB_NAME", "?")
    build = os.environ.get("BUILD_NUMBER", "?")
    status = sys.argv[1] if len(sys.argv) > 1 else "?"

    smile = "PASSED" if status == "success" else "FAILED"
    msg = f"Jenkins: {job} #{build} {smile}"

    log_file = "build.log"
    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        send_document(log_file, caption=msg)
    else:
        send_message(msg)


if __name__ == "__main__":
    main()
