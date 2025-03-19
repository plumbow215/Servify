from fastapi import FastAPI
import flet as ft
from Pages import *
from Backend.routes.User import router as User
from Backend.routes.Profile import router as Profiles
from Backend.routes.CommunityServices import router as CommunityServices
from Backend.routes.BookmarkedServices import router as BookmarkedServices

app = FastAPI()

app.include_router(BookmarkedServices)
app.include_router(CommunityServices)
app.include_router(User)
app.include_router(Profiles)

def main(page: ft.Page) -> None:
    page.title = "Servify"
    page.bgcolor = ft.Colors.BLACK
    page.window.min_height = 700
    page.window.min_width = 1080
        
    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.BLACK,
        title=ft.Text("Servify", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=35),
    )
    
    loginUI = ft.Container(
            expand=True,
            width=page.width,
            height=page.height,
            bgcolor=ft.Colors.BLACK12,
            alignment=ft.Alignment(0,-.35),
            content=Login.Login(page)
        )
    
    def routeChange(e) -> None:
        pageRerouting = {
            "/Dashboard/ServiceRecords": ServiceRecords.Page(page),
            "/Dashboard/Profile": Profile.Page(page),
            "/Dashboard/Event": Events.Page(page),
            "/Dashboard": Dashboard.Page(page),
            
            "/Organizer/Dashboard/OrganizeEvent": OrganizeEvent.Page(page),
            "/Organizer/Dashboard": OrganizerDashboard.Page(page),
            
            "/Register/Role": Role.Page(page),
            "/Register/Skills": Skills.Page(page),
            "/Register/Interests": Interests.Page(page),
            "/Register": Register.Page(page),
            
            "/ForgotPassword": ForgotPassword.Page(page),
            "/": Login.Page(page),
        }
        
        page.views.clear()
        page.views.append(pageRerouting[page.route])
        page.update()
    
    page.add(
        loginUI
    )
    
    page.on_route_change = routeChange
    
if __name__ == '__main__':
    ft.app(target=main)