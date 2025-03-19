import flet as ft
import UIComponents.GreenBackground as gb
import json, httpx

class roleButton(ft.ElevatedButton):
    def __init__(self, label : str, desc : str):
        super().__init__()
        
        self.role = label
        
        self.width=175
        self.style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_700,
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        
        self.content=ft.Column(
            controls=[
                ft.Text(label, color=ft.Colors.BLACK, size=25, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(desc, color=ft.Colors.BLACK54, size=12, text_align=ft.TextAlign.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Center vertically
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center horizontally
        )
        
        self.on_click = self.onClick
    
    def onClick(self,e):
        with open("Backend/registration.json", "r") as f:
            registration_data = json.load(f)
            
        registration_data["role"] = self.role
        
        with open("Backend/registration.json", "w") as f:
            json.dump(registration_data, f, indent=4)
        
        if e.control.role == "Volunteer":
            self.page.go("/Register/Skills")
        elif e.control.role == "Organization":
            with open("Backend/session.json", "r") as f:
                session_data = json.load(f)
            
            userid = session_data["user_id"]
            
            url = "http://127.0.0.1:8000/users/change-role"
            
            with httpx.Client() as client:
                response = client.patch(url, params={"UserId": userid, "role": str(e.control.role)})

                self.page.go("/")

class Role(gb.Box):
    def __init__(self, page):
        super().__init__()
        
        self.content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    # Header
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(value="Pick your role!", weight=ft.FontWeight.BOLD, size=30, text_align=ft.TextAlign.CENTER)
                    ),
                    ft. Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(value="Which are you?", color=ft.Colors.BLACK54)
                    ),
                    
                    # Login Button
                    ft.Container(
                        width=page.width,
                        height=170,
                        border_radius=5,
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            controls=[
                                roleButton("Volunteer", "Participate in organized charitable events!"),
                                roleButton("Organization", "Host events for volunteers to participate in!")
                            ]
                        )
                    )
                ]
            )

class Page(ft.View):
    def __init__(self,page):
        super().__init__()
        
        self.bgcolor = ft.Colors.BLACK
        self.route="/Register/Role"
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
                content=Role(page)
            )
        ]