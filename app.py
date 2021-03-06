from bottle import Bottle, route, run, request, abort, static_file

from fsm import TocMachine
import states_config
import global_config
import os

Hi chatbot 

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
    goto_list = ['state_init', 'oneweek_state4', 'ask_temp_state5', 'ask_rain_state6', 'ask_pheno_state7']

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        sender_id = event['sender']['id']

        if sender_id in global_config.id_list[0]:
            machine.state = global_config.get_state(sender_id)
            print('\nFSM STATE: ' + machine.state)
            if machine.state in goto_list:
                machine.go_to(event)
            elif machine.state == 'finish_state9':
                machine.go_back(event)
            else:
                machine.advance(event)
        else:
            global_config.set_id(sender_id)
            print('\nNew user: ' + sender_id)
            global_config.set_state(sender_id,'state_init')
            print('\nFSM STATE: ' + machine.state)
            machine.state = 'state_init'
            machine.go_to(event)
        return 'OK'

if __name__ == "__main__":
    machine = TocMachine(
        states = states_config.states,
        transitions = states_config.transitions,
        initial = 'state_init',
        auto_transitions = False,
        show_conditions = True
    )
    # machine.get_graph().draw('show-fsm.png', prog='dot')
    app.run(host="0.0.0.0", port=PORT, debug=True, reloader=True)
