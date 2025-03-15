import flet as ft
from UIComponents import LoginField
import httpx
import json

class Login(ft.Container):
    def __init__(self, page):
        super().__init__()
        
        self.alignment = ft.alignment.center
        self.bgcolor = ft.Colors.GREEN_600
        self.width=400
        self.height=400
        self.border_radius=10
        self.padding=ft.padding.only(left=20, right=20)
        
        self.email_field = LoginField.LoginField("Email", False, page.width)
        self.password_field = LoginField.LoginField("Password", True, page.width)
        self.status_text = ft.Text("", color=ft.Colors.RED, weight=ft.FontWeight.BOLD)
        
        self.content=(
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    # Header
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(value="Sign in to Servify", weight=ft.FontWeight.BOLD, size=30, text_align=ft.TextAlign.CENTER)
                    ),
                    ft. Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(value="Volunteer to organized events!", color=ft.Colors.BLACK54)
                    ),
                    
                    # Email & Password
                    self.email_field,
                    self.password_field,
                    
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.TextButton(
                                on_click=lambda _: page.go('/ForgotPassword'),
                                    content=(
                                        ft.Text(value="Forgot password?", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
                                    )
                                ),
                    ),
                    
                    # Login Button
                    ft.Container(
                        bgcolor=ft.Colors.BLACK87,
                        width=page.width,
                        height=50,
                        border_radius=5,
                        alignment=ft.alignment.center,
                        on_click=self.login,
                        content=(
                            ft.Text(value="Login", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        )
                    ),
                    
                    ft. Container(
                        alignment=ft.alignment.center,
                        content=self.status_text
                    ),
                    
                    ft.Container(
                        content=(
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Text("Don't have an account?"),
                                    ft.TextButton(content=ft.Text(value="Register Now!", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), on_click=lambda _: page.go('/Register'))
                                ]
                            )
                        )    
                    )
                ]
            )
        )
        
    async def login(self, e):
        email = self.email_field.value
        password = self.password_field.value
        
        url = "http://127.0.0.1:8000/users/verify-login"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, params={"email":email, "password":password})
            
            # if its successful then
            if response.status_code == 200:
                self.page.go("/Dashboard")
                    
            else:
                self.email_field.border_color=ft.Colors.RED
                self.password_field.border_color=ft.Colors.RED
                self.status_text.value = response.json().get("detail")
                self.page.update()
        

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
                content=Login(page)
            )
        ]