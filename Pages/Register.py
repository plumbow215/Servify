import flet as ft
from UIComponents import LoginField
import httpx

class Register(ft.Container):
    def __init__(self, page):
        super().__init__()
        
        self.alignment = ft.alignment.center
        self.bgcolor = ft.Colors.GREEN_600
        self.width=400
        self.height=400
        self.border_radius=10
        self.padding=ft.padding.only(left=20, right=20)
        
        self.Username = LoginField.LoginField("Username", False, page.width)
        self.Email = LoginField.LoginField("Email", False, page.width)
        self.Password = LoginField.LoginField("Password", True, page.width)
        self.status_text = ft.Text("", color=ft.Colors.RED, weight=ft.FontWeight.BOLD)
                    
        self.content=(
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    # Header
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(value="Create an account", weight=ft.FontWeight.BOLD, size=30, text_align=ft.TextAlign.CENTER)
                    ),
                    
                    # Email & Password
                    self.Username,
                    self.Email,
                    self.Password,
                    
                    ft. Container(
                        alignment=ft.alignment.center,
                        content=self.status_text
                    ),
                    
                    # Register Button
                    ft.Container(
                        bgcolor=ft.Colors.BLACK87,
                        width=page.width,
                        height=50,
                        border_radius=5,
                        alignment=ft.alignment.center,
                        on_click=self.create_account,
                        content=(
                            ft.Text(value="Register", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        )
                    ),
                    
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.TextButton(
                                on_click=lambda _: page.go('/'),
                                    content=(
                                        ft.Text(value="Go back to Login Page", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
                                    )
                                ),
                    ),
                ]
            )
        )
        
    async def create_account(self , e):
        username = self.Username.value
        email = self.Email.value
        password = self.Password.value
        
        url = "http://127.0.0.1:8000/users/create-user"
        
        async with httpx.AsyncClient() as client:
            response = await(client.post(url, params={"username": username, "email": email, "password": password}))
            
            print(response.status_code)
            
            if response.status_code == 200:
                self.page.go("/")
            else:
                self.Username.border_color = ft.Colors.RED
                self.Email.border_color = ft.Colors.RED
                self.Password.border_color = ft.Colors.RED
                self.status_text.value = response.json().get("detail")
                
        

# When you click on the Logout button, it shows the Login Page
class Page(ft.View):
    def __init__(self,page):
        super().__init__()
        
        self.bgcolor = ft.Colors.BLACK
        self.route="/"
        self.controls=[
            ft.AppBar(
                    bgcolor=ft.Colors.BLACK,
                    title=ft.Text("Servify", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=35),
                ),
            ft.Container(
                expand=True,
                width=page.width,
                height=page.height,
                bgcolor=ft.Colors.BLACK12,
                alignment=ft.Alignment(0,-.35),
                content=Register(page)
            )
        ]