import os,json
#import pyodbc
from distutils.dir_util import copy_tree
import numpy as np
import pandas as pd
import pwd_gen
import mail
from flask import request,session
import mysql.connector

default_path="./Working_dir"
intent_file="Intent.json"
corpus="Corpus.xlsx"
corpus_ta="Corpus_ta.xlsx"
intent_file_ta="Intent_ta.json"

conn = mysql.connector.connect(host="chatbot-panel.ckjqe647gpza.us-east-1.rds.amazonaws.com",user="admin",passwd="Cbt2020$",port='3306',database="sys")
#conn = mysql.connector.connect(host="localhost",user="root",passwd="Brainy123$",port='3306',database="chatbot_panel")
#conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=103.102.234.23;Database=Chatbot_Panel;uid=CB_Chatbot;pwd=Brainy123$;')
#conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=localhost;Database=Chatbot_Panel;Trusted_Connection=yes;')

#cursor=conn.cursor()

def get_customer_id_verification(cust_id, domain):
    user = pd.read_sql_query("Select * from chatbot_panel Where Customer_ID='"+cust_id+"' and Domain='"+domain+"' and Status='Active';", conn)
    if user.empty:
        return False
    else:
        return True

def check_user(email, password):
    user_check="Select * from users Where Email='"+email+"' and password='"+password+"' and Status='Active';"
    cursor=conn.cursor()
    cursor.execute(user_check)
    value=cursor.fetchall()
    print(user_check)
    if len(value) > 0:
        for val in value:
            isfirstlogin=val[7]
            custid=val[6]
            userid=val[0]
            usertype=val[5]
            if isfirstlogin == "No":
                return "Success",custid,userid,usertype
            else:
                return "FirstLogin",custid,userid,usertype
    else:
        return "","","",""
    cursor.close()
 
def get_domain():
    Domain = pd.read_sql_query("Select distinct Domain from chatbot_panel where Status='Active';", conn)
    Domain = list(filter(lambda x: str(x) != '', Domain['Domain'].tolist()))
    Domain=sorted(Domain)
    return Domain

def get_Customer_ID():
    Customer_ID = pd.read_sql_query("Select CusId from customers where Status='Active';", conn)
    Customer_ID = list(filter(lambda x: str(x) != '', Customer_ID['CusId'].tolist()))
    return Customer_ID

def get_file_path():
    if request.method=="POST":
        domain=request.form['domain_input']
        cust_id=request.form['cust_id_input']
        if cust_id !="--Select Customer ID--":
            full_domain=domain+"_"+cust_id
            cur_path=os.path.join(default_path,full_domain)
            full_path=os.path.join(cur_path,"data")
            return full_path

def get_languages():
    if request.method=="POST":
        domain=request.form['domain_input']
        cust_id=request.form['cust_id_input']
        query = "Select * from chatbot_customer_languages Where Domain='"+domain+"' and Customer_ID='"+cust_id+"' and Status='Active';"
        print(query)
        Language = pd.read_sql_query(query, conn)
        Language = list(filter(lambda x: str(x) != '', Language['Language'].tolist()))
        Language=sorted(Language)
        return Language

def create_folder():
    template_path="./Templates"
    dir_path="./Working_dir"
    if request.method=="POST":
        name=request.form["domain"]
        #welcome=request.form["welcome"]
        customer_id=request.form['cust_id']
        botname=request.form['botname']
        theme_color=request.form['theme_color']
        if customer_id != "" and name!="":
            list=os.listdir(template_path)
            for folder_name in list:
                if name == folder_name:
                    full_name=name+"_"+customer_id
                    path_2=os.path.join(dir_path,full_name)
                    new_path=os.path.join(template_path,folder_name)
                    copy_tree(new_path, path_2)
                    cur=conn.cursor()
                    # cur.execute("insert into chatbot_panel (ChatbotName,WelcomeMessage,Domain,Customer_ID,ColorCode) values (?,?,?,?,?);",(botname,welcome,name,customer_id,theme_color))
                    cur.execute("insert into chatbot_panel (ChatbotName,Domain,Customer_ID,ColorCode) values ('"+botname+"','"+name+"','"+customer_id+"','"+theme_color+"');")
                    conn.commit()
                    cur.close()

