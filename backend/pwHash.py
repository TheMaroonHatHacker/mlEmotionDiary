from bcrypt import hashpw, gensalt, checkpw

class pwHash:
    def __init__(self):
        pass
    def hash(self, password):
        return hashpw(password.encode('utf-8'), gensalt())
    def check(self, password, hashed):
        return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    def decode(self, password):
        return password.decode('utf-8')