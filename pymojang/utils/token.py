import pickle

class TokenPair:

    def __init__(self, access_token: str, client_token: str):
        self.__access_token = access_token
        self.__client_token = client_token

    @property
    def access_token(self):
        return self.__access_token

    @property
    def client_token(self):
        return self.__client_token

    def update(self, **kwargs):
        self.__access_token = kwargs.get('access_token', self.access_token)
        self.__client_token = kwargs.get('client_token', self.client_token)
            
    def to_pickle(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def from_pickle(cls, filename: str):
        obj = None
        with open(filename, 'rb') as f:
            obj = pickle.load(f)
        
        return obj

    def __getnewargs__(self):
        return (self.access_token, self.client_token)

    def __iter__(self):
        return (self.access_token, self.client_token).__iter__()

    def __str__(self):
        return "('{}','{}')".format(self.access_token, self.client_token)

    def __repr__(self):
        return "('{}','{}')".format(self.access_token, self.client_token)
