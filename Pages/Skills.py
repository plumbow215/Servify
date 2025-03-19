import flet as ft
import UIComponents.GreenBackground as gb
import Misc.skills as sk
import json

class Skills(gb.Box):
    def __init__(self, page):
        super().__init__()
        
        listView = ft.ListView(
            height=250,
        )
        
        for skill in sk.skills:
            # Create a checkbox for each skill
            checkbox = ft.Checkbox(label=skill, value=False)
            checkbox.on_change=self.onClick
            listView.controls.append(checkbox)

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(alignment=ft.alignment.center,content=ft.Text(value="Choose your skills!", weight=ft.FontWeight.BOLD, size=30, text_align=ft.TextAlign.CENTER)),
                    ft.Divider(color=ft.Colors.BLACK),
                    listView,
                    ft.Container(
                        bgcolor=ft.Colors.BLACK87,
                        width=page.width,
                        height=50,
                        border_radius=5,
                        alignment=ft.alignment.center,
                        on_click=lambda e: page.go("/Register/Interests"),
                        content=(
                            ft.Text(value="Confirm", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        )
                    ),
                ]
            )
        )
        
    def onClick(self, e):

        with open("Backend/registration.json", "r") as file:
            reg_data = json.load(file)

        interest = e.control.label
        value = e.control.value
        
        if value == True:
            if interest not in reg_data["skills"]:
                reg_data["skills"].append(interest)
        else:
            if interest in reg_data["skills"]:
                reg_data["skills"].remove(interest)

        # Write the updated data back to the file.
        with open("Backend/registration.json", "w") as file:
            json.dump(reg_data, file, indent=4)

class Page(ft.View):
    def __init__(self,page):
        super().__init__()
        
        self.bgcolor = ft.Colors.BLACK
        self.route="/Register/Skills"
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
                content=Skills(page)
            )
        ]