def create_customer():
    if request.method=="POST":
        customer_id=request.form['cust_id']
        user_type=request.form['usertype']
        new_mail_id=request.form['new_mail_id']
        password=request.form['createpassword']
        if customer_id != "" and user_type!="" and new_mail_id!="":
            cur=conn.cursor()
            cur.execute("insert into customers (CusId) values (?);",(customer_id))
            cur.execute("insert into users (Email,UserType,Cusid,password,IsFirstLogin) values ('"+new_mail_id+"','"+user_type+"','"+customer_id+"','"+password+"','Yes');")
            conn.commit()
            cur.close()
      

def get_intent_json():
    intent_list=[]
    path=get_file_path()
    if request.method=="POST":
        language=request.form['language_input']
        if language != "--Select Language--":
            if language=="English":
                print(os.path.join(path,intent_file))
                with open (os.path.join(path,intent_file),'r') as f:
                    data=json.load(f)
                    for x in data['data']:
                        intent=x['responses']
                        if len(intent) > 0:
                            intent_list.append(intent)
                    return(intent_list)
            else:
                intent_file_other_language="Intent_"+language+".json"
                with open (os.path.join(path,intent_file_other_language),encoding="utf8") as f:
                    data=json.load(f)
                    for x in data['data']:
                        intent=x['responses']
                        if len(intent) > 0:
                            intent_list.append(intent)
                        intent_list=sorted(intent_list)
                    return(intent_list)

def get_keyword_management_intent():
    path=get_file_path()
    if request.method=="POST":
        intent=request.form['intent_input']
        language=request.form['language_input']
        if language != "--Select Language--":
            if language=="English":
                with open (os.path.join(path,intent_file),'r') as f:
                    data=json.load(f)
                    for x in data['data']:
                        intent_json=x['responses']
                        for words in intent_json:
                            if words==intent:
                                keywords=x['patterns']
                                return keywords
            else:
                intent_file_other_language="Intent_"+language+".json"
                with open (os.path.join(path,intent_file_other_language),encoding="utf8") as f:
                    data=json.load(f)
                    for x in data['data']:
                        intent_json=x['responses']
                        for words in intent_json:
                            if words==intent:
                                keywords=x['patterns']
                                return keywords
        

def add_keyword_json():
    path=get_file_path()
    if request.method=="POST":
        domain=request.form['domain_input']
        cust_id=request.form['cust_id_input']
        intent=request.form['intent_input']
        keyword=request.form['keyword_input']
        language=request.form['language_input']
        if language != "--Select Language--":
            if language=="English":
                if keyword!="":
                    with open (os.path.join(path,intent_file),'r') as f:
                        data=json.load(f)
                        for x in data['data']:
                            pattern=x['patterns']
                            response=x['responses']
                            for words in response :
                                if words==intent:
                                    pattern.append(keyword)
                                    file = open(os.path.join(path,intent_file), "w")
                                    json.dump(data, file,indent=4)
                                
            else:
                if keyword!="":
                    intent_file_other_language="Intent_"+language+".json"
                    with open (os.path.join(path,intent_file_other_language),encoding="utf8") as f:
                        data=json.load(f)
                        for x in data['data']:
                            pattern=x['patterns']
                            response=x['responses']
                            for words in response :
                                if words==intent:
                                    pattern.append(keyword)
                                    file = open(os.path.join(path,intent_file_other_language),"w",encoding="utf8")
                                    json.dump(data, file,ensure_ascii=False,indent=4)
        id=0                            
        user_id=session['userid']
        Description="keyword added using keyword management"
        chatbot_id ="Select ChatBot_ID from chatbot_panel Where Domain='"+domain+"' and Customer_ID='"+cust_id+"' and Status='Active';"
        cur=conn.cursor()
        cur.execute(chatbot_id)
        value=cur.fetchall()
        for val in value:
            id=val[0]
        conn.commit()
        cur.close()

        audit_log(int(id), int(user_id), Description)
    
