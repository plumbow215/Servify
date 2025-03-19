from flet import *
from UIComponents import *
import Backend.session as session
import sqlite3, datetime, json

class SRSearchBar(Card):
     def __init__(self, page):
        super().__init__()
        
        self.width=page.width
        self.height=80
        self.elevation = 8
        
        self.content=Row(
            controls=[
                Container(
                    bgcolor=Colors.GREEN_700,
                    height=80,
                    padding=10,
                    border_radius=10,
                    content=Row(
                        controls=[
                            Icon(name=Icons.SEARCH, color=Colors.BLACK),
                            SearchBar(
                                bar_bgcolor=Colors.GREEN_600,
                            ),
                            Container(
                                bgcolor=Colors.GREEN_600,
                                border_radius=10,
                                content=SubmenuButton(
                                    content=Row(
                                        controls=[
                                            Text("Filters"),
                                            Icon(Icons.ARROW_DROP_UP)
                                        ]
                                    ),
                                    controls=[
                                        MenuItemButton(content=Text("Finished"), leading=Icon(Icons.CHECKLIST)),
                                        MenuItemButton(content=Text("Ongoing"), leading=Icon(Icons.UPDATE)),
                                        MenuItemButton(content=Text("Date Created"), leading=Icon(Icons.DATE_RANGE))
                                    ]
                                ),
                            )
                        ]
                        
                    )
                )
            ]    
        )

class Categories(Card):
    def __init__(self, page):
        super().__init__()
        
        maxHeight = 50
        self.color = Colors.GREEN_500
        
        self.expand = True
        self.elevation = 15
        self.shadow_color = colors.BLACK
        self.height = maxHeight
        self.width = page.width
        
        self.content=Row(
            alignment=MainAxisAlignment.SPACE_EVENLY,
            controls=[
                Text("Date & Time", size=15, weight=FontWeight.BOLD),
                Text("Venue", size=15, weight=FontWeight.BOLD),
                Text("Volunteered on", size=15, weight=FontWeight.BOLD),
                Text("Published on", size=15, weight=FontWeight.BOLD),
                Text("Creator", size=15, weight=FontWeight.BOLD),
            ]
        )
        
class SRListing(Card):
    def __init__(self, page, Timeline, Venue, volunteeredDate, publishedDate, Publisher):
        super().__init__()
        
        maxHeight = 80
        self.color = Colors.GREEN_400
        
        self.expand = True
        self.elevation = 15
        self.shadow_color = colors.BLACK
        self.height = maxHeight
        self.width = page.width
        
        self.content=Row(
            alignment=MainAxisAlignment.SPACE_EVENLY,
            controls=[
                Text(Timeline, size=15, weight=FontWeight.BOLD),
                Text(Venue, size=15, weight=FontWeight.BOLD),
                Text(volunteeredDate, size=15, weight=FontWeight.BOLD),
                Text(publishedDate, size=15, weight=FontWeight.BOLD),
                Text(Publisher, size=15, weight=FontWeight.BOLD),
            ]
        )

class ServiceRecords(Row):
    def __init__(self, page):
        super().__init__()
        
        self.page = page
        self.expand=True,
        self.alignment=alignment.center,
        self.spacing = 10,
        
        self.Column = Column()
        self.controls=[
                # main
                Container(
                    expand=True,
                    margin=0,
                    padding=10,
                    width=980,
                    height=page.height,
                    bgcolor=Colors.GREEN_600,
                    border_radius=20, 
                                    
                    # column
                    content=Column(
                        expand=True,
                        scroll=True,
                        spacing=5,
                        controls=[
                            #Title
                            Container(
                                margin=margin.only(left=5),
                                content=Row(
                                    controls=[
                                        Text("My Service Records", weight=FontWeight.BOLD, size=30),
                                        Container(
                                            expand=1
                                        ),
                                        ]
                                    )
                                ),
                            
                            #Events
                            SRSearchBar(page),
                            Categories(page),
                            self.Column
                        ]
                    )
                )
        ]
        
        self.loadServices(page)
    
    def loadServices(self, page):
        with open("Backend/session.json", "r") as f:
            session_data = json.load(f)

        user_id = session_data["user_id"]
        
        conn = sqlite3.connect("Servify.db")  # Adjust the path if needed
        cursor = conn.cursor()

        cursor.execute("""
            SELECT EventId FROM USEREVENTS WHERE UserId = ?
        """, (user_id,))
        
        events = cursor.fetchall()

        collected_events = []
        for eventid in events:
            cursor.execute("""
                SELECT venue, publishedSince, publisher FROM EVENTS WHERE EventId = ?
            """, (eventid[0],))
            event = cursor.fetchone()
            collected_events.append(event)
            
        for event in collected_events:
            venue, publishedSince, publisher = event
            
            element = SRListing(page, datetime.datetime.now().strftime("%I%M:%S"), venue, datetime.datetime.now().strftime("%d %b %Y"), publishedSince, publisher)
            self.Column.controls.append(element)
            
        self.page.update()

# When you click on the My Service Records button, it shows the Service Records Page
class Page(Page.View):
    def __init__(self, page):
        super().__init__(page)
        
        self.Row.controls.append(ServiceRecords(page))
        self.route = "/Dashboard"