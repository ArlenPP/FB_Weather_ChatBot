from bottle import route, run, request, abort, static_file

import os

VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")
# VERIFY_TOKEN = "yiju20181212"

@route("/yiju", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge
    else:
        abort(403)

if __name__ == "__main__":
    run(host="localhost", port=1029, debug=True, reloader=True)
