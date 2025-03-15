from flet import *

class CSListing(Card): 
    def __init__(self, pageWidth : int, Publisher : str, publishedSince : str, Title : str, Description : str):
        super().__init__()
        
        maxHeight = 300
        containerBGColor = Colors.GREEN
        textColor = Colors.WHITE
        
        self.expand = True
        self.elevation = 15 
        self.shadow_color = colors.BLACK
        self.height = maxHeight
        self.width = pageWidth
        
        self.content=Container(
            bgcolor=containerBGColor,
            border_radius=10,
            height=maxHeight,
            width=pageWidth,
            
            content=Column(
                expand=True,
                spacing=10,
                controls=[
                    #title (task title)
                    Container(
                        margin=margin.only(top=20, left=30),
                        alignment=alignment.center_left,
                        bgcolor=containerBGColor,
                        content=Text(Title, size=30, weight=FontWeight.BOLD)
                    ),
                    
                    #information (user profile, username, published since when)
                    Container(
                        margin=margin.only(left=30),
                        content=Row(
                            controls=[
                                Icon(name=Icons.PERSON, color=Colors.BLACK, size=50),
                                Column(
                                    spacing=2,
                                    controls=[
                                        Text(Publisher, size=20, weight=FontWeight.BOLD),
                                        Text(publishedSince, size=10, color=colors.BLACK38)
                                    ]
                                )
                                
                            ]
                        )
                        
                        ),
                    
                    #body (task information)
                    Container(
                        width=500,
                        margin=margin.only(left=30),
                        alignment=alignment.center_left,
                        bgcolor=containerBGColor,
                        content=Text(Description, size=10)
                    ),
                    
                    #buttons
                    Container(
                        margin=margin.only(left=30),
                        content=Row(
                            spacing=5,
                            controls=[
                                TextButton (
                                    style=ButtonStyle(shape=RoundedRectangleBorder(radius=10), bgcolor=Colors.GREEN_600),
                                    content=Container(content=Icon(name=Icons.BOOKMARK, color=Colors.BLACK12))
                                ),
                                
                                TextButton(
                                    style=ButtonStyle(shape=RoundedRectangleBorder(radius=10), bgcolor=Colors.GREEN_600),
                                    content=Row(
                                        controls=[
                                            Container(content=Icon(name=Icons.CHAT, color=Colors.BLACK12)),
                                            Text("Add Response", color=Colors.BLACK)
                                        ]
                                    )
                                ),
                                
                                
                            ]
                        ),
                    )
                ]
                )
        )
        
