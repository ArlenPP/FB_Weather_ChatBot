from bottle import Bottle, route, run, request, abort, static_file

import states_config
import global_config
import os
import send
from fsm import TocMachine

app = Bottle()

VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")
PORT = os.environ['PORT']

@app.route("/yiju", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge
    else:
        abort(403)

@app.route("/yiju", method="POST")
def webhook_handler():
    body = request.json
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        if event.get("message"):
            text = event['message']['text']
            sender_id = event['sender']['id']
            send.send_start(sender_id, text)
        return 'OK'


if __name__ == "__main__":
    # machine = TocMachine(
    #     states = states_config.states,
    #     transitions = states_config.transitions,
    #     initial = 'state_init',
    #     auto_transitions = False,
    #     show_conditions = True
    # )
    app.run(host="0.0.0.0", port=PORT, debug=True, reloader=True)
