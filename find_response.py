import pandas as pd
import json
import load_corpus
import re
import db_proxy

class response_finder:

    cnx = ''
    cursor = ''
    # welcome_message = ''
    # website_data = ''
    # master_intent_entity = ''
    logger = ''
    invalid_user_chat = ['who', 'where']

    def __init__(self, _logger):
        self.logger = _logger
        # self.welcome_message = load_corpus.get_welcome_message()

        # self.website_data, self.master_intent_entity = load_corpus.get_data()


    def get_welcome_message(self, domain, cust_id):
        
        res_json = {}

        welcome_message = db_proxy.get_welcome_message(domain, cust_id)
        
        try:            
            res_json = {
                "output_text": welcome_message,
                "bullet": '',
                "video_url": '',
                "hyperlink_text": '',
                "hyperlink_url": '',
                "image_url": '',
                "display_type": 'Welcome',
                "recommend_intent": '',
                "visit_page": ''
            }

        except Exception as e:
            print(str(e))
            self.logger.write_exception(str(e), 'get_welcome_message')

        return json.dumps(res_json)

    def remove_stopwords(self, review_words):
        with open('stopwords.txt') as stopfile:
            stopwords_data = stopfile.read()
            stopwords = stopwords_data.splitlines()
            review_words = review_words.split()

            resultwords  = [word for word in review_words if word.lower() not in stopwords]
            
            return resultwords

    def find_response(self, chat_message, corpus_path, general_intent_json_path, intent_json_path, chatbotname, isRecommend=False):
        res_json = {}
        try:
            chat = ''
            intent = []
            import predict
            if isRecommend == False:
                # isInvalid = self.validateUserinput(chat_message)
                
                # if isInvalid == False:
                intent = predict.predict(chat_message, intent_json_path)
                
                if len(intent) > 0:                
                    if isRecommend == True:
                        try:
                            intent.remove(chat_message)
                        except:
                            pass
                    chat = intent[0]
            else:
                chat = chat_message
            # chats = self.remove_stopwords(chat_message)
            # master = self.master_intent_entity
            website_data, master_intent_entity = load_corpus.get_data(corpus_path)
            corpus = website_data

            if chat != '':
                corpus = corpus.loc[(corpus['Sub Functional Area'] == str(chat))]
                
                if not corpus.empty:
                    output_text = '' if str(corpus['Response'].iloc[0]) == 'nan' else corpus['Response'].iloc[0]
                    bullet = '' if str(corpus['Bullets'].iloc[0]) == 'nan' else corpus['Bullets'].iloc[0]
                    video_url = '' if str(corpus['Video URL'].iloc[0]) == 'nan' else corpus['Video URL'].iloc[0]
                    hyperlink_text = '' if str(corpus['Hyperlink Text'].iloc[0]) == 'nan' else corpus['Hyperlink Text'].iloc[0]
                    hyperlink = '' if str(corpus['Hyperlink URL'].iloc[0]) == 'nan' else corpus['Hyperlink URL'].iloc[0]
                    image_url = '' if str(corpus['Image URL'].iloc[0]) == 'nan' else corpus['Image URL'].iloc[0]
                    #recommend_text = '' if str(corpus['Recommend Text'].iloc[0]) == 'nan' else corpus['Recommend Text'].iloc[0]
                    recommend_intent = '' if str(corpus['Recommend Intent'].iloc[0]) == 'nan' else corpus['Recommend Intent'].iloc[0]
                    visit_page = '' if str(corpus['Visit Page'].iloc[0]) == 'nan' else corpus['Visit Page'].iloc[0]

                    res_json = {
                        "output_text": output_text,
                        "bullet": bullet,
                        "video_url": video_url,
                        "hyperlink_text": hyperlink_text,
                        "hyperlink_url": hyperlink,
                        "image_url": image_url,
                        #"recommend_text": recommend_text,
                        "recommend_intent": recommend_intent,
                        "visit_page": visit_page,
                        "is_general": False
                    }
                else:
                    cnt = 1
                    while True:
                        try:
                            if len(intent) == 0:
                                break
                            chat = intent[cnt]
                            chat = chat

                            corpus = website_data
                            corpus = corpus.loc[corpus['Sub Functional Area'].str.lower() == str(chat).lower()]
                            
                            if not corpus.empty:
                                
                                output_text = '' if str(corpus['Response'].iloc[0]) == 'nan' else corpus['Response'].iloc[0]
                                bullet = '' if str(corpus['Bullets'].iloc[0]) == 'nan' else corpus['Bullets'].iloc[0]
                                video_url = '' if str(corpus['Video URL'].iloc[0]) == 'nan' else corpus['Video URL'].iloc[0]
                                hyperlink_text = '' if str(corpus['Hyperlink Text'].iloc[0]) == 'nan' else corpus['Hyperlink Text'].iloc[0]
                                hyperlink = '' if str(corpus['Hyperlink URL'].iloc[0]) == 'nan' else corpus['Hyperlink URL'].iloc[0]
                                image_url = '' if str(corpus['Image URL'].iloc[0]) == 'nan' else corpus['Image URL'].iloc[0]
                                #recommend_text = '' if str(corpus['Recommend Text'].iloc[0]) == 'nan' else corpus['Recommend Text'].iloc[0]
                                recommend_intent = '' if str(corpus['Recommend Intent'].iloc[0]) == 'nan' else corpus['Recommend Intent'].iloc[0]
                                visit_page = '' if str(corpus['Visit Page'].iloc[0]) == 'nan' else corpus['Visit Page'].iloc[0]

                                res_json = {
                                    "output_text": output_text,
                                    "bullet": bullet,
                                    "video_url": video_url,
                                    "hyperlink_text": hyperlink_text,
                                    "hyperlink_url": hyperlink,
                                    "image_url": image_url,
                                    #"recommend_text": recommend_text,
                                    "recommend_intent": recommend_intent,
                                    "visit_page": visit_page,
                                    "is_general": False
                                }
                                break

                            cnt = cnt + 1
                        except Exception as e:
                            break
                            pass
                        
            if not bool(res_json):
                response = predict.getGeneralResponse(chat_message, general_intent_json_path)
                response = response.replace("[CHATBOTNAME]", chatbotname)
                # print('response', response)
                if str(response).strip() == '':
                    response = "I am sorry, can you rephrase your question?"
                res_json = {
                    "output_text": response,
                    "bullet": '',
                    "video_url": '',
                    "hyperlink_text": '',
                    "hyperlink_url": '',
                    "image_url": '',
                    #"recommend_text": recommend_text,
                    "recommend_intent": '',
                    "visit_page": '',
                    "is_general": True
                }

        except Exception as e:
            print(str(e))
            self.logger.write_exception(str(e), 'find_response')
            pass

        return json.dumps(res_json)

    def getAllKeywords(self):
        with open("./data/All_Keywords.json") as json_data:
            multi_keywords = json.load(json_data)
        
        all_keywords = []

        for muliti in multi_keywords['keywords']:
            all_keywords.append(muliti)

        return json.dumps(all_keywords)

    def getAllKeywordsForAutocomplete(self, intent_json_path):
        all_keywords = []

        with open(intent_json_path) as json_data:
            all_intents = json.load(json_data)

        for intent in all_intents['data']:
            for pattern in intent['patterns']:
                all_keywords.append(pattern)

        return all_keywords                    

    def validateUserinput(self, chat_message):
        with open("./data/All_Keywords.json") as json_data:
            multi_keywords = json.load(json_data)
                
        lots_of_stopwords = []
        stopword_file = open("./data/long_stopwords.txt", "r")
        isKeywordAvl = False
        
        with open("./data/intent.json") as json_data:
            all_intents = json.load(json_data)
                
        for line in stopword_file.readlines():
            lots_of_stopwords.append(str(line.strip()))

        all_keywords_temp = []

        for muliti in multi_keywords['keywords']:
            all_keywords_temp.append(muliti)

        isBreak = False

        for intent in all_intents['data']:
            
            if isBreak == True:
                break

            for pattern in intent['patterns']:
                
                if isBreak == True:
                    break
                words = []
                pattern = re.sub(r'[?|$|.|_|(|)|,|&|!]',r'',pattern)
                w = pattern.split(' ')
                #w = [(_w.lower()) for _w in w if _w.lower() not in lots_of_stopwords]
                for word in w:
                    wrd = ''
                    if word.lower() not in lots_of_stopwords:
                        if word.endswith('s'):
                            wrd = word[:-1]
                            if word not in all_keywords_temp and wrd not in all_keywords_temp:
                                cont = any(item.lower() in self.invalid_user_chat for item in chat_message.split(' '))
                                
                                if 'acadia' in chat_message.lower() and ('who' in chat_message.lower() or 'where' in chat_message.lower()):
                                    isKeywordAvl = False
                                    isBreak = True
                                    break
                                if word.lower() in chat_message.lower() and cont == True:
                                    isKeywordAvl = True
                                    isBreak = True
                                    break
                                if 'how acadia' in chat_message.lower() and 'how is acadia' in chat_message.lower():
                                    isKeywordAvl = True
                                    isBreak = True
                                    break
                                all_keywords_temp.append(word)
                        else:
                            wrd = word + 's'
                            if word not in all_keywords_temp and wrd not in all_keywords_temp:
                                if word != '':
                                    cont = any(item.lower() in self.invalid_user_chat for item in chat_message.split(' '))
                                    
                                    if 'acadia' in chat_message.lower() and ('who' in chat_message.lower() or 'where' in chat_message.lower()):
                                        isKeywordAvl = False
                                        isBreak = True
                                        break
                                    if word.lower() in chat_message.lower() and cont == True:
                                        isKeywordAvl = True
                                        isBreak = True
                                        break
                                    if 'how acadia' in chat_message.lower() and 'how is acadia' in chat_message.lower():
                                        isKeywordAvl = True
                                        isBreak = True
                                        break
                                    all_keywords_temp.append(word)
        
        return isKeywordAvl