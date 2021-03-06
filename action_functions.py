import player_data
import scratch_interface


def get_point_values(server_messages, users, user_index, activity, value_remaining):
    print("Returning get point values for: ",activity['user'])
    scratch_interface.server_buffer_send(server_messages, activity['user'],'0',users[user_index].get_values())
    return server_messages    

def start_pairing(server_messages, users, user_index, activity, value_remaining):
    pass

def end_pairing(server_messages, users, user_index, activity, value_remaining):
    pass

def buy_card(server_messages, users, user_index, activity, value_remaining):
    if len(value_remaining)<2:
        return
    card_id = value_remaining[:2]
    print(activity['user'],"bought",card_id)
    users[user_index].buy_card(card_id)

def send_message(server_messages, users, user_index, activity, value_remaining):
    pass

def get_message_with_index(server_messages, users, user_index, activity, value_remaining):
    pass

def get_message_count(server_messages, users, user_index, activity, value_remaining):
    pass
    
actions_on_recieve = {
    0: get_point_values,
    1: start_pairing,
    2: end_pairing,
    3: buy_card,
    4: send_message,
    5: get_message_with_index,
    6: get_message_count
}

#Finds the index of the user data object with the specified username. Returns none on failiure.
def try_get_user(username, users):
    match = [index for index in range(len(users)) if users[index].username == username]
    if len(match)==0:
        return None
    else:
        return match[0]

def get_user(activity, users):
    user_index=try_get_user(activity['user'], users)
    print(activity)
    #New user
    if(user_index==None):
        print("New user: "+activity['user'])
        user_index = len(users)
        users.append(player_data.PlayerStaticData(activity['user']))
    return user_index

#Perform actions based on the new requests
def actions(server_messages, activities, users):
    for activity in activities:
        if activity['name'] == "☁ user" and activity['verb']=="set_var":#If it is actually a request
            user_index = get_user(activity, users)
            if len(activity['value'])<1:
                print("The request had no value")
                return
            request = activity['value'][0]
            #We find functions the function here based on the first digit of the value.
            func = actions_on_recieve.get(int(request))
            if func==None:
                print("The server had no function to handle the request.")
                return
            func (server_messages, users, user_index, activity, activity['value'][1:]) #Call the function
