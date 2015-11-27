import pickle
import base64

from cryptography.fernet import Fernet

f = Fernet(b'tIoUIXthxKcwzYY9uEKnyyir_eKQUlCqvB1tKH5eG7U=')
b= bytes('tIoUIXthxKcwzYY9uEKnyyir_eKQUlCqvB1tKH5eG7U=','utf-8')
print(b)