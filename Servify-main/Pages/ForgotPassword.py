from flet import *

from flet import *
from UIComponents import LoginField

class ForgotPassword(Container):
    def __init__(self, page):
        super().__init__()
        
        self.alignment = alignment.center
        self.bgcolor = Colors.GREEN_600
        self.width=400
        self.height=400
        self.border_radius=10
        self.padding=padding.only(left=20, right=20)
        self.content=(
            Column(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    # Header
                    Container(
                        alignment=alignment.center,
                        content=Text(value="Enter your email", weight=FontWeight.BOLD, size=30, text_align=TextAlign.CENTER)
                    ),
                    
                    # Email & Password
                    LoginField.LoginField("Email", False, page.width),
                    LoginField.VerificationField("Verfication Code", page),
                    
                    # Login Button
                    Container(
                        bgcolor=Colors.BLACK87,
                        width=page.width,
                        height=50,
                        border_radius=5,
                        alignment=alignment.center,
                        on_click=lambda _: page.go('/'),
                        content=(
                            Text(value="Send verification code", size=20, weight=FontWeight.BOLD, color=Colors.WHITE)
                        )
                    ),
                ]
            )
        )

# When you click on the Logout button, it shows the Login Page
class Page(View):
    def __init__(self,page):
        super().__init__()
        
        self.bgcolor = Colors.BLACK
        self.route="/"
        self.controls=[
            AppBar(
                    bgcolor=Colors.BLACK,
                    title=Text("Servify", color=Colors.WHITE, weight=FontWeight.BOLD, size=35),
                ),
            Container(
                expand=True,
                width=page.width,
                height=page.height,
                bgcolor=Colors.BLACK12,
                alignment=Alignment(0,-.35),
                content=ForgotPassword(page)
            )
        ]