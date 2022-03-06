import find_response
import response_generator
import get_history
from lazywritter import log_writter
import datetime
import config
import EnDe
from flask_cors import CORS, cross_origin
import auth
import json
from flask import Flask, request,render_template,session
import db_proxy
import json
import EnDe


def create_app():
# %% Declaration(s)
    cfg = config.Config()

    application = Flask(__name__, template_folder='template')
    application.secret_key = 'POC1'
    CORS(application)

    logger = log_writter()

    geneset = response_generator.response_generator(logger)

    finder = find_response.response_finder(logger)

    unauthorized_msg = 'Unauthorized Access.'

    chat_msg_time_format = '%d/%m/%y %H:%M:%S'

    login_users = []
    cus_id=[]

    # %% Common
    # app = Flask(__name__,template_folder='template')
    # app.secret_key = 'POC1'

    @application.route('/home')
    def home():
        try:
            if session["email"] == "":
                return render_template('login.html')
        except:
            return render_template('login.html')

        if session['UserType']=="Admin":
            return render_template('Keyword-management-admin.html')

        elif session['UserType']=="User":
            return render_template('Keyword-management-user.html')

        else:    
            return render_template('manage_chatbot.html')


    @application.route('/cblang')
    def cblang():
        try:
            if session["email"] == "":
                return render_template('login.html')
        except:
            return render_template('login.html')

        if session['UserType']=="Admin":
            return render_template('Keyword-management-admin.html')

        elif session['UserType']=="User":
            return render_template('Keyword-management-user.html')

        else:    
            return render_template('manage_language.html')

    @application.route('/manage_customer')
    def manage_customer():
        try:
            if session["email"] == "":
                return render_template('login.html')
        except:
            return render_template('login.html')

        return render_template('manage_customer.html')

    @application.route('/')
    def login():
        return render_template('login.html')

    @application.route('/chatbot_generator')
    def chatbot_generator():
        try:
            if session["email"] == "":
                return render_template('login.html')
        except:
            return render_template('login.html')

        return render_template('chatbot_generator.html')

    @application.route('/reset_password')
    def forgot_password():
        return render_template('reset_password.html')
    
    @application.route("/keyword_management",methods=['GET','POST'])
    def keyword_management():
        try:
            if session["email"] == "":
                return render_template('login.html')
        except:
            return render_template('login.html')
        
        if session['UserType']=="User":
            return render_template("Keyword-management-user.html")

        elif session['UserType']=="Admin":
            return render_template("Keyword-management-admin.html")

        else:
            return render_template("Keyword-management.html")

    @application.route("/response_management",methods=['GET','POST'])
    def response_management():
        try:
            if session["email"] == "":
                return render_template('login.html')
        except:
            return render_template('login.html')

        if session['UserType']=="User":
            return render_template("Response-management-user.html")
        
        elif session['UserType']=="Admin":
            return render_template("Response-management-Admin.html")

        else:
            return render_template("Response-management.html")

    @application.route('/get_domain', methods=['GET', 'POST'])
    def get_domain():
        domain = db_proxy.get_domain()
        return json.dumps(domain)

    @application.route('/get_intent_json', methods=['GET', 'POST'])
    def get_intent_json():
        intent=db_proxy.get_intent_json()
        return json.dumps(intent)

    @application.route('/get_response_management_table', methods=['GET', 'POST'])
    def get_response_management_table():
        intent=db_proxy.get_response_management_table()
        return intent.to_json(orient="index")

    @application.route('/get_keyword_management_intent', methods=['GET', 'POST'])
    def get_keyword_management_intent():
        intent=db_proxy.get_keyword_management_intent()
        return json.dumps(intent)

    @application.route('/edit_keyword_management', methods=['GET', 'POST'])
    def edit_keyword_management():
        intent=db_proxy.edit_keyword_management()
        return json.dumps(intent)

    @application.route('/edit_response_management', methods=['GET', 'POST'])
    def edit_response_management():
        intent=db_proxy.edit_response_management()
        return json.dumps(intent)

    @application.route('/edit_manage_customer', methods=['GET', 'POST'])
    def edit_manage_customer():
        intent=db_proxy.edit_manage_customer()
        return json.dumps(intent)

    @application.route('/edit_manage_chatbot', methods=['GET', 'POST'])
    def edit_manage_chatbot():
        intent=db_proxy.edit_manage_chatbot()
        return json.dumps(intent)

    @application.route('/edit_new_keyword_management', methods=['GET', 'POST'])
    def edit_new_keyword_management():
        intent=db_proxy.edit_new_keyword_management()
        return json.dumps(intent)

    @application.route('/generate_link', methods=['GET', 'POST'])
    def generate_link():
        link = ""

        if request.method=="POST":
            domain=request.form['domain_input']
            cust_id=request.form['cust_id_input']

            domain = EnDe.encode(domain).decode()
            cust_id = EnDe.encode(cust_id).decode()

            link = """
            <script type="text/javascript" 
            src="cb_chatbot.js?cnt=d587e61f987001x0e"
            data-domain=\""""+domain+"""\"
            data-cusid=\""""+cust_id+"""\" ></script>
            """

        return json.dumps(link)

    @application.route('/get_languages', methods=['GET', 'POST'])
    def get_languages():
        intent=db_proxy.get_languages()
        return json.dumps(intent)


    @application.route('/add_keyword_json', methods=['GET', 'POST'])
    def add_keyword_json():
        intent=db_proxy.add_keyword_json()
        return json.dumps(intent)

    @application.route('/delete_keyword_json', methods=['GET', 'POST'])
    def delete_keyword_json():
        intent=db_proxy.delete_keyword_json()
        return json.dumps(intent)

    @application.route('/get_Customer_id', methods=['GET', 'POST'])
    def get_Customer_id():
        cust_id = db_proxy.get_Customer_ID()
        return json.dumps(cust_id)


    @application.route('/add_corpus_details', methods=['GET', 'POST'])
    def add_corpus_details():
        intent=db_proxy.add_corpus_details()
        return json.dumps(intent)

    @application.route('/delete_corpus_details', methods=['GET', 'POST'])
    def delete_corpus_details():
        intent=db_proxy.delete_corpus_details()
        return json.dumps(intent)

    @application.route('/change_password', methods=['GET', 'POST'])
    def change_password():
        return render_template("change_password.html")

    @application.route('/change_password_in_sql', methods=['GET', 'POST'])
    def change_password_in_sql():
        intent=db_proxy.change_password_in_sql()
        return json.dumps(intent)


    @application.route('/logon', methods=['GET', 'POST'])
    def logon():
        res = False
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            res,cusid,userid,usertype= db_proxy.check_user(email, password)
            session['userid']=userid
            if res == "Success":
                session['custid']=cusid
                session['UserType']=usertype
                login_users.append(email)
                session['email'] = email
            
        return res
        

    @application.route('/get_customer_id_user', methods=['GET', 'POST'])
    def get_customer_id_user():
        lst=[]
        custid=session['custid']
        lst.append(custid)
        return json.dumps(lst)
        
    # @application.route('/get_all_domains', methods=['GET', 'POST'])
    # def get_all_domains():
    #     lst=[]
    #     custid=session['custid']
    #     lst.append(custid)
    #     return json.dumps(lst)

    @application.route('/get_customer_id_verification',methods=["GET","POST"])
    def get_customer_id_verification():
        res = False
        if request.method == 'POST':
            cust_id=request.form['cust_id']
            domain=request.form['domain']
            res = db_proxy.get_customer_id_verification(cust_id, domain)
            if res == True:
                cus_id.append(cust_id)

        return json.dumps(res)

    @application.route('/create_folder', methods=['GET', 'POST'])
    def create_folder():
        intent=db_proxy.create_folder()
        return json.dumps(intent)

    @application.route('/create_customer', methods=['GET', 'POST'])
    def create_customer():
        intent=db_proxy.create_customer()
        return json.dumps(intent)

    @application.route("/view_chatbot_table" ,methods=["GET","POST"])
    def view_chatbot_table(): 
        intent=db_proxy.view_chatbot_table()
        return intent.to_json(orient="index")
        
    @application.route("/view_language_table" ,methods=["GET","POST"])
    def view_language_table(): 
        intent=db_proxy.view_language_table()
        return intent.to_json(orient="index")
        
    @application.route("/view_customer_table" ,methods=["GET","POST"])
    def view_customer_table(): 
        intent=db_proxy.view_customer_table()
        return intent.to_json(orient="index")

    @application.route("/set_new_password" ,methods=["GET","POST"])
    def set_new_password():
        if request.method == 'POST':
            email=request.form['email']
            intent=db_proxy.set_new_password(email)
            return intent

    @application.route('/logout', methods=['GET', 'POST'])
    def logout():
        status = ""

        try:
            session["email"] = ''
            status = "updated"
        except:
            pass

        return status

    @application.route('/change_bot_status', methods=['GET', 'POST'])
    @cross_origin()
    def change_bot_status():
        res_status = ''
        if request.method == 'POST':
            botId=request.form['botId']
            status=request.form['status']
            if status == "true":
                status = "Active"
            else:
                status = "InActive"
            res_status = db_proxy.change_bot_status(botId, status)

        return res_status

    @application.route('/change_bot_language_status', methods=['GET', 'POST'])
    @cross_origin()
    def change_bot_language_status():
        res_status = ''
        if request.method == 'POST':
            botId=request.form['botId']
            status=request.form['status']
            if status == "true":
                status = "Active"
            else:
                status = "InActive"
            res_status = db_proxy.change_bot_language_status(botId, status)

        return res_status

    @application.route('/add_new_language', methods=['GET', 'POST'])
    @cross_origin()
    def add_new_language():
        res_status = ''
        if request.method == 'POST':
            domain=request.form['domain']
            cust_id=request.form['cust_id']
            lang=request.form['lang']

            res_status = db_proxy.add_new_language(domain,cust_id,lang)

        return res_status
    #%% Chatbot Web Methods %%

    @application.route('/getConfigs', methods=['GET', 'POST'])
    @cross_origin()
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
    @cross_origin()
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

        #history = get_history.History()
        #feedback = request.headers.get('feedback')
        disp_t = request.form.get('disp_t')
        # UIProtocolHostName = request.form.get('UIProtocolHostName')
        # uid = request.args['uid']

        # user_chat = "<p>" + feedback + "</p>"
        
        # cur_response = ''
        # if feedback.lower() == "yes":
        #     cur_response = cur_response + '<p>How may I help you?</p>'
        # else:
        #     cur_response = cur_response + "<p>Thank you! I'm so glad I could help.</p>"

        # history.check_update_history(uid, user_chat, cur_response, disp_t)

        # IsLast = ""
        # if "I'm so glad I could help" in cur_response:
        #     IsLast = "true"

        # response = {
        #     "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t, "is_last": IsLast}],
        #     "uid": uid
        # }

        response = geneset.generate_feedback(disp_t)

        return response
        
    @application.route('/timeouthit', methods=['GET', 'POST'])
    @cross_origin()
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
        
        chatbotname = get_chatbot_name()
        cur_response = ''
        cur_response = cur_response + "<p>Hi, I am "+chatbotname+". How can I help you today?</p>"
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
    @cross_origin()
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

        #history = get_history.History()
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

    @application.route('/chat', methods=['GET', 'POST'])
    @cross_origin()
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
            user_message_formatted = request.form.get('user_message_formatted')
            
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
            chatbotname = get_chatbot_name()
            Lang = request.headers.get("Lang")
            print(user_chat)
            
            res_json = finder.find_response(user_chat, corpus_path, general_intent_json_path, intent_json_path, chatbotname, Lang, is_recommend)
            
            cur_response = geneset.generate_response(res_json, UIProtocolHostName, Lang)
            
            uid = history.check_generate_uid(uid)
            
            if 'cb_contact_name' not in cur_response:
                history.check_update_history(uid, user_message_formatted, cur_response, disp_t)
            
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

    @application.route('/chathistory', methods=['GET', 'POST'])
    @cross_origin()
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
        Domain = request.headers.get("Domain")
        Cust_Id = request.headers.get("WhoIs")
        
        Domain = EnDe.decode(Domain)
        Cust_Id = EnDe.decode(Cust_Id)

        corpus_path = get_corpus_path()
        Lang = request.headers.get("Lang")

        uid = history.check_generate_uid(uid)
        response = history.get_history_alone(uid, finder, geneset, disp_t, UIProtocolHostName, Domain, Cust_Id, corpus_path, Lang)
        
        return response


    @application.route('/getKeys', methods=['GET', 'POST'])
    @cross_origin()
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
        
        intent_json_path = get_intent_json_path()

        keys = finder.getAllKeywordsForAutocomplete(intent_json_path)

        return json.dumps(keys)


    @application.route('/getBotTheme', methods=['GET', 'POST'])
    @cross_origin()
    def getBotTheme():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass
        
        Domain = request.headers.get("Domain")
        Cust_Id = request.headers.get("WhoIs")
        
        Domain = EnDe.decode(Domain)
        Cust_Id = EnDe.decode(Cust_Id)

        color_code = db_proxy.get_chatbot_theme(Domain, Cust_Id)

        return color_code


    @application.route('/getBotLanguages', methods=['GET', 'POST'])
    @cross_origin()
    def getBotLanguages():
        try:
            auth_creds = request.authorization
            is_authorize = auth.Authorize(
                auth_creds.username, auth_creds.password)
            if is_authorize == False:
                return unauthorized_msg
        except Exception as d:
            return unauthorized_msg
            pass
        
        Domain = request.headers.get("Domain")
        Cust_Id = request.headers.get("WhoIs")
        
        Domain = EnDe.decode(Domain)
        Cust_Id = EnDe.decode(Cust_Id)

        keys = db_proxy.get_languages_by_details(Domain, Cust_Id)

        return json.dumps(keys)


    @application.route('/getChatbotName', methods=['GET', 'POST'])
    @cross_origin()
    def getChatbotName():
        Domain = request.headers.get("Domain")
        Cust_Id = request.headers.get("WhoIs")
        
        Domain = EnDe.decode(Domain)
        Cust_Id = EnDe.decode(Cust_Id)

        chatbotname = db_proxy.get_chatbot_name(Domain, Cust_Id)

        return chatbotname
        

    @application.route('/getIsActiveCust', methods=['GET', 'POST'])
    @cross_origin()
    def getIsActiveCust():
        Domain = request.headers.get("Domain")
        Cust_Id = request.headers.get("WhoIs")
        
        Domain = EnDe.decode(Domain)
        Cust_Id = EnDe.decode(Cust_Id)

        status = db_proxy.get_IsActiveCust(Domain, Cust_Id)

        return status

    @application.route('/SendContactDetails', methods=['GET', 'POST'])
    @cross_origin()
    def SendContactDetails():
        Domain = request.headers.get("Domain")
        Cust_Id = request.headers.get("WhoIs")
        Lang = request.headers.get("Lang")
        contact_name = request.form.get('contact_name')
        contact_email = request.form.get('contact_email')
        contact_number = request.form.get('contact_number')
        disp_t = request.form.get('disp_t')
        uid = request.args['uid']

        Domain = EnDe.decode(Domain)
        Cust_Id = EnDe.decode(Cust_Id)

        res = db_proxy.send_contact(Domain, Cust_Id, contact_name, contact_email, contact_number)
        ctrl = ""

        if Lang == "English":
            ctrl = geneset.generate_plain_text("Thank you for connecting with us. We will get back to you.<br>Is there anything else you are looking for ?", disp_t)
        else:
            ctrl = geneset.generate_plain_text("எங்களுடன் இணைந்ததற்கு நன்றி. நாங்கள் உங்களை தொடர்புகொள்வோம்.<br>வேறு ஏதாவது கேட்க விரும்புகிறீர்களா ?", disp_t)

        response = {
                "chats": [{"message": ctrl, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t, "seperate_response": "", "is_last": "", 'is_general': ""}],
                "uid": uid
            }

        return response
        

    def get_chatbot_name():
        Domain = request.headers.get("Domain")
        Cust_Id = request.headers.get("WhoIs")
        
        Domain = EnDe.decode(Domain)
        Cust_Id = EnDe.decode(Cust_Id)

        chatbotname=db_proxy.get_chatbot_name(Domain, Cust_Id)

        return chatbotname

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
            return root_path + "General_Intent_" + Lang + ".json"
    
    def get_intent_json_path():
        Lang = request.headers.get("Lang")

        root_path = get_root_path()

        if Lang.lower() == "english":
            return root_path + "Intent.json"
        else:
            return root_path + "Intent_" + Lang + ".json"


    # if __name__ == "__main__":
    #     app.run(debug = True,port=2000)
    return application

application = create_app()
application.run(debug=True)
    