from flet import *

class LoginField(TextField):
    def __init__(self, Label : str, isPassword : bool, pageWidth : int):
        super().__init__()
        
        if isPassword:
            self.password = True
            self.can_reveal_password = True
            self.prefix_icon = Icons.LOCK
        elif isPassword == False:
            self.prefix_icon = Icons.EMAIL
        
        self.width = pageWidth
        self.label = Label
        self.border_radius = 5
        
class VerificationField(TextField):
    def __init__(self, Label : str, page):
        super().__init__()
        
        self.prefix_icon = Icons.MARK_EMAIL_READ_ROUNDED
        self.width = page.width
        self.label = Label
        self.border_radius = 5