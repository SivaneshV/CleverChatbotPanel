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
        
    def generate_feedback(self, disp_t):
        return '<div class="wpic-conversation-item slide-in-bottom">' +\
        '<div class="wpic-conversation-avatar"><img src="https://botsify-production-eu-1.s3.eu-west-1.amazonaws.com/web-bot/avatars/110177.png"></div>' +\
        '<div class="wpic-conversation-body">' +\
        '<div class="wpic-conversation-text" style="background:#EBEFF4 !important">' +\
        '<p class="chat-text" dir="auto">Do you need help with anything else?</p>' +\
        '<div class="cb-quick_replies" style="">' +\
        '<button class="btn btn-primary btn-sm cb-quick_msg quick_reply_buttons" style="background-color:var(--bot_theme) !important; white-space: normal;color:white; margin-top:0px;" data-qr-title="Yes" data-qr-payload="Yes">Yes</button>' +\
        '<button class="btn btn-primary btn-sm cb-quick_msg quick_reply_buttons" style="background-color:var(--bot_theme) !important; white-space: normal;color:white; margin-top:0px;" data-qr-title="No" data-qr-payload="No">No</button>' +\
        '</div>' +\
        '</div>' +\
        '<div class="wpic-conversation-footer"><span class="wpic-conversation-timestamp" data-direction="bot" data-timestamp="1646385563">'+disp_t+'</span></div>' +\
        '</div>' +\
        '</div>'

    def generate_plain_text(self, text, disp_t):
        return '<div class="wpic-conversation-item slide-in-bottom"><div class="wpic-conversation-avatar">' + \
                            '<img src="https://cleverbrain.in/images/BotIcon.png"></div><div class="wpic-conversation-body"><div class="wpic-conversation-text bot">'+\
                            '<p class="chat-text" dir="auto">' + text + '</p>'+\
                            '</div><div class="wpic-conversation-footer">' +\
                            '<span class="wpic-conversation-timestamp" data-direction="bot" data-timestamp="1645595696">'+disp_t+'</span></div>'+\
                            '</div></div>'
        

    def generate_response(self, json_data, UIProtocolHostName, Lang):
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

            # %% Control Generation
            if json_obj['other'] == 'Get User Contact':
                response = '''
                <div role="row" class="cb-1gvabgf" id="getcontact">
                    <div role="gridcell" class="cb-1jm5qtp e1r9cm3y0" tabindex="0">
                        <div aria-hidden="true" class="cb-1ywcuv7 e1q4zsg91">
                            <div class="cb-3pmf97 e1q4zsg90"><svg color="#FFFFFF" viewBox="0 0 32 32" class="cb-1mpchac"><path d="M18.8,16.3C17.9,16.8,17,17,16,17c-1,0-1.9-0.2-2.8-0.7c-3.2,0.8-5.2,2.8-5.2,5c0,0.8,0,0.9,0,2c0,0,0,0,0.1,0	c0.4,0.1,1,0.3,1.9,0.4c1.6,0.2,3.8,0.3,6.1,0.3s4.5-0.1,6.1-0.3c0.8-0.1,1.4-0.2,1.9-0.4c0,0,0.1,0,0.1,0v-2	C24,19.2,21.9,17.1,18.8,16.3z M20.6,14.8c3.2,1.2,5.4,3.7,5.4,6.5v2.4c0,1.8-3.7,2.2-10,2.2S6,25.5,6,23.8c0-1.5,0-1.5,0-2.4	c0-2.9,2.2-5.3,5.4-6.5c-0.9-1-1.4-2.4-1.4-3.8c0-3.3,2.7-6,6-6s6,2.7,6,6C22,12.5,21.5,13.8,20.6,14.8z M16,15c2.2,0,4-1.8,4-4	s-1.8-4-4-4s-4,1.8-4,4S13.8,15,16,15z"></path></svg></div>
                        </div>
                        <div id="i49ri9srqec" aria-hidden="false" class="cb-1c6qsjd e9s6ynt0" style="max-height: none;">
                            <div class="cb-vlmzoh e1cdxu9o0">
                                <form name="form_153200509478604627" class="cb-71fb3p e1nyj5rz0">
                                    <div class="cb-1g9ek8d e108e6fy0">
                                        <div class="cb-1qa09gl eptvlbh0">
                                            <div class="cb-1ynzeli e12liu9t1">
                                                <h2 class="cb-2g7ffp e12liu9t0">'''+json_obj['output_text']+'''</h2>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="cb-1g9ek8d e108e6fy0">
                                        <div class="cb-1qa09gl eptvlbh0"><label id="react-aria-2400522173-8" for="name" class="cb-ioxvoy e2zxkge0"><span class="Linkify">Your name:</span></label><input id="cb_contact_name" aria-labelledby="react-aria-2400522173-8" type="text" aria-required="true"
                                                aria-errormessage="react-aria-2400522173-7" autocomplete="name" name="name" class="cb-22twvl e1xplv9i0" value="" tabindex="-1" aria-invalid="true">
                                        </div>
                                    </div>
                                    <div class="cb-1g9ek8d e108e6fy0">
                                        <div class="cb-1qa09gl eptvlbh0"><label id="react-aria-2400522173-10" for="email" class="cb-ioxvoy e2zxkge0"><span class="Linkify">E-mail:</span></label><input id="cb_contact_email" aria-labelledby="react-aria-2400522173-10" type="email" aria-required="true"
                                                aria-errormessage="react-aria-2400522173-9" autocomplete="email" name="email" class="cb-22twvl e1xplv9i0" value="" tabindex="-1">
                                            <p id="react-aria-2400522173-9" role="alert" class="cb-1p8zazf exlwksr0" style="height: 0px;"></p>
                                        </div>
                                    </div>
                                    <div class="cb-1g9ek8d e108e6fy0">
                                        <div class="cb-1qa09gl eptvlbh0"><label id="react-aria-2400522173-12" for="9e5nl6d7qjb_153200509478607391" class="cb-ioxvoy e2zxkge0"><span class="Linkify">Your Contact #:</span></label><input id="cb_contact_number" aria-labelledby="react-aria-2400522173-12"
                                                type="text" aria-required="true" aria-errormessage="react-aria-2400522173-11" autocomplete="off" name="9e5nl6d7qjb_153200509478607391" class="cb-22twvl e1xplv9i0" value="" tabindex="-1">
                                            <p id="react-aria-2400522173-11" role="alert" class="cb-1p8zazf exlwksr0" style="height: 0px;"></p>
                                        </div>
                                    </div>
                                    <div class="cb-1g9ek8d e108e6fy0">
                                        <div class="cb-1qa09gl eptvlbh0">
                                            <fieldset class="cb-1mq73z0">
                                                <div class="cb-5lu3o4 egdebj42">
                                                    <div class="cb-1pm2qf9 egdebj40">
                                                        <div class="cb-7m5ww7">
                                                            <input type="checkbox" id="chk_contact_agree" aria-checked="false" style="margin-top: 0px" class="cb-bzdp9w e81sjne0" value="index0_0" tabindex="-1">
                                                        </div>
                                                    </div><label for="chk_contact_agree" class="cb-36igo0 egdebj41">I agree to receive notifications</label></div>
                                                <p id="react-aria-2400522173-14" role="alert" class="cb-1p8zazf exlwksr0" style="height: 0px;"></p>
                                            </fieldset>
                                        </div>
                                    </div>
                                    <p role="alert" class="cb-1p8zazf exlwksr0" style="height: 0px;"></p>
                                    <div class="cb-1s5bjh3 e1n7ru1l0">
                                        <div class="cb-action_btn"><a style="cursor: pointer;" onclick="SendContact()" id="btn_send_contact">Submit</a></div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
                '''

            # %% Image Generation
            if json_obj['image_url'] != '':
                response = '''
                <center>
                <img src="'''+json_obj['image_url']+'''" style="height: 160px;width: auto;max-width: 250px;">
                </center>
                '''+response


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
                
                if 'https://' in json_obj['visit_page'] or 'http://' in json_obj['visit_page'] or 'www.' in json_obj['visit_page']:
                    response = response + '<div class="cb-action_btn"><a target="_blank" href="' + \
                        json_obj['visit_page']
                else:
                    response = response + '<div class="cb-action_btn"><a target="_blank" href="' + \
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
                if Lang == "English":
                    response = "<p>I am sorry, can you rephrase your question?</p>"
                else:
                    response = "<p>மன்னிக்கவும், உங்கள் கேள்வியை மாற்றி முடியுமா?</p>"
            
            if json_obj['other'] != 'Get User Contact':
                response = '<div class="wpic-conversation-item slide-in-bottom"><div class="wpic-conversation-avatar">' + \
                            '<img src="https://cleverbrain.in/images/BotIcon.png"></div><div class="wpic-conversation-body"><div class="wpic-conversation-text bot">'+\
                                response +\
                            '</div><div class="wpic-conversation-footer">' +\
                            '<span class="wpic-conversation-timestamp" data-direction="bot" data-timestamp="1645595696">[REPONSE_TIME]</span></div>'+\
                            '</div></div>'

        except Exception as e:
            print('Error')
            if Lang == "English":
                response = "<p>I am sorry, can you rephrase your question?</p>"
            else:
                response = "<p>மன்னிக்கவும், உங்கள் கேள்வியை மாற்றி முடியுமா?</p>"
            
            response = '<div class="wpic-conversation-item slide-in-bottom"><div class="wpic-conversation-avatar">' + \
                        '<img src="https://cleverbrain.in/images/BotIcon.png"></div><div class="wpic-conversation-body"><div class="wpic-conversation-text bot">'+\
                            response +\
                        '</div><div class="wpic-conversation-footer">' +\
                        '<span class="wpic-conversation-timestamp" data-direction="bot" data-timestamp="1645595696">[REPONSE_TIME]</span></div>'+\
                        '</div></div>'
            print(str(e))
            self.logger.write_exception(str(e), 'generate_response')

        return response
