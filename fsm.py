from transitions.extensions import GraphMachine

import global_config
import send

zone = ['東區', '南區', '北區', '安南區', '安平區', '中西區', '新營區', '鹽水區', '白河區', '柳營區', '後壁區', '東山區',
        '麻豆區', '下營區', '六甲區', '官田區', '大內區', '佳里區', '學甲區', '西港區', '七股區', '將軍區', '北門區',
        '新化區', '善化區', '新市區', '安定區', '山上區', '玉井區', '楠西區', '南化區', '左鎮區', '仁德區', '歸仁區', 
        '關廟區', '龍崎嶇', '永康區']
yes = ['想', '好', '是', 'yes', 'Yes', '要']
no = ['不想', '不好', '不是', 'no', 'No', '不要', '不']

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_state1(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text.find("天氣") == 0:
                    return True
                else:
                    # print(text)
                    return False

    # def not_going_to_state1(self, event):
    #     if event.get("message"):
    #         text = event['message']['text']
    #         if text.find("天氣") == 0:
    #             return False
    #         else:
    #             print(text)
    #             return True

    def is_going_to_state2(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                sender_id = event['sender']['id']
                if text in zone:
                    global_config.set_zone(sender_id, text)
                    return True
                else:
                    global_config.set_zone(event['sender']['id'], '東區')  # 預設
                    return False

    def is_going_to_state3(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text.find("現在") == 0:
                    return True
                else:
                    return False

    def is_going_to_state4(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text.find("一週") == 0:
                    return True
                else:
                    return False
    
    def is_going_to_state4_2(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text in yes:
                    return True
                else:
                    return False

    def not_going_to_state4_2(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text in no:
                    return True
                else:
                    return False
    
    def is_going_to_state5(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text.find("溫度") == 0:
                    return True
                else:
                    return False

    def is_going_to_state6(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text.find("降雨") == 0:
                    return True
                else:
                    return False

    def is_going_to_state7(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text.find("天氣狀態") == 0 or text.find("天氣狀況") == 0:
                    return True
                else:
                    return False

    def is_going_to_state9(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text.find("結束") == 0:
                    return True
                else:
                    return False
        
    def on_enter_start_state0(self, event):
        print("I'm entering state0")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'start_state0')
        send.send_start(sender_id,"嗨~\n有什麼想問的嗎?")

    def on_enter_ask_zone_state1(self, event):
        print("I'm entering state1")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'ask_zone_state1')
        send.send_start(sender_id,"你想知道台南的哪個地區呢?\n")

    def on_enter_ask_interval_state2(self, event):
        print("I'm entering state2")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'ask_interval_state2')
        send.send_start(sender_id,"你想問\"現在\"還是未來\"一週\"的天氣?")

    def on_enter_realtime_state3(self, event):
        print("I'm entering state3")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'realtime_state3')
        send.send_start(sender_id,"你想知道\"溫度\"還是\"降雨機率\"還是\"天氣狀態\"?")

    def on_enter_oneweek_state4(self, event):
        print("I'm entering state4")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'oneweek_state4')
        send.forecast_1week(sender_id, global_config.get_zone(sender_id))
        self.go_to(event)

    def on_enter_ask_temp_state5(self, event):
        print("I'm entering state5")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'ask_temp_state5')
        send.forecast_3day_temp(sender_id, global_config.get_zone(sender_id))
        self.go_to(event)

    def on_enter_ask_rain_state6(self, event):
        print("I'm entering state6")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'ask_rain_state6')
        send.forecast_3day(sender_id, global_config.get_zone(sender_id), 'PoP6h')
        self.go_to(event)

    def on_enter_ask_pheno_state7(self, event):
        print("I'm entering state7")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'ask_pheno_state7')
        send.forecast_3day(sender_id, global_config.get_zone(sender_id), 'Wx')
        self.go_to(event)

    def on_enter_ask_oneweek_state8(self, event):
        print("I'm entering state8")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'ask_oneweek_state8')
        send.send_start(sender_id,"你還想知道未來一週的天氣嗎?")

    def on_enter_finish_state9(self, event):
        print("I'm entering state9")

        sender_id = event['sender']['id']
        global_config.set_state(sender_id,'finish_state9')
        send.send_start(sender_id,"歡迎下次再來詢問天氣~")
        self.go_back(event)
