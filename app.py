from bottle import route, run, request, abort, static_file

import send
# import states_config

@route("/yiju", method="POST")
def webhook_handler():
    body = request.json
    sender_id = body['entry'][0]['messaging'][0]['sender']['id']
    sender_text = body['entry'][0]['messaging'][0]['message']['text']
    
    if sender_text.find("天氣") == 0:
        send.forecast_36hr(sender_id,sender_text)
    elif sender_text.find("三天") == 0:
        send.forecast_3day(sender_id,"區","Wx")
    elif sender_text.find("溫度") == 0:
        send.forecast_3day_temp(sender_id,"區")
    elif sender_text.find("一週") == 0:
        send.forecast_1week(sender_id,sender_text)
    else:
        send.send_start(sender_id,"嗨~\n有什麼想問的嗎?")

#     body = request.json
#     print('\nFSM STATE: ' + machine.state)

#     if body['object'] == "page":
#         event = body['entry'][0]['messaging'][0]
#         machine.advance(event)
#         return 'OK'
    
if __name__ == "__main__":
    run(host="localhost", port=1029, debug=True, reloader=True)