def get_keyword_management_intent():
    path=get_file_path()
    if request.method=="POST":
        intent=request.form['intent_input']
        language=request.form['language_input']
        if language != "--Select Language--":
            if language=="English":
                with open (os.path.join(path,intent_file),'r') as f:
                    data=json.load(f)
                    for x in data['data']:
                        intent_json=x['responses']
                        for words in intent_json:
                            if words==intent:
                                keywords=x['patterns']
                                return keywords
            else:
                intent_file_other_language="Intent_"+language+".json"
                with open (os.path.join(path,intent_file_other_language),encoding="utf8") as f:
                    data=json.load(f)
                    for x in data['data']:
                        intent_json=x['responses']
                        for words in intent_json:
                            if words==intent:
                                keywords=x['patterns']
                                return keywords
        

def add_keyword_json():
    path=get_file_path()
    if request.method=="POST":
        domain=request.form['domain_input']
        cust_id=request.form['cust_id_input']
        intent=request.form['intent_input']
        keyword=request.form['keyword_input']
        language=request.form['language_input']
        if language != "--Select Language--":
            if language=="English":
                if keyword!="":
                    with open (os.path.join(path,intent_file),'r') as f:
                        data=json.load(f)
                        for x in data['data']:
                            pattern=x['patterns']
                            response=x['responses']
                            for words in response :
                                if words==intent:
                                    pattern.append(keyword)
                                    file = open(os.path.join(path,intent_file), "w")
                                    json.dump(data, file,indent=4)
                                
            else:
                if keyword!="":
                    intent_file_other_language="Intent_"+language+".json"
                    with open (os.path.join(path,intent_file_other_language),encoding="utf8") as f:
                        data=json.load(f)
                        for x in data['data']:
                            pattern=x['patterns']
                            response=x['responses']
                            for words in response :
                                if words==intent:
                                    pattern.append(keyword)
                                    file = open(os.path.join(path,intent_file_other_language),"w",encoding="utf8")
                                    json.dump(data, file,ensure_ascii=False,indent=4)
        id=0
        user_id=session['userid']
        Description="keyword added using keyword management"
        chatbot_id ="Select ChatBot_ID from chatbot_panel Where Domain='"+domain+"' and Customer_ID='"+cust_id+"' and Status='Active';"
        cur=conn.cursor()
        cur.execute(chatbot_id)
        value=cur.fetchall()
        for val in value:
            id=val[0]
        #cur.execute("insert into chatbot_audit (ChatBot_ID,User_ID,Description) values ("+id+","+user_id+",'"+Description+"');")
        conn.commit()
        cur.close()

        
        audit_log(int(id), int(user_id), Description)
    
def delete_corpus_details():
    path=get_file_path()
    if request.method=="POST":
        domain=request.form['domain_input']
        cust_id=request.form['cust_id_input']
        del_word=request.form['delete_input']
        language=request.form['language_input']
        del_word=del_word.replace("|","'")
        if language != "--Select Language--":
            if language=="English":
                df=pd.read_excel(os.path.join(path,corpus),index_col="Sub Functional Area", engine='openpyxl')
                df.drop(del_word,inplace=True)
                df.to_excel(os.path.join(path,corpus), index = False)
                with open (os.path.join(path,intent_file)) as f:
                    data=json.load(f)
                    new_data = [x for x in data['data'] if x['Intent'] != del_word]
                    new_data = {'data':new_data}
                    file=open(os.path.join(path,intent_file),"w")
                    json.dump(new_data,file,indent=4)
            else:
                intent_file_other_language="Intent_"+language+".json"
                corpus_other_language="Corpus_"+language+".xlsx"
                df=pd.read_excel(os.path.join(path,corpus_other_language),index_col="Sub Functional Area", engine='openpyxl')
                df.drop(del_word,inplace=True)
                df.to_excel(os.path.join(path,corpus_other_language), index = False)
                with open (os.path.join(path,intent_file_other_language),encoding="utf8") as f:
                    data=json.load(f)
                    new_data = [x for x in data['data'] if x['Intent'] != del_word]
                    new_data = {'data':new_data}
                    file = open(os.path.join(path,intent_file_other_language), "w",encoding="utf8")
                    json.dump(new_data,file,ensure_ascii=False,indent=4)
        id=0
        Description="corpus details deleted using response Management"
        user_id=session['userid']
        chatbot_id ="Select ChatBot_ID from chatbot_panel Where Domain='"+domain+"' and Customer_ID='"+cust_id+"' and Status='Active';"
        cur=conn.cursor()
        cur.execute(chatbot_id)
        value=cur.fetchall()
        for val in value:
            id=val[0]
        #cur.execute("insert into chatbot_audit (ChatBot_ID,User_ID,Description) values ("+id+","+user_id+",'"+Description+"');")
        conn.commit()
        cur.close()
        audit_log(int(id), int(user_id), Description)

