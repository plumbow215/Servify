import flet as ft
from Pages.Dashboard import Dashboard
import UIComponents.Sidebar as Sidebar
import UIComponents.Page as Page

class OrganizerDashboard(Dashboard):
    def __init__(self, page):
        super().__init__(page, load_events=False)

        self.createEventButton = ft.ElevatedButton(
            text="Create Event",
            icon=ft.icons.ADD,  # ➕ Add icon
            bgcolor=ft.Colors.GREEN_700,  # Background color
            color=ft.Colors.BLACK,  # Text color
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20)  # Rounded corners
            ),
            on_click=lambda e: page.go("/Organizer/Dashboard/OrganizeEvent")
        )
        
        self.Title.content.controls.append(self.createEventButton)
        
        self.LoadEvents()
        
        
class Page(Page.View):
    def __init__(self, page):
        super().__init__(page)
        
        self.Row.controls.append(OrganizerDashboard(page))
        self.route = "/OrganizerDashboard"
