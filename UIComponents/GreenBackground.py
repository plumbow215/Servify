import flet as ft

def getBackground(page):
    return ft.Container(
                expand=True,
                margin=0,
                padding=10,
                width=page.width,
                height=page.height,
                bgcolor=ft.Colors.GREEN_600,
                border_radius=20,
    )

class Box(ft.Container):
    def __init__(self):
        super().__init__()
        
        self.alignment = ft.alignment.center
        self.bgcolor = ft.Colors.GREEN_600
        self.width = 400
        self.height = 400
        self.border_radius = 10
        self.padding = ft.padding.only(left=20, right=20)