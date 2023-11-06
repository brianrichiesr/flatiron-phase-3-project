class Player:
    def __init__(self, username):
        self.username = username
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        elif not 1 <= len(username) <= 10:
            raise ValueError("Username must be between 1 and 10 characters long")
        else:
            self._username = username