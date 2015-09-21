import pickle
import base64



from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key)
f = Fernet(b'tIoUIXthxKcwzYY9uEKnyyir_eKQUlCqvB1tKH5eG7U=')

token = f.encrypt(b"Esprit12")
print('encryoted ',token)
encoded = base64.b64encode(token)
print('encoded: ',encoded)



decoded = base64.b64decode(encoded)
print('decoded ',decoded.decode("utf-8") )
toto = decoded.decode("utf-8")
print('decoded byte ',bytes(toto, 'utf-8') )

print('password ',f.decrypt(decoded))

# write python dict to a file
mydict = encoded
output = open('myfile.pkl', 'wb')
pickle.dump(mydict, output)
output.close()

# read python dict back from the file
pkl_file = open('myfile.pkl', 'rb')
mydict2 = pickle.load(pkl_file)
pkl_file.close()
t = 'tIoUIXthxKcwzYY9uEKnyyir_eKQUlCqvB1tKH5eG7U='
t = bytes(t ,'utf-8')
print(t)
print (mydict)
print (mydict2)