def view_chatbot_table():
    botname_list=[]
    welcome_list=[]
    domain_list=[]
    cus_id_list=[]
    color_list=[]
    status_list=[]
    created_on_list=[]
    Chatbot_ID_list=[]
    cursor=conn.cursor()
    cursor.execute("select ChatbotName,WelcomeMessage,Domain,Customer_ID,ColorCode,Status,Created_on,Chatbot_ID from chatbot_panel order by Created_on desc;") 
    data = cursor.fetchall()
    for x in data:
        botname=x[0]
        welcome=x[1]
        domain=x[2]
        cust_id=x[3]
        color=x[4]
        status=x[5]
        created_on=x[6]
        Chatbot_ID=x[7]
        
        botname_list.append(botname)
        welcome_list.append(welcome)
        domain_list.append(domain)
        cus_id_list.append(cust_id)
        color_list.append(color)
        status_list.append(status)
        Chatbot_ID_list.append(Chatbot_ID)
        created_on_list.append(str(created_on.strftime('%d-%b-%Y')))
    
    cursor.close()
    new_df={
        "botname":botname_list,
        "welcome":welcome_list,
        "domain":domain_list,
        "customer_id":cus_id_list,
        "color":color_list,
        "status":status_list,
        "created_on":created_on_list,
        "chatbot_id":Chatbot_ID_list
    }
    df=pd.DataFrame(new_df)
    
    return df

def view_language_table():
    Id_list=[]
    domain_list=[]
    cus_id_list=[]
    lang_list=[]
    status_list=[]
    created_on_list=[]
    cursor=conn.cursor()
    cursor.execute("select Id,Domain,Customer_ID,Language,Status,Created_on from chatbot_customer_languages order by Domain,Customer_ID;") 
    data = cursor.fetchall()
    for x in data:
        Id=x[0]
        domain=x[1]
        cust_id=x[2]
        lang=x[3]
        status=x[4]
        created_on=x[5]
        
        Id_list.append(Id)
        domain_list.append(domain)
        cus_id_list.append(cust_id)
        lang_list.append(lang)
        status_list.append(status)
        created_on_list.append(str(created_on.strftime('%d-%b-%Y')))
    
    cursor.close()
    new_df={
        "id":Id_list,
        "domain":domain_list,
        "customer_id":cus_id_list,
        "lang":lang_list,
        "status":status_list,
        "created_on":created_on_list
    }
    df=pd.DataFrame(new_df)
    
    return df


def set_new_password(email):
    
    cwd = os.getcwd()
    current_path = cwd

    pwd = pwd_gen.generate_password()
    body = """
    <html>
        <body>
            <p>
                Hi,
            </p>
            <p>
                <b>Your password has been reseted.</b>
            </p>
            <p style="text-align: center">
                <b style="padding: 10px">""" + pwd + """</b>
            </p>
            <p>
                Regards,
                <img src="cid:0">
            </p>
        </body>
    </html>
    """
    mail.SendMail(email, "Password has been reseted for CleverBrain Chatbot Panel", body, [current_path + "\static\dist\img\logotextalt.png"])

    cur=conn.cursor()
    cur.execute("update users set password='"+pwd+"', IsFirstLogin='Yes' where Email='"+email+"';")
    conn.commit()
    cur.close()

    return "Mail has been sent."

