import pickle
import base64



from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key)
f = Fernet(b'tIoUIXthxKcwzYY9uEKnyyir_eKQUlCqvB1tKH5eG7U=')

token = f.encrypt(b"Esprit12")
print('token encryoted ',token)

mydict = token
output = open('myfile.pkl', 'wb')
pickle.dump(mydict, output)


encoded = base64.b64encode(token)
print('Token encoded: ',encoded)
print(type(encoded))


keyencode = base64.b64encode(b'tIoUIXthxKcwzYY9uEKnyyir_eKQUlCqvB1tKH5eG7U=')
print('keyencode',keyencode)
