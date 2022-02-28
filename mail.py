from email.mime.base import MIMEBase
import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

user = 'chatbotnotifier@gmail.com'
password = 'Brainy123$'
smtp = 'smtp.gmail.com'

port = 587

def SendMail(to_address, subject, body, attachments):
    sent_from = user

    email_text = """\
    Subject: %s
    %s
    """ % (subject, body)
    print(email_text)

    message = MIMEMultipart()
    message['From'] = sent_from
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'html'))

    imgCnt = 1
    for attachement in attachments:
        # to add an attachment is just add a MIMEBase object to read a picture locally.
        with open(attachement, 'rb') as f:
            tempfilename = 'img' + str(imgCnt) + '.png'
            # set attachment mime and file name, the image type is png
            mime = MIMEBase('image', 'png', filename=tempfilename)
            # add required header data:
            mime.add_header('Content-Disposition', 'attachment', filename=tempfilename)
            mime.add_header('X-Attachment-Id', '0')
            mime.add_header('Content-ID', '<0>')
            # read attachment file content into the MIMEBase object
            mime.set_payload(f.read())
            # encode with base64
            encoders.encode_base64(mime)
            # add MIMEBase object to MIMEMultipart object
            message.attach(mime)

            imgCnt = imgCnt + 1

    try:
        context = ssl.create_default_context()
        smtp_server = smtplib.SMTP(smtp, port)
        smtp_server.starttls(context=context)
        smtp_server.ehlo()
        smtp_server.login(user, password)
        smtp_server.sendmail(sent_from, to_address, message.as_string())
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)


# actbody = """
# <html>
#     <body>
#         <p>
#             Hi,
#         </p>
#         <p>
#             <b>Threat has been detected in Clever Eye 2 Camera.</b>
#         </p>
#         <p>
#             <img src="cid:0">
#         </p>
#     </body>
# </html>
# """ 
# SendMail("siva@cleverbrain.in", "Threat Detected", actbody, ['frame25.jpg'])
