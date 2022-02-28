import json

class response_generator:

    logger = ''

    def __init__(self, _logger):
        self.logger = _logger
        pass

    def generate_feedback_response(self):
        response = ''

        try:
            # %% Plain Text Generation
            response = response + 'Thank you for your feedback. Everyday I am learning. I will answer your questions to the best of my ability.'
        except Exception as e:
            print('Error')
            response = "I am sorry, can you rephrase your question?"
            print(str(e))
            self.logger.write_exception(str(e), 'get_welcome_message')

        return response

    def generate_user_response(self, user_data, disp_t):
        return '<div class="wpic-conversation-item alt slide-in-bottom"><div class="wpic-conversation-body">' + \
                        '<div class="wpic-conversation-text user"><p class="chat-text" dir="auto">'+ user_data + \
                        '</p></div><div class="wpic-conversation-footer">' +\
                        '<span class="wpic-conversation-timestamp" data-direction="user" data-timestamp="1645595696">'+disp_t+'</span></div>'+\
                        '</div></div>'
        

    def generate_response(self, json_data, UIProtocolHostName):
        response = ''

        try:
            json_obj = json.loads(json_data)
            
            # %% Plain Text Generation
            if '\n' in json_obj['output_text']:
                txts = json_obj['output_text'].split('\n')

                for txt in txts:
                    response = response + '<p class="chat-text" dir="auto">' + txt + '</p>'
                            
                    #response = response + '<p>' + txt + '</p>'
            else:
                if json_obj['output_text'] != '':
                    response = response + '<p class="chat-text" dir="auto">' + json_obj['output_text'] + '</p>'
                    
                    #response = response + '<p>' + json_obj['output_text'] + '</p>'
            
            if 'Goodbye' in json_obj['output_text'] or 'My pleasure' in json_obj['output_text']:
                response = response + '<div class="chat-individual-feedback"><span>Was this helpful?</span>'
                response = response + \
                    '<button class="chat-individual-feedback-button-no" onclick="feedbackno()">No</button>'
                response = response + \
                    '<button class="chat-individual-feedback-button-yes" onclick="feedbackyes()">Yes</button>'
                response = response + '<div class="chat-float-clear"></div></div>'

            # %% Bullet Generation
            
            if json_obj['bullet'] != '':
                response = response + '<ul>'
                
                if '\n' in json_obj['bullet']:
                    bullets = json_obj['bullet'].split('\n')
                    
                    for bull in bullets:
                        response = response + '<li>' + bull + '</li>'
                else:
                    response = response + '<li>' + json_obj['bullet'] + '</li>'
            
                if '<ul>' in response:
                    response = response + '</ul>'
                
            # %% Video Generation
            
            if json_obj['video_url'] != '':
                response = response + '<div class="chat-text-divider"></div>'
                response = response + '<div class="chat-buttons-container"><button><a href="' + json_obj['video_url'] 
                response = response + '" >Watch Video</a></button></div>'
            # %% Hyperlink Generation
            
            if json_obj['hyperlink_text'] != '' and json_obj['hyperlink_url'] != '':
                response = response + '<div class="chat-text-divider"></div>'
                
                if '\n' in json_obj['hyperlink_url']:
                    hyperlinks = json_obj['hyperlink_url'].split('\n')
                    hyperlink_texts = json_obj['hyperlink_text'].split('\n')
                    cnt = 0
                    response = response + '<ul>'
                    for hyperlink in hyperlinks:
                        txt = json_obj['hyperlink_text']
                        try:
                            txt = hyperlink_texts[cnt]
                        except Exception as e:
                            pass
                        
                        response = response + '<li><a href="' + hyperlink + '" >' 
                            
                        response = response + txt + '</a></li>'

                        cnt = cnt + 1
                    response = response + '</ul>'
                else:
                    response = response + '<a href="' + json_obj['hyperlink_url'] + '" >' 
                    response = response + json_obj['hyperlink_text'] + '</a>'
            # %% Image Generation
            
            # %% Visit Page Generation
            if json_obj['visit_page'] != '':
                # if response != '':
                #     response = response + '<br>'
                response = response + '<p>Here is a link that may help </p>'
                
                if 'ordering.com' in json_obj['visit_page']:
                    response = response + '<div class="cb-action_btn"><a target="_blank" href="' + \
                        json_obj['visit_page']
                else:
                    response = response + '<div class="cb-action_btn"><a href="' + \
                        UIProtocolHostName + json_obj['visit_page']
                response = response + '" >Click here</a></div>'
                isMoreInfo = True

            # # %% Recommend Generation
            # if json_obj['recommend_intent'] != '':
            #     if isMoreInfo == True:
            #         response = response + '<div class="chat-text-divider" style="margin-top: 33px"></div>'
            #     else:
            #         response = response + '<div class="chat-text-divider"></div>'
            #     response = response + "<p><b>Related Information </b></p>"
            #     response = response + '<ul>'
            #     if '\n' in json_obj['recommend_intent']:
            #         recommend_intents = json_obj['recommend_intent'].split(
            #             '\n')

            #         for recommend_intent in recommend_intents:
            #             if recommend_intent.strip() != '':
            #                 response = response + \
            #                     '<li><a href="#" class="recommended" onclick="recommend(this)">' + \
            #                     recommend_intent + '</a></li>'
            #     else:
            #         response = response + \
            #             '<li><a href="#" class="recommended" onclick="recommend(this)">' + \
            #             json_obj['recommend_intent'] + '</a></li>'
            #     response = response + '</ul>'

            if response == '':
                response = "<p>I am sorry, can you rephrase your question?</p>"
            

            response = '<div class="wpic-conversation-item slide-in-bottom"><div class="wpic-conversation-avatar">' + \
                        '<img src="https://cleverbrain.in/images/BotIcon.png"></div><div class="wpic-conversation-body"><div class="wpic-conversation-text bot">'+\
                            response +\
                        '</div><div class="wpic-conversation-footer">' +\
                        '<span class="wpic-conversation-timestamp" data-direction="bot" data-timestamp="1645595696">[REPONSE_TIME]</span></div>'+\
                        '</div></div>'

        except Exception as e:
            print('Error')
            response = "I am sorry, can you rephrase your question?"
            print(str(e))
            self.logger.write_exception(str(e), 'generate_response')

        return response
