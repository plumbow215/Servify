from flet import *
from UIComponents import *
    
class Dashboard(Row):
    def __init__(self, pageHeight : int, pageWidth : int):
        super().__init__()
        
        self.expand=True,
        self.alignment=alignment.center,
        self.spacing = 10,
        
        self.controls=[
                # main
                Container(
                    expand=True,
                    margin=0,
                    padding=10,
                    width=980,
                    height=pageHeight,
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
                                        Text("Community Service Listings", weight=FontWeight.BOLD, size=30),
                                        Container(
                                            expand=1
                                        ),
                                        TextButton(
                                            content=Row(
                                                controls=[
                                                    Icon(name=Icons.ADD, color=colors.BLACK),
                                                    Text(value="Create New Entry", color=colors.BLACK)
                                                ]
                                            )
                                        )
                                        ]
                                    )
                                ),
                            
                            #Events
                            Handout.CSListing(pageWidth, "Ethan Guardian", "8h ago", "Lecture Rescheduling", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                            Handout.CSListing(pageWidth, "Ethan Guardian", "5h ago", "Lecture Rescheduling", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                            Handout.CSListing(pageWidth, "Ethan Guardian", "2h ago","Lecture Rescheduling", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                            Handout.CSListing(pageWidth, "Ethan Guardian", "5m ago","Lecture Rescheduling", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
                        ]
                    )
                )
        ]
        
class Page(View):
    def __init__(self, page):
        super().__init__()
        
        self.bgcolor = Colors.BLACK
        self.route="/Dashboard",
        self.controls=[
            AppBar(
                bgcolor=Colors.BLACK,
                title=Text("Servify", color=Colors.WHITE, weight=FontWeight.BOLD, size=35),
            ),
            Container(
                bgcolor=Colors.BLACK,
                expand=True,
                width=page.width,
                height=page.height,
                alignment=alignment.center,
                content=(
                    Row(
                        expand=True,
                        width=page.window.width,
                        height=page.window.height,
                        controls=[
                            Sidebar.UI(page),
                            Dashboard(page.height, page.width)
                        ]
                    )
                )
            )
        ]
                
        
