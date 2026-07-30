import urllib.request
import urllib.parse
import sys
import os
import io
import uuid

TOKEN = "8738868776:AAHbKTBfFItG7ATSEd5BuR5c_M3NJZSaO7w"
CHAT_ID = "1203641879"


def send_message(text):
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data)


def send_document(file_path, caption=""):
    boundary = uuid.uuid4().hex
    body = io.BytesIO()

    def w(s):
        body.write(s.encode())

    if caption:
        w(f"--{boundary}\r\n")
        w('Content-Disposition: form-data; name="caption"\r\n\r\n')
        w(f"{caption}\r\n")

    w(f"--{boundary}\r\n")
    w(f'Content-Disposition: form-data; name="document"; filename="build.log"\r\n')
    w("Content-Type: text/plain\r\n\r\n")
    with open(file_path, "rb") as f:
        body.write(f.read())
    w("\r\n")
    w(f"--{boundary}--\r\n")

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/sendDocument",
        data=body.getvalue(),
    )
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    urllib.request.urlopen(req)


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
