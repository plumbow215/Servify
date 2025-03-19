import flet as ft
import httpx, json
from UIComponents import *

class EventUI(ft.Container):
    def __init__(self, page):
        super().__init__()
        
        self.page = page
        self.width = 980
        greenBackground = GreenBackground.getBackground(page)
        self.content = greenBackground
        
        #participants
        self.participants = ft.ListView()
        
        #publisher
        self.publisher = [
            ft.CircleAvatar(
                width=50,
                height=50,
                content=ft.Text("FF", color=ft.Colors.ORANGE)
                ),
            ft.Column(
                controls=[
                    ft.Text(value="User", weight=ft.FontWeight.BOLD, size=20),
                    ft.Text(value="Published x time ago", size=12)
                ]
                ),
        ]
        
        #title
        self.eventTitle = ft.Column(
            controls=[ft.Text(value="Title", weight=ft.FontWeight.BOLD, size=25),
                      ft.Text(value="Venue", weight=ft.FontWeight.BOLD, size=15)
                    ]
        )

        #description
        self.eventDescription = ft.Text("Description")
        
        self.joinEvent = ft.TextButton(
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.GREEN_700),
            on_click=self.joinEvent,
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.BOOKMARK_ADD, color=ft.Colors.BLACK12),
                    ft.Text("Participate in Event", color=ft.Colors.BLACK)
                ]
            )
        )
        
        self.addResponse = ft.TextButton(
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.GREEN_700),
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.CHAT, color=ft.Colors.BLACK12),
                    ft.Text("Add Response", color=ft.Colors.BLACK)
                ]
            )
        )
        
        self.Comments = ft.ListView(spacing=5)
        
        greenBackground.content=ft.Row(
                    controls=[
                        ft.Container(
                            width=800,
                            padding=20,
                            content=ft.Column(
                                    controls=[
                                        ft.Row(controls=self.publisher),
                                        self.eventTitle,
                                        self.eventDescription,
                                        ft.Divider(color=ft.Colors.BLACK),
                                        ft.Row(controls=[self.joinEvent , self.addResponse]),
                                        ft.Text("Comments", size=20, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            expand=True,
                                            content=self.Comments
                                        ),
                                    ]
                                ),
                            ),
                        ft.Column(
                            controls=[
                                ft.Text(value="Participants", weight=ft.FontWeight.BOLD, size=20),
                                ft.Divider(color=ft.Colors.BLACK),
                                ft.Container(
                                    expand=True,
                                    width=150,
                                    content=self.participants
                                ),
                            ]
                        )
                    ]
                )
        
        self.displayEvent()
        
    def displayEvent(self):
        url = "http://127.0.0.1:8000/community-service/show-listing"
        
        with httpx.Client() as client:
            with open("Backend/session.json", "r") as file:
                eventid = json.load(file)
                
            response = client.get(url, params={"EventId": eventid["event_id"]})
            
            if response.status_code == 200:
                data = response.json()
                
                if "event" in data:
                    event = data["event"][0]
                    
                    self.publisher[1].controls[0].value = event["publisher"]
                    self.publisher[1].controls[1].value = event["publishedSince"]
                    self.eventTitle.controls[0].value = event["title"]
                    self.eventTitle.controls[1].value = event["venue"]
                    self.eventDescription.value = event["description"]
                    
                    self.page.update()
                    
    def joinEvent(self, e):
        url = "http://127.0.0.1:8000/BookmarkedServices/save-userevent"
        
        with open("Backend/session.json", "r") as file:
            session_data = json.load(file)
            
        with httpx.Client() as client:
            response = client.post(url, params={"UserId": session_data["user_id"], "EventId": session_data["event_id"]})                           
    
class Page(Page.View):
    def __init__(self, page):
        super().__init__(page)
        
        self.Row.controls.append(EventUI(page))
        self.route = "/Dashboard"