import flet as ft
from UIComponents import Sidebar
from UIComponents import *
import httpx, json

class Profile(ft.Container):
    def __init__(self, page):
        super().__init__()
        
        self.page = page
        self.bgcolor=ft.Colors.GREEN_600
        self.width=980
        self.height=page.height
        self.padding=20
        self.border_radius=20
        
        #self.realName = ft.TextField(label="Name", value=realName, read_only=True),
        self.emailAddress = ft.TextField(label="Email Address", read_only=True, prefix_icon=ft.Icons.EMAIL)
        self.username = ft.TextField(label="Username", read_only=True, prefix_icon=ft.Icons.ALTERNATE_EMAIL)
        self.aboutMe = ft.TextField(label="About Me", read_only=True, multiline=True)
        self.accountCreation = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Created On", weight=ft.FontWeight.BOLD, size=17),
                    ft.Text("Loading..", text_align=ft.TextAlign.CENTER)
                ]
            )
        )
        
        self.lastActive = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Last Active", weight=ft.FontWeight.BOLD, size=17),
                    ft.Text("Loading..", text_align=ft.TextAlign.CENTER)
                ]
            )
        )
        self.Services = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("No. of Services", weight=ft.FontWeight.BOLD, size=17),
                    ft.Text("Loading..", text_align=ft.TextAlign.CENTER)
                ]
            )
        )
        
        self.Column = ft.Column(
                controls=[
                    ft.Text("Profile", size=40, weight=ft.FontWeight.BOLD), #[0]
                    #profile + information
                    ft.Row(                                                 #[1]
                        controls=[
                            ft.CircleAvatar(
                                width=100,
                                height=100,
                                bgcolor=ft.Colors.BLACK,
                                content=ft.Text("FF", color=ft.Colors.ORANGE)
                            ),
                            self.accountCreation,
                            self.lastActive,
                            self.Services
                        ]
                    ),
                    ft.Divider(color=ft.Colors.BLACK),                      #[2]
                    
                    #email
                    self.emailAddress,                                      #[3]
                    ft.Divider(color=ft.Colors.BLACK),                      #[4]
                    
                    #username
                    self.username,                                          #[5]
                    ft.Divider(color=ft.Colors.BLACK),                      #[6]
                    
                    #aboutme
                    self.aboutMe                                            #[7]
                ]
            )
        
        self.content=self.Column
        
        self.displayProfile()
    
    def displayProfile(self):
        with open("Backend/session.json", "r") as file:
            session_data = json.load(file)
                
        url = f"http://127.0.0.1:8000/Profile/{session_data['user_id']}"
        
        with httpx.Client() as client:
            
            
            response = client.get(url, params={"user_id": session_data["user_id"]})
            
            if response.status_code == 200:
                data = response.json()

                if "user" in data:
                    user = data["user"][0]
                    
                    self.username.value = user["username"]
                    self.emailAddress.value = user["email"]
                    self.aboutMe.value = user["aboutMe"]
                    
                    self.accountCreation.content.controls[1].value = user['creationDate']
                    self.lastActive.content.controls[1].value = user["lastActive"]
                    self.Services.content.controls[1].value = user["services"]
                    
                    self.page.update()
                    

# When you click on the Profile button, it shows the Profile Page
class Page(ft.View):
    def __init__(self, page):
        super().__init__()
        
        self.bgcolor = ft.Colors.BLACK
        self.route="/Dashboard/Profile",
        self.controls=[
            ft.AppBar(
                bgcolor=ft.Colors.BLACK,
                title=ft.Text("Servify", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=35),
            ),
            ft.Container(
                bgcolor=ft.Colors.BLACK,
                expand=True,
                width=page.width,
                height=page.height,
                alignment=ft.alignment.center,
                content=(
                    ft.Row(
                        expand=True,
                        width=page.window.width,
                        height=page.window.height,
                        controls=[
                            Sidebar.UI(page),
                            Profile(page)
                        ]
                    )
                )
            )
        ]