def view_customer_table():
    email_list=[]
    usertype_list=[]
    cus_id_list=[]
    status_list=[]
    created_on_list=[]
    contact_list=[]
    cursor=conn.cursor()
    cursor.execute("select C.CusId,U.Email,U.UserType,C.Status,C.Created_on,U.Contact from customers C Join users U On C.CusId = U.CusId order by Created_on desc;") 
    data = cursor.fetchall()
    for x in data:
        cust_id=x[0]
        email=x[1]
        usertype=x[2]
        status=x[3]
        created_on=x[4]
        contact=x[5]
        
        email_list.append(email)
        usertype_list.append(usertype)
        cus_id_list.append(cust_id)
        status_list.append(status)
        contact_list.append(contact)
        created_on_list.append(str(created_on.strftime('%d-%b-%Y')))

    cursor.close()
    new_df={
        "email":email_list,
        "usertype":usertype_list,
        "customer_id":cus_id_list,
        "status":status_list,
        "created_on":created_on_list,
        "contact":contact_list
    }
    df=pd.DataFrame(new_df)
    
    return df


def change_password_in_sql():
    if request.method=="POST":
        password=request.form['password']
        user_id=session['userid']
        cur=conn.cursor()
        cur.execute("update users set password='"+password+"', IsFirstLogin='No' where UserID='"+user_id+"';")
        conn.commit()
        cur.close()

def get_chatbot_name(domain, cust_id):
    chatbotname = ''
    cursor=conn.cursor()
    cursor.execute("Select ChatbotName from chatbot_panel Where Domain='"+domain+"' and Customer_ID='"+cust_id+"';")
    value=cursor.fetchall()
    if len(value) > 0:
        for val in value:
            chatbotname=val[0]
    conn.commit()
    cursor.close()

    return chatbotname

def get_IsActiveCust(domain, cust_id):
    Status = ''
    cursor=conn.cursor()
    cursor.execute("Select Status from chatbot_panel Where Domain='"+domain+"' and Customer_ID='"+cust_id+"';")
    value=cursor.fetchall()
    if len(value) > 0:
        for val in value:
            Status=val[0]
    conn.commit()
    cursor.close()

    return Status

def change_bot_status(botId, status):
    Status = ''
    cursor=conn.cursor()
    cursor.execute("Update chatbot_panel set Status='"+status+"' Where Chatbot_Id='"+botId+"';")
    Status = 'Updated'
    #value=cursor.fetchall()
    # if len(value) > 0:
    #     for val in value:
    #         Status=val[0]
    conn.commit()
    cursor.close()

    return Status

def change_bot_language_status(botId, status):
    Status = ''
    cursor=conn.cursor()
    cursor.execute("Update chatbot_customer_languages set Status='"+status+"' Where Id='"+botId+"';")
    Status = 'Updated'
    #value=cursor.fetchall()
    # if len(value) > 0:
    #     for val in value:
    #         Status=val[0]
    conn.commit()
    cursor.close()

    return Status

def add_new_language(domain,cust_id,lang):
    Status = ''
    cursor=conn.cursor()
    cursor.execute("Insert into chatbot_customer_languages (Domain,Customer_ID,Language) values ('"+domain+"','"+cust_id+"','"+lang+"');")
    Status = 'Updated'
    #value=cursor.fetchall()
    # if len(value) > 0:
    #     for val in value:
    #         Status=val[0]
    conn.commit()
    cursor.close()

    return Status

