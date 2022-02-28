import base64
cipherText = ''
plainText = ''
exceptions = ''
def encode(message):
    try:
        cipherText = base64.b64encode(message.encode())
    except Exception as e:
        exceptions = str(e)
        
    return cipherText

def decode(message):
    try:
        plainText = base64.b64decode(message)
    except Exception as e:
        exceptions = str(e)
    
    return plainText.decode()


# import string

# alphabet = string.ascii_lowercase # "abcdefghijklmnopqrstuvwxyz"
# key = 42856973135874619

# def encrypt(message):
    
#     encrypted_message = ""

#     for c in message:

#         if c in alphabet:
#             position = alphabet.find(c)
#             new_position = (position + key) % 26
#             new_character = alphabet[new_position]
#             encrypted_message += new_character
#         else:
#             encrypted_message += c

#     return encrypted_message

# def decrypt(encrypted_message):
    
#     decrypted_message = ""

#     for c in encrypted_message:

#         if c in alphabet:
#             position = alphabet.find(c)
#             new_position = (position - key) % 26
#             new_character = alphabet[new_position]
#             decrypted_message += new_character
#         else:
#             decrypted_message += c

#     return decrypted_message



# from cryptography.fernet import Fernet

# key = Fernet.generate_key()

# print(key)
