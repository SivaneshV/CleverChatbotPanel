# %% Import(s)
import find_response
import response_generator
import get_history
from lazywritter import log_writter
from flask import Flask, request, flash, jsonify
import subprocess
import time
import datetime
import os
import sys
import config
import EnDe
from flask_cors import CORS
import auth
import json

def create_app():
    # %% Declaration(s)
    cfg = config.Config()

    application = Flask(__name__)
    CORS(application)

    logger = log_writter()

    geneset = response_generator.response_generator(logger)

    finder = find_response.response_finder(logger)

    unauthorized_msg = 'Unauthorized Access.'

    chat_msg_time_format = '%d/%m/%y %H:%M:%S'

    # %% Common


    @application.route('/', methods=['GET', 'POST'])
    def index():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass

        logger.write_activity('Index Logging Activity', 1)
        try:
            return "Welcome."
        except Exception as e:
            return str(e)

    @application.route('/getConfigs', methods=['GET', 'POST'])
    def getConfigs():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass

        config_details = cfg.get_ui_configs()
        
        configs = {
            "chat_timeout_sec": config_details["chat_timeout_sec"],
            "chat_anythingelse_sec": config_details["chat_anythingelse_sec"]
        }

        return configs
        
    @application.route('/feedback', methods=['GET', 'POST'])
    def feedback():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass

        history = get_history.History()
        feedback = request.headers.get('feedback')
        disp_t = request.form.get('disp_t')
        UIProtocolHostName = request.form.get('UIProtocolHostName')
        uid = request.args['uid']

        user_chat = "<p>" + feedback + "</p>"
        
        cur_response = ''
        if feedback.lower() == "yes":
            cur_response = cur_response + '<p>How may I help you?</p>'
        else:
            cur_response = cur_response + "<p>Thank you! I'm so glad I could help.</p>"

        history.check_update_history(uid, user_chat, cur_response, disp_t)

        IsLast = ""
        if "I'm so glad I could help" in cur_response:
            IsLast = "true"

        response = {
            "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t, "is_last": IsLast}],
            "uid": uid
        }

        return response
        
    @application.route('/timeouthit', methods=['GET', 'POST'])
    def timeouthit():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass

        history = get_history.History()
        disp_t = request.form.get('disp_t')
        uid = request.args['uid']
        
        cur_response = ''
        cur_response = cur_response + "<p>Hi, I am Clever Brain Assistant. How can I help you today?</p>"
        # cur_response = cur_response + '<button class="chat-feedback-button-no" onclick="feedbacklookingno()">No</button>'
        # cur_response = cur_response + '<button class="chat-feedback-button-yes" onclick="feedbacklookingyes()">Yes</button></div>'

        isAvoid = history.check_update_bot_history(uid, cur_response, disp_t)
        response = ''

        if isAvoid == False:
            response = {
                "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t}],
                "uid": uid
            }

        return response
        

    @application.route('/lookingfor', methods=['GET', 'POST'])
    def lookingfor():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass

        history = get_history.History()
        disp_t = request.form.get('disp_t')
        uid = request.args['uid']
        
        cur_response = ''
        cur_response = cur_response + '<p>Is there anything else you are looking for?</p>'
        cur_response = cur_response + '<button class="chat-feedback-button-no" onclick="feedbacklookingno()">No</button>'
        cur_response = cur_response + '<button class="chat-feedback-button-yes" onclick="feedbacklookingyes()">Yes</button>'
        
        #isAvoid = history.check_update_bot_history(uid, cur_response, disp_t)
        response = ''

        #if isAvoid == False:
        response = {
            "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t}],
            "uid": uid
        }

        return response

    # @application.route('/welcome', methods=['GET', 'POST'])
    # def welcome():

    #     try:
    #         auth_creds = request.authorization
    #         UIProtocolHostName = request.form.get('UIProtocolHostName')
    #         is_authorize = auth.Authorize(
    #             auth_creds.username, auth_creds.password)
    #         if is_authorize == False:
    #             return unauthorized_msg
    #     except Exception as d:
    #         return unauthorized_msg
    #         pass


    #     res_json = finder.get_welcome_message()

    #     response = geneset.generate_response(res_json,UIProtocolHostName)
    #     return response


    # @application.route('/pred', methods=['GET', 'POST'])
    # def pred():
    #     try:
    #         auth_creds = request.authorization
    #         is_authorize = auth.Authorize(
    #             auth_creds.username, auth_creds.password)
    #         if is_authorize == False:
    #             return unauthorized_msg
    #     except Exception as d:
    #         return unauthorized_msg
    #         pass

    #     user_chat = request.headers.get('conv')

    #     import predict

    #     preds = predict.predict(user_chat)

    #     response = {"intents": preds}

    #     return response


    # @application.route('/updatefeedback', methods=['GET', 'POST'])
    # def updatefeedback():
    #     try:
    #         auth_creds = request.authorization
    #         is_authorize = auth.Authorize(
    #             auth_creds.username, auth_creds.password)
    #         if is_authorize == False:
    #             return unauthorized_msg
    #     except Exception as d:
    #         return unauthorized_msg
    #         pass

    #     try:
    #         history = get_history.History()
    #         user_chat = request.headers.get('conv')
    #         disp_t = request.form.get('disp_t')
    #         UIProtocolHostName = request.form.get('UIProtocolHostName')
    #         uid = request.args['uid']
    #         is_recommend = False
    #         try:
    #             rec = request.args['rec']
    #             is_recommend = bool(rec)
    #         except:
    #             pass

    #         cur_response = geneset.generate_feedback_response()

    #         uid = history.check_generate_uid(uid)

    #         history.check_update_history(uid, user_chat, cur_response, disp_t)

    #         response = {
    #             "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t}],
    #             "uid": uid
    #         }
    #     except Exception as ee:
    #         logger.write_exception(str(ee), 'chatbot')
    #         response = {
    #             "chats": [{"message": str(ee), "who": "bot", "time":  datetime.datetime.now().strftime(chat_msg_time_format), "display_time": ""}],
    #             "uid": "Unknown"
    #         }

    #     return response


    @application.route('/chat', methods=['GET', 'POST'])
    def chatbot():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass

        try:
            history = get_history.History()
            disp_t = request.form.get('disp_t')
            UIProtocolHostName = request.form.get('UIProtocolHostName')
            user_input_chat = request.form.get('conv')
            
            user_chat=user_input_chat
            uid = request.args['uid']
            is_recommend = False
            try:
                rec = request.args['rec']
                is_recommend = bool(rec)
            except:
                pass

            corpus_path = get_corpus_path()
            general_intent_json_path = get_general_intent_json_path()
            intent_json_path = get_intent_json_path()
            
            res_json = finder.find_response(user_chat, corpus_path, general_intent_json_path, intent_json_path, is_recommend)
            
            cur_response = geneset.generate_response(res_json, UIProtocolHostName)
            
            uid = history.check_generate_uid(uid)
            
            history.check_update_history(uid, user_chat, cur_response, disp_t)
            
            seperate_response = ""

            IsLast = ""
            if "I'm so glad I could help" in cur_response:
                IsLast = "true"

            is_general = ''
            try:
                json_obj = json.loads(res_json)
                is_general = json_obj["is_general"]
            except:
                pass

            response = {
                "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t, "seperate_response": seperate_response, "is_last": IsLast, 'is_general': is_general}],
                "uid": uid
            }
        except Exception as ee:
            print(str(ee))
            logger.write_exception(str(ee), 'chatbot')
            response = {
                "chats": [{"message": str(ee), "who": "bot", "time":  datetime.datetime.now().strftime(chat_msg_time_format), "display_time": ""}],
                "uid": "Unknown"
            }

        return response


    # @application.route('/recommendchat', methods=['GET', 'POST'])
    # def recommendchat():
    #     try:
    #         auth_creds = request.authorization
    #         is_authorize = auth.Authorize(
    #             auth_creds.username, auth_creds.password)
    #         if is_authorize == False:
    #             return unauthorized_msg
    #     except Exception as d:
    #         return unauthorized_msg
    #         pass

    #     try:
    #         history = get_history.History()
    #         user_chat = request.headers.get('conv')
    #         disp_t = request.form.get('disp_t')
    #         UIProtocolHostName = request.form.get('UIProtocolHostName')
    #         uid = request.args['uid']

    #         res_json = finder.find_response(user_chat, True)
    #         cur_response = geneset.generate_response(res_json, UIProtocolHostName)
    #         uid = history.check_generate_uid(uid)

    #         history.check_update_history(uid, user_chat, cur_response, disp_t)

    #         response = {
    #             "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t}],
    #             "uid": uid
    #         }
    #     except Exception as ee:
    #         logger.write_exception(str(ee), 'recommendchat')
    #         response = {
    #             "chats": [{"message": str(ee), "who": "bot", "time":  datetime.datetime.now().strftime(chat_msg_time_format), "display_time": ""}],
    #             "uid": "Unknown"
    #         }

    #     return response


    @application.route('/chathistory', methods=['GET', 'POST'])
    def chathistory():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass

        disp_t = request.form.get('disp_t')
        UIProtocolHostName = request.form.get('UIProtocolHostName')
        history = get_history.History()
        uid = request.args['uid']

        uid = history.check_generate_uid(uid)
        response = history.get_history_alone(uid, finder, geneset, disp_t, UIProtocolHostName)

        return response


    @application.route('/getKeys', methods=['GET', 'POST'])
    def getKeys():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass

        keys = finder.getAllKeywords()

        return keys


    # %% Refresh Pickle Models

    @application.route('/refreshModel', methods=['GET', 'POST'])
    def refreshModel():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return "Unauthorized Access."
        except Exception as d:
            pass

        import keywordextraction

        return "Model has been updated."

    def get_root_path():
        Domain = request.headers.get("Domain")
        Cust_Id = request.headers.get("WhoIs")
        
        Domain = EnDe.decode(Domain)
        Cust_Id = EnDe.decode(Cust_Id)

        return "Working_dir/" + Domain + "_" + Cust_Id + "/data/"

    def get_corpus_path():
        Lang = request.headers.get("Lang")

        root_path = get_root_path()

        if Lang.lower() == "english":
            return root_path + "Corpus.xlsx"
        else:
            return root_path + "Corpus_" + Lang + ".xlsx"
    
    def get_general_intent_json_path():
        Lang = request.headers.get("Lang")

        root_path = get_root_path()

        if Lang.lower() == "english":
            return root_path + "General_Intent.json"
        else:
            return root_path + "General_Intent_" + Lang + ".xlsx"

    
    def get_intent_json_path():
        Lang = request.headers.get("Lang")

        root_path = get_root_path()

        if Lang.lower() == "english":
            return root_path + "Intent.json"
        else:
            return root_path + "Intent_" + Lang + ".xlsx"

    # %% Main but it should be commented before upload to Git
    # if __name__ == "__main__":
    #     application.run(debug=True)
    return application

application = create_app()
application.run(debug=True)