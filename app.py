from bottle import route, run, request, abort, static_file

from fsm import TocMachine
import states_config

@route("/yiju", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        if machine.state == 'state_init':
            machine.go_to(event)
        else:
            machine.advance(event)
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