def add_corpus_details():
    path=get_file_path()
    if request.method=="POST":
        domain=request.form['domain_input']
        other=request.form['other']
        cust_id=request.form['cust_id_input']
        intent=request.form['intent_input']
        response=request.form['response_input']
        bullet=request.form['bullets_input']
        visit_page=request.form['visit_page_input']
        image_url=request.form['image_url']
        language=request.form['language_input']
        if language != "--Select Language--":
            if (intent or response or bullet or visit_page or other) !="":
                if language=="English":
                    df=pd.read_excel(os.path.join(path,corpus), engine='openpyxl')
                    new_data={
                        "Functional Area":other,
                        "Recommend Intent":"",
                        "Sub Functional Area":intent,
                        "Keyword": "",
                        "Question": "",
                        "Response":response,
                        "Bullets":bullet,
                        "Video URL": "",
                        "Hyperlink Text": "",
                        "Hyperlink URL": "",
                        "Image URL": image_url,
                        "Visit Page":visit_page,
                        "Reference URL":""
                    }
                    new=df.append(new_data, ignore_index=True)
                    new.to_excel(os.path.join(path,corpus), index = False)
                    with open (os.path.join(path,intent_file),'r') as f:
                        det = f.readlines()
                        if len(det) == 0:
                            new_intent={
                                "data": [
                                    {
                                        "Intent":"",
                                        "patterns":[],
                                        "responses":[intent]
                                    }
                                ]
                            }
                            
                            with open (os.path.join(path,intent_file),'w') as fl:
                            #file = open(os.path.join(path,intent_file), "w")
                                json.dump(new_intent, fl)
                        else:
                            with open (os.path.join(path,intent_file),'r') as f:
                                data=json.load(f)
                                new_intent={
                                    "Intent":"",
                                    "patterns":[],
                                    "responses":[intent]
                                    }
                                data['data'].append(new_intent)
                                with open (os.path.join(path,intent_file),'w') as fl:
                                #file = open(os.path.join(path,intent_file), "w")
                                    json.dump(data, fl)
                else:
                    intent_file_other_language="Intent_"+language+".json"
                    corpus_other_language="Corpus_"+language+".xlsx"
                    df=pd.read_excel(os.path.join(path,corpus_other_language), engine='openpyxl')
                    new_data={
                        "Functional Area":other,
                        "Recommend Intent":"",
                        "Sub Functional Area":intent,
                        "Keyword": "",
                        "Question": "",
                        "Response":response,
                        "Bullets":bullet,
                        "Video URL": "",
                        "Hyperlink Text": "",
                        "Hyperlink URL": "",
                        "Image URL": image_url,
                        "Visit Page":visit_page,
                        "Reference URL":""
                        }
                    new=df.append(new_data, ignore_index=True)
                    new.to_excel(os.path.join(path,corpus_other_language), index = False)

                    with open (os.path.join(path,intent_file_other_language),'r') as f:
                        det = f.readlines()
                        if len(det) == 0:
                            new_intent={
                                "data": [
                                    {
                                        "Intent":"",
                                        "patterns":[],
                                        "responses":[intent]
                                    }
                                ]
                            }
                            
                            with open (os.path.join(path,intent_file_other_language),'w') as fl:
                            #file = open(os.path.join(path,intent_file_other_language), "w")
                                json.dump(new_intent, fl)
                        else:
                            with open (os.path.join(path,intent_file_other_language),'r') as f:
                                data=json.load(f)
                                new_intent={
                                    "Intent":"",
                                    "patterns":[],
                                    "responses":[intent]
                                    }
                                data['data'].append(new_intent)
                                with open (os.path.join(path,intent_file_other_language),'w') as fl:
                                #file = open(os.path.join(path,intent_file_other_language), "w")
                                    json.dump(data, fl)


                    # with open (os.path.join(path,intent_file_other_language),encoding="utf8") as f:
                    #     data=json.load(f)
                    #     new_intent={
                    #         "Intent":"",
                    #         "patterns":[],
                    #         "responses":[intent]
                    #         }
                    #     data['data'].append(new_intent)
                    #     with open (os.path.join(path,intent_file_other_language),'w',encoding="utf8") as fl:
                    #     #file = open(os.path.join(path,intent_file_other_language), "w",encoding="utf8")
                    #         json.dump(data,fl,ensure_ascii=False)
        id=0            
        Description="corpus details added using response Management"
        user_id=session['userid']
        chatbot_id ="Select ChatBot_ID from chatbot_panel Where Domain='"+domain+"' and Customer_ID='"+cust_id+"' and Status='Active';"
        cur=conn.cursor()
        cur.execute(chatbot_id)
        value=cur.fetchall()
        for val in value:
            id=val[0]
        conn.commit()
        cur.close()

        audit_log(int(id), int(user_id), Description)


def get_welcome_message(domain, cust_id):
    welcome_message = ''
    cursor=conn.cursor()
    cursor.execute("Select WelcomeMessage from chatbot_panel Where Domain='"+domain+"' and Customer_ID='"+cust_id+"' and Status='Active';")
    value=cursor.fetchall()
    if len(value) > 0:
        for val in value:
            welcome_message=val[0]
    conn.commit()
    cursor.close()

    return welcome_message


