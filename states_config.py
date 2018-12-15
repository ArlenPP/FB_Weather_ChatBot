states=[
    'state_init',
    'start_state0',
    'ask_zone_state1',
    'ask_interval_state2',
    'realtime_state3',
    'oneweek_state4',
    'ask_temp_state5',
    'ask_rain_state6',
    'ask_pheno_state7',
    'ask_oneweek_state8',
    'finish_state9'
]
transitions=[
    {
        'trigger': 'go_to',
        'source': 'state_init',
        'dest': 'start_state0',
    },
    {
        'trigger': 'advance',
        'source': 'start_state0',
        'dest': 'ask_zone_state1',
        'conditions': 'is_going_to_state1'
    },
    {
        'trigger': 'advance',
        'source': 'ask_zone_state1',
        'dest': 'ask_interval_state2',
        'conditions': 'is_going_to_state2'
    },
    {
        'trigger': 'advance',
        'source': 'ask_interval_state2',
        'dest': 'realtime_state3',
        'conditions': 'is_going_to_state3'
    },
    {
        'trigger': 'advance',
        'source': 'ask_interval_state2',
        'dest': 'oneweek_state4',
        'conditions': 'is_going_to_state4'
    },
    {
        'trigger': 'advance',
        'source': 'realtime_state3',
        'dest': 'ask_temp_state5',
        'conditions': 'is_going_to_state5'
    },
    {
        'trigger': 'advance',
        'source': 'realtime_state3',
        'dest': 'ask_rain_state6',
        'conditions': 'is_going_to_state6'
    },
    {
        'trigger': 'advance',
        'source': 'realtime_state3',
        'dest': 'ask_pheno_state7',
        'conditions': 'is_going_to_state7'
    },
    {
        'trigger': 'go_back',
        'source': ['ask_temp_state5','ask_rain_state6','ask_pheno_state7'],
        'dest': 'ask_oneweek_state8',
    },
    {
        'trigger': 'advance',
        'source': 'ask_oneweek_state8',
        'dest': 'oneweek_state4',
        'conditions': 'is_going_to_state4_2'
    },
    {
        'trigger': 'go_back',
        'source': 'oneweek_state4',
        'dest': 'finish_state9',
    },
    {
        'trigger': 'advance',
        'source': [
            'ask_zone_state1',
            'ask_interval_state2',
            'realtime_state3',
            'ask_temp_state5',
            'ask_rain_state6',
            'ask_pheno_state7',
            'ask_oneweek_state8'
        ],
        'dest': 'finish_state9',
        'conditions': 'is_going_to_state9'
    },
    {
        'trigger': 'go_back',
        'source': 'finish_state9',
        'dest': 'start_state0',
    }
]