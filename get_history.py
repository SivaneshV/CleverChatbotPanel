import json, os, datetime
import uuid
import config

cfg = config.Config()

config_details = cfg.get_app_configs()

chat_msg_time_format = '%d/%m/%y %H:%M:%S'

if not os.path.exists('History'):
    os.makedirs('History')

def check_buffer_time_to_clear(chats, uid):
    if chats != '':
        chat_his = chats["chats"]
        time_his = []
        if len(chat_his) > 0:
            for chat_h in chat_his:
                time_his.append(chat_h["time"])
            
            max_time = max(time_his)
            max_time = datetime.datetime.strptime(max_time, chat_msg_time_format)
            # cur_time = datetime.datetime.strptime(datetime.datetime.now(), "%d/%m/%y %H:%M:%S")
            cur_time = datetime.datetime.now()
            diff = (cur_time - max_time).total_seconds() / 60.0
            
            chat_clear_buffer_min = int(config_details["chat_clear_buffer_min"])

            if chat_clear_buffer_min < diff:
                chats = {"uid": uid, "chats": []}

    return chats

class History:
    def __init__(self):
        pass

    def check_generate_uid(self, uid):
        if uid == '' or uid == 'null':
            uid = str(uuid.uuid4())
        return uid

    def check_update_history(self, uid, cur_user_chat, cur_bot_chat, disp_t):
        
        json_data = {
            "uid": uid,
            "chats": []
        }

        history_path = 'History/' + uid + '.json'

        try:

            if os.path.exists(history_path):
                with open(history_path) as outfile:
                    json_data = outfile.read()
                    json_data = json.loads(json_data)

            
            #json_data = check_buffer_time_to_clear(json_data, uid)
            

            json_data_chats = json_data["chats"]
            cur_json = {
                "message": cur_user_chat,
                "who": "user",
                "time": str(datetime.datetime.now().strftime(chat_msg_time_format)),
                "display_time": disp_t
            }
            json_data_chats.append(cur_json)
            cur_json = {
                "message": cur_bot_chat,
                "who": "bot",
                "time": str(datetime.datetime.now().strftime(chat_msg_time_format)),
                "display_time": disp_t
            }
            json_data_chats.append(cur_json)

            if not os.path.exists(history_path):
                with open(history_path, 'w') as outfile:  
                    json.dump(json_data, outfile)
            else:
                with open(history_path, 'r+') as outfile:  
                    json.dump(json_data, outfile)
            
        except Exception as e:
            try:
                os.remove(history_path)
            except:
                pass
            
            try:
                if os.path.exists(history_path):
                    with open(history_path) as outfile:
                        json_data = outfile.read()
                        json_data = json.loads(json_data)

                json_data = check_buffer_time_to_clear(json_data, uid)

                json_data_chats = json_data["chats"]
                cur_json = {
                    "message": cur_user_chat,
                    "who": "user",
                    "time": str(datetime.datetime.now().strftime(chat_msg_time_format)),
                    "display_time": disp_t
                }
                json_data_chats.append(cur_json)
                cur_json = {
                    "message": cur_bot_chat,
                    "who": "bot",
                    "time": str(datetime.datetime.now().strftime(chat_msg_time_format)),
                    "display_time": disp_t
                }
                json_data_chats.append(cur_json)

                if not os.path.exists(history_path):
                    with open(history_path, 'w') as outfile:  
                        json.dump(json_data, outfile)
                else:
                    with open(history_path, 'r+') as outfile:  
                        json.dump(json_data, outfile)
            except:
                pass
            pass
        
        return json_data

    def check_update_bot_history(self, uid, cur_bot_chat, disp_t):
        
        json_data = {
            "uid": uid,
            "chats": []
        }
        isAvoid = False

        try:
            history_path = 'History/' + uid + '.json'

            if os.path.exists(history_path):
                with open(history_path) as outfile:
                    json_data = outfile.read()
                    json_data = json.loads(json_data)

            json_data = check_buffer_time_to_clear(json_data, uid)

            json_data_chats = json_data["chats"]
            
            for dat in json_data_chats:
                if dat["message"] == cur_bot_chat:
                    isAvoid = True

            if isAvoid == False:
                cur_json = {
                    "message": cur_bot_chat,
                    "who": "bot",
                    "time": str(datetime.datetime.now().strftime(chat_msg_time_format)),
                    "display_time": disp_t
                }

                json_data_chats.append(cur_json)

                if not os.path.exists(history_path):
                    with open(history_path, 'w') as outfile:
                        json.dump(json_data, outfile)
                else:
                    with open(history_path, 'r+') as outfile:
                        json.dump(json_data, outfile)
            
        except Exception as e:
            try:
                os.remove(history_path)
            except:
                pass
            
            try:
                if os.path.exists(history_path):
                    with open(history_path) as outfile:
                        json_data = outfile.read()
                        json_data = json.loads(json_data)

                json_data = check_buffer_time_to_clear(json_data, uid)

                json_data_chats = json_data["chats"]
                
                for dat in json_data_chats:
                    if dat["message"] == cur_bot_chat:
                        isAvoid = True
                        
                if isAvoid == False:
                    cur_json = {
                        "message": cur_bot_chat,
                        "who": "bot",
                        "time": str(datetime.datetime.now().strftime(chat_msg_time_format)),
                        "display_time": disp_t
                    }

                    json_data_chats.append(cur_json)

                    if not os.path.exists(history_path):
                        with open(history_path, 'w') as outfile:  
                            json.dump(json_data, outfile)
                    else:
                        with open(history_path, 'r+') as outfile:  
                            json.dump(json_data, outfile)
            except Exception as e:
                print('Error : ' + str(e))
                pass
            
            pass
        
        return isAvoid

    def get_history_alone(self, uid, finder, geneset, disp_t, UIProtocolHostName, domain, cust_id):
        history_path = 'History/' + uid + '.json'
        json_data = {
            "uid": uid,
            "chats": []
        }

        try:
            if os.path.exists(history_path):
                with open(history_path) as outfile:
                    json_data = outfile.read()
                    json_data = json.loads(json_data)
        except:
            json_data = {
                "uid": uid,
                "chats": []
            }   
            pass
        
        
        json_data = check_buffer_time_to_clear(json_data, uid)
        

        if len(json_data["chats"]) <= 0:
            res_json = finder.get_welcome_message(domain, cust_id)
            
            welcome_response = geneset.generate_response(res_json, UIProtocolHostName)

            json_data = {
                "chats": [{
                    "message": welcome_response,
                    "who": "bot",
                    "time": str(datetime.datetime.now().strftime(chat_msg_time_format)),
                    "display_time": disp_t
                }],
                "uid": uid
            }
        
        cur_response = json_data["chats"][len(json_data["chats"]) - 1]

        seperate_response = ''
        if 'can you rephrase your question' not in cur_response and "Thank you, I'm so glad I could help " not in cur_response and str(cur_response["message"]).find("How can I help you") == -1:
            #seperate_response = seperate_response + '<div id="lookingfeedback"><div class="chat-text-divider"></div>'
            seperate_response = seperate_response + '<p>Is there anything else you are looking for?</p>'
            seperate_response = seperate_response + '<button class="chat-feedback-button-no" onclick="feedbacklookingno()">No</button>'
            seperate_response = seperate_response + '<button class="chat-feedback-button-yes" onclick="feedbacklookingyes()">Yes</button>'#</div>

        json_data["chats"][len(json_data["chats"]) - 1]["seperate_response"] = seperate_response;

        if not os.path.exists(history_path):
            with open(history_path, 'w') as outfile:  
                json.dump(json_data, outfile)
        
        return json_data
