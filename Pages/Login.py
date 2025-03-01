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

class Login(Container):
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
                        content=Text(value="Sign in to Servify", weight=FontWeight.BOLD, size=30, text_align=TextAlign.CENTER)
                    ),
                    Container(
                        alignment=alignment.center,
                        content=Text(value="Volunteer to organized events!", color=Colors.BLACK54)
                    ),
                    
                    # Email & Password
                    LoginField("Email", False, page.width),
                    LoginField("Password", True, page.width),
                    Container(
                        alignment=alignment.center,
                        content=TextButton(
                                    content=(
                                        Text(value="Forgot password?", weight=FontWeight.BOLD, color=Colors.BLACK)
                                    )
                                ),
                    ),
                    
                    # Login Button
                    Container(
                        bgcolor=Colors.BLACK87,
                        width=page.width,
                        height=50,
                        border_radius=5,
                        alignment=alignment.center,
                        on_click=lambda _: page.go('/Dashboard'),
                        content=(
                            Text(value="Login", size=20, weight=FontWeight.BOLD, color=Colors.WHITE)
                        )
                    ),
                    
                    Container(
                        content=(
                            Row(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Text("Don't have an account?"),
                                    TextButton(content=Text(value="Register Now!", weight=FontWeight.BOLD, color=Colors.BLACK))
                                ]
                            )
                        )    
                    )
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
                content=Login(page)
            )
        ]