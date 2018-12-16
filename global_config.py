id_list = []
id_list.append([])
id_list.append([])
id_list.append([])

def set_id(sender_id):
    '''設定使用者id'''
    id_list[0].append(sender_id)
    print('新使用者: ')
    print(id_list[0].index(sender_id))

def set_state(sender_id, state):
    '''設定使用者state的狀態'''
    index = id_list[0].index(sender_id)
    id_list[1].insert(index, state)
    print(state)

def get_state(sender_id):
    '''拿使用者state的狀態'''
    index = id_list[0].index(sender_id)
    print(index)
    return id_list[1][index]

def set_zone(sender_id, zone):
    '''設定使用者的地區'''
    index = id_list[0].index(sender_id)
    id_list[2].insert(index, zone)
    print(zone)

def get_zone(sender_id):
    '''拿使用者的地區'''
    index = id_list[0].index(sender_id)
    return id_list[2][index]