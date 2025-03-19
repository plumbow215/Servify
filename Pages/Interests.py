import flet as ft
import UIComponents.GreenBackground as gb
import Misc.interests as sk
import json, httpx

class Interests(gb.Box):
    def __init__(self, page):
        super().__init__()
        
        listView = ft.ListView(
            height=250,
        )
        
        for skill in sk.interests:
            # Create a checkbox for each skill
            checkbox = ft.Checkbox(label=skill, value=False)
            checkbox.on_change=self.onClick
            listView.controls.append(checkbox)

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(alignment=ft.alignment.center,content=ft.Text(value="Choose your interests!", weight=ft.FontWeight.BOLD, size=30, text_align=ft.TextAlign.CENTER)),
                    ft.Divider(color=ft.Colors.BLACK),
                    listView,
                    ft.Container(
                        bgcolor=ft.Colors.BLACK87,
                        width=page.width,
                        height=50,
                        border_radius=5,
                        alignment=ft.alignment.center,
                        on_click=self.confirm,
                        content=(
                            ft.Text(value="Create Account", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        )
                    ),
                ]
            )
        )
    
    def confirm(self, e):
        session_path = "Backend/session.json"

        # Load session data
        try:
            with open(session_path, "r") as f:
                session_data = json.load(f)
                user_id = session_data.get("user_id")
                if user_id is None:
                    print("Error: User ID not found in session.json")
                    return
        except (FileNotFoundError, json.JSONDecodeError) as err:
            print(f"Error loading session.json: {err}")
            return

        url = "http://127.0.0.1:8000/users/update-registration"

        try:
            response = httpx.patch(url, params={"UserId": user_id})
            if response.status_code == 200:
                print(response.json())  # Log the success message
                self.page.go("/")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except httpx.RequestError as err:
            print(f"Request failed: {err}")
        
    def onClick(self, e):
        with open("Backend/registration.json", "r") as file:
            reg_data = json.load(file)

        interest = e.control.label
        value = e.control.value
        
        if value == True:
            if interest not in reg_data["interests"]:
                reg_data["interests"].append(interest)
        else:
            if interest in reg_data["interests"]:
                reg_data["interests"].remove(interest)

        # Write the updated data back to the file.
        with open("Backend/registration.json", "w") as file:
            json.dump(reg_data, file, indent=4)

class Page(ft.View):
    def __init__(self,page):
        super().__init__()
        
        self.bgcolor = ft.Colors.BLACK
        self.route="/Register/Interests"
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
                content=Interests(page)
            )
        ]