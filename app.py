from bottle import route, run, request, abort, static_file

from fsm import TocMachine
import states_config
import global_config

@route("/yiju", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        sender_id = event['sender']['id']

        if sender_id in global_config.id_list[0]:
            global_config.get_state(sender_id)
            if machine.state == 'state_init':
                machine.go_to(event)
            else:
                machine.advance(event)
        else:
            global_config.set_id(sender_id)
            global_config.set_state(sender_id,'state_init')
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
    machine.get_graph().draw('show-fsm.png', prog='dot')
    run(host="localhost", port=1029, debug=True, reloader=True)