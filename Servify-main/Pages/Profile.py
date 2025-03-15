from flet import *
from UIComponents import Sidebar
from UIComponents import *

class Information(Container):
    def __init__(self, Label, Info):
        super().__init__()
        
        self.alignment=alignment.center
        self.content=(
            Column(
                controls=[
                    Text(Label, weight=FontWeight.BOLD, size=17),
                    Text(Info, text_align=TextAlign.CENTER)
                ]
            )
        )

class Profile(Container):
    def __init__(self, page, realName:None, userName:None, Email:None, aboutMe:None, accountCreation:None, lastActive:None, Services:None):
        super().__init__()
        
        self.bgcolor=Colors.GREEN_600
        self.width=980
        self.height=page.height
        self.padding=20
        self.border_radius=20
        self.content=(
            Column(
                controls=[
                    Text("Profile", size=40, weight=FontWeight.BOLD),
                    #profile + information
                    Row(
                        controls=[
                            CircleAvatar(
                                width=100,
                                height=100,
                                bgcolor=Colors.BLACK,
                                content=Text("FF", color=Colors.ORANGE)
                            ),
                            Information("Account Creation", accountCreation),
                            Information("Last Active", lastActive),
                            Information("Services", Services)
                        ]
                    ),
                    Divider(color=Colors.BLACK),
                    
                    #real name
                    TextField(label="Name", value=realName, read_only=True),
                    Divider(color=Colors.BLACK),
                    
                    #email
                    TextField(label="Email Address",value=Email, read_only=True, prefix_icon=Icons.EMAIL),
                    Divider(color=Colors.BLACK),
                    
                    #username
                    TextField(label="Username",value=userName, read_only=True, prefix_icon=Icons.ALTERNATE_EMAIL),
                    Divider(color=Colors.BLACK),
                    
                    #aboutme
                    TextField(label="About Me", value=aboutMe, read_only=True, multiline=True),
                ]
            )
        )

# When you click on the Profile button, it shows the Profile Page
class Page(View):
    def __init__(self, page):
        super().__init__()
        
        self.bgcolor = Colors.BLACK
        self.route="/Dashboard/Profile",
        self.controls=[
            AppBar(
                bgcolor=Colors.BLACK,
                title=Text("Servify", color=Colors.WHITE, weight=FontWeight.BOLD, size=35),
            ),
            Container(
                bgcolor=Colors.BLACK,
                expand=True,
                width=page.width,
                height=page.height,
                alignment=alignment.center,
                content=(
                    Row(
                        expand=True,
                        width=page.window.width,
                        height=page.window.height,
                        controls=[
                            Sidebar.UI(page),
                            Profile(page, "Ethan Guardian", "plumbow", "ejmguardian@mymail.mapua.edu.ph", None, "17 Feb 2025", "25 Feb 2025", 1)
                        ]
                    )
                )
            )
        ]