def get_chatbot_theme(domain, cust_id):
    color_code = ''
    cursor=conn.cursor()
    cursor.execute("Select ColorCode from chatbot_panel Where Domain='"+domain+"' and Customer_ID='"+cust_id+"' and Status='Active';")
    value=cursor.fetchall()
    if len(value) > 0:
        for val in value:
            color_code=val[0]
    conn.commit()
    cursor.close()

    return color_code


def get_response_management_table():
    path=get_file_path()
    if request.method=="POST":
        language=request.form['language_input']
        if language != "--Select Language--":
            if language=="English":         
                df=pd.read_excel(os.path.join(path,corpus), engine='openpyxl')
                df=df.replace(np.nan,"")
                corpus_other=df['Functional Area'].tolist()
                corpus_intent=df['Sub Functional Area'].tolist()
                corpus_response=df['Response'].tolist()
                corpus_bullets=df['Bullets'].tolist()
                corpus_visit_page=df['Visit Page'].tolist()
                image_url=df['Image URL'].tolist()
                new_df={
                    "other":corpus_other,
                    "intent":corpus_intent,
                    "response":corpus_response,
                    "bullets":corpus_bullets,
                    "visit_page":corpus_visit_page,
                    "image_url":image_url
                }
                input_df=pd.DataFrame(new_df)
                
                return input_df
            else:
                corpus_other_language="Corpus_"+language+".xlsx"
                df=pd.read_excel(os.path.join(path,corpus_other_language), engine='openpyxl')
                df=df.replace(np.nan,"")
                corpus_other=df['Functional Area'].tolist()
                corpus_intent=df['Sub Functional Area'].tolist()
                corpus_response=df['Response'].tolist()
                corpus_bullets=df['Bullets'].tolist()
                corpus_visit_page=df['Visit Page'].tolist()
                image_url=df['Image URL'].tolist()
                new_df={
                    "other":corpus_other,
                    "intent":corpus_intent,
                    "response":corpus_response,
                    "bullets":corpus_bullets,
                    "visit_page":corpus_visit_page,
                    "image_url":image_url
                }
                input_df=pd.DataFrame(new_df)
                
                return input_df


def edit_new_keyword_management():
    path=get_file_path()
    if request.method=="POST":
        new_keyword=request.form['new_keyword']
        keyword=request.form['edit_keyword']
        intent_input=request.form['intent_input']
        language=request.form['language_input']
        if language != "--Select Language--":
            if language == 'English':
                with open (os.path.join(path,intent_file)) as f:
                    data=json.load(f)
                    for x in data['data']:
                        intent=x['responses']
                        patterns=x['patterns']
                        for words in intent :
                            if words == intent_input:
                                patterns.remove(keyword)
                                patterns.append(new_keyword)
                                file = open(os.path.join(path,intent_file), "w")
                                json.dump(data, file,indent=4)
            else:
                intent_file_other_language="Intent_"+language+".json"
                with open (os.path.join(path,intent_file_other_language)) as f:
                    data=json.load(f)
                    for x in data['data']:
                        intent=x['responses']
                        patterns=x['patterns']
                        for words in intent :
                            if words == intent_input:
                                patterns.remove(keyword)
                                patterns.append(new_keyword)
                                file = open(os.path.join(path,intent_file_other_language), "w",encoding="utf8")
                                json.dump(data, file,ensure_ascii=False,indent=4)


def edit_manage_customer():
    if request.method=="POST":
        cust_id=request.form['cust_id']
        email=request.form['mail_id']
        contact=request.form['contact']
        cur=conn.cursor()
        cur.execute("update users set Email='"+email+"',Contact='"+contact+"' where CusId='"+cust_id+"';")
        conn.commit()
        cur.close()


def edit_manage_chatbot():
    if request.method=="POST":
        domain=request.form['domain']
        welcome=request.form['welcome']
        color=request.form['color']
        botname=request.form['botname']
        cust_id=request.form['cust_id']
        cur=conn.cursor()
        cur.execute("update chatbot_panel set WelcomeMessage='"+welcome+"' ,ChatbotName='"+botname+"' ,ColorCode='"+color+"' where Domain='"+domain+"' and  Customer_ID='"+cust_id+"';")
        conn.commit()
        cur.close()


def edit_response_management():
    path=get_file_path()
    if request.method=="POST":
        other=request.form['other']
        intent=request.form['intent_input']
        response=request.form['response_input']
        bullet=request.form['bullets_input']
        visit_page=request.form['visit_page_input']
        image_url=request.form['image_url']
        language=request.form['language_input']
        if language != "--Select Language--":
            if (intent and (response or bullet or visit_page)) !="":
                if language == 'English':
                    df=pd.read_excel(os.path.join(path,corpus), engine='openpyxl')
                    for index in df.index:
                        if df.loc[index,'Sub Functional Area']==intent:
                            df.loc[index,'Functional Area'] = other
                            df.loc[index,'Response'] = response
                            df.loc[index,'Bullets'] = bullet
                            df.loc[index,'Visit Page'] = visit_page
                            df.loc[index,'Image URL'] = image_url
                            df.to_excel(os.path.join(path,corpus), index = False)                       
                else:
                    corpus_other_language="Corpus_"+language+".xlsx"
                    df=pd.read_excel(os.path.join(path,corpus_other_language), engine='openpyxl')
                    for index in df.index:
                        if df.loc[index,'Sub Functional Area']==intent:
                            df.loc[index,'Functional Area'] = other
                            df.loc[index,'Response'] = response
                            df.loc[index,'Bullets'] = bullet
                            df.loc[index,'Visit Page'] = visit_page
                            df.loc[index,'Image URL'] = image_url
                            df.to_excel(os.path.join(path,corpus_other_language), index = False)
                            

def get_languages_by_details(domain, cust_id):
    print(domain, cust_id)
    languages = []
    cursor=conn.cursor()
    cursor.execute("Select Language from chatbot_customer_languages Where Domain='"+domain+"' and Customer_ID='"+cust_id+"' and Status='Active';")
    value=cursor.fetchall()
    if len(value) > 0:
        for val in value:
            languages.append(val[0])
    conn.commit()
    cursor.close()

    return languages
    
def audit_log(id, user_id, Description):

    query = "insert into chatbot_audit (ChatBot_ID,User_ID,Description) values ("+str(id)+","+str(user_id)+",'"+Description+"');"
    
    print(query)
    cur=conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()

def send_contact(Domain, CustId, contact_name, contact_email, contact_number):
    cus_email = ''
    bot_name = ''
    email_cnt = ''
    contact_cnt = ''
    cwd = os.getcwd()
    current_path = cwd

    user_check="Select * from users Where CusId='"+CustId+"' and Status='Active';"
    cursor=conn.cursor()
    cursor.execute(user_check)
    value=cursor.fetchall()
    if len(value) > 0:
        for val in value:
            cus_email=val[1]

    user_check="Select * from chatbot_panel Where Customer_ID='"+CustId+"' and Domain='"+Domain+"' and Status='Active';"
    cursor.execute(user_check)
    value=cursor.fetchall()
    if len(value) > 0:
        for val in value:
            bot_name=val[6]
    
    if contact_email != "":
        email_cnt = """<tr>
            <td>
            <b>Email:</b>
            </td>
            <td>
            """ + contact_email + """
            </td>
        </tr>"""

    if contact_number != "":
        contact_cnt = """<tr>
            <td>
            <b>Contact # :</b>
            </td>
            <td>
            """ + contact_number + """
            </td>
        </tr>"""

    body = """
    <html>
        <body>
            <p>
                Hi,
            </p>
            <p>
                <b>Please find below user's contact details.</b>
            </p>
            <p style="text-align: center">
                <table>
                    <tr>
                        <td>
                        <b>Name:</b>
                        </td>
                        <td>"""+contact_name+"""
                        </td>
                    </tr>
                    """+ email_cnt + contact_cnt + """
                </table>
            </p>
            <p>
                Regards,<br>
                Support Team<br>
                Clever Brain Technologies Private Limited<br>
                <a href="mailto:support@cleverbrain.in">support@cleverbrain.in</a>
            </p>
        </body>
    </html>"""

    cursor.close()

    mail.SendMail(cus_email, ("User Contact Details from " + bot_name), body, [current_path + "\static\dist\img\logotextalt.png"])

    return "Sent"
