import flet as ft
import UIComponents.IconText as IconText
import httpx, json

class CSListing(ft.Card): 
    def __init__(self, page, EventId : int, Publisher : str, publishedSince : str, Title : str, Description : str):
        super().__init__()
        
        self.EventId = EventId
        maxHeight = 300
        containerBGColor = ft.Colors.GREEN
        textColor = ft.Colors.WHITE
        
        self.expand = True
        self.elevation = 15 
        self.shadow_color = ft.colors.BLACK
        self.height = maxHeight
        self.width = page.width
        
        self.viewEvent = ft.TextButton(
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.GREEN_600),
            on_click=self.onClick,
            content=ft.Row(
                controls=[
                    ft.Container(content=ft.Icon(name=ft.Icons.SUBDIRECTORY_ARROW_RIGHT, color=ft.Colors.BLACK12)),
                    ft.Text("View Event", color=ft.Colors.BLACK)
                ]
            )
        )
        
        self.content=ft.Container(
            bgcolor=containerBGColor,
            border_radius=10,
            height=maxHeight,
            width=page.width,
            
            content=ft.Column(
                expand=True,
                spacing=10,
                controls=[
                    #title (task title)
                    ft.Container(
                        margin=ft.margin.only(top=20, left=30),
                        alignment=ft.alignment.center_left,
                        bgcolor=containerBGColor,
                        content=ft.Text(Title, size=30, weight=ft.FontWeight.BOLD)
                    ),
                    
                    #information (user profile, username, published since when)
                    ft.Container(
                        margin=ft.margin.only(left=30),
                        content=ft.Row(
                            controls=[
                                ft.Icon(name=ft.Icons.PERSON, color=ft.Colors.BLACK, size=50),
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(Publisher, size=20, weight=ft.FontWeight.BOLD),
                                        ft.Text(publishedSince, size=10, color=ft.colors.BLACK38)
                                    ]
                                )
                                
                            ]
                        )
                        
                        ),
                    
                    #body (task information)
                    ft.Container(
                        width=500,
                        margin=ft.margin.only(left=30),
                        alignment=ft.alignment.center_left,
                        bgcolor=containerBGColor,
                        content=ft.Text(Description, size=10)
                    ),
                    
                    #buttons
                    ft.Container(
                        margin=ft.margin.only(left=30),
                        content=ft.Row(
                            spacing=5,
                            controls=[
                                self.viewEvent
                            ]
                        ),
                    )
                ]
                )
        )
        
    async def onClick(self, e):
        self.page.go("/Dashboard/Event")
        
        with open("Backend/session.json", "r") as file:
            session_data = json.load(file)

        session_data["event_id"] = self.EventId
        
        with open("Backend/session.json", "w") as file:
            json.dump(session_data, file)
                    
                    
        
class UserComment(ft.Container):
    def __init__(self, username : str, comment : str):
        super().__init__()
        
        self.padding=10
        self.bgcolor=ft.Colors.GREEN_700
        self.border_radius=15
        self.User = IconText.createProfileWithText(username)
        self.Comment = ft.Text(comment)
        
        self.content=ft.Column(
            controls=[
                self.User,
                self.Comment
            ]
        )
