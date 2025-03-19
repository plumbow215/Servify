import flet as ft
import UIComponents.Sidebar as Sidebar
import json

class View(ft.View):
    def __init__(self, page):
        super().__init__(page)
        
        with open("Backend/session.json", "r") as f:
            session_data = json.load(f)
        
        if session_data["role"]:
            if session_data["role"] == "Volunteer":
                self.useSidebar = Sidebar.UI(page)
            elif session_data["role"] == "Organization":
                self.useSidebar = Sidebar.OrganizerUI(page)

        self.Row=ft.Row(
            expand=True,
            width=page.window.width,
            height=page.window.height,
            controls=[
                self.useSidebar 
            ]
        )
        
        self.bgcolor = ft.Colors.BLACK
        self.route="/Dashboard",
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
                    self.Row
                )
            )
        ]