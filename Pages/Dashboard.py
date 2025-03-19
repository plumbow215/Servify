import flet as ft
import httpx, asyncio, tracemalloc
from UIComponents import *
tracemalloc.start()
    
class Dashboard(ft.Row):
    def __init__(self, page, load_events=True):
        super().__init__()
        
        self.page = page
        self.expand=True
        self.alignment=ft.alignment.center
        self.spacing = 10
        
        self.Title = ft.Container(
            margin=ft.margin.only(left=5),
            content=ft.Row(
                controls=[
                    ft.Text("Community Service Listings", weight=ft.FontWeight.BOLD, size=30),
                    ft.Container(
                        expand=1
                    ),
                    ]
                )
            )
        
        self.Column = ft.Column(
                        expand=True,
                        scroll=True,
                        spacing=5,
                        controls=[
                            #Title
                            self.Title
                        ]
        )
                        
        self.controls=[
                # main
                ft.Container(
                    expand=True,
                    margin=0,
                    padding=10,
                    width=980,
                    height=page.height,
                    bgcolor=ft.Colors.GREEN_600,
                    border_radius=20, 
                                    
                    # column
                    content=self.Column
                )
        ]
        
        if load_events:  # ✅ Prevent recursion when inherited
            self.LoadEvents()
    
    def LoadEvents(self):
        url = "http://127.0.0.1:8000/community-service/get-listings"

        with httpx.Client() as client:
            response = client.get(url)

            if response.status_code == 200:
                data = response.json()

                if "events" in data:
                    for event in data["events"]:
                        newHandout = Handout.CSListing(
                            self.page, event['EventId'], event['publisher'], 
                            event['publishedSince'], event['title'], event['description']
                        )
                        
                        self.Column.controls.append(newHandout)
                        
                    self.page.update()
        
class Page(Page.View):
    def __init__(self, page):
        super().__init__(page)
        
        self.Row.controls.append(Dashboard(page))
        self.route = "/Dashboard"
                
        
