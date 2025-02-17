import flet as ft
    
class Handout(ft.Card):
    def __init__(self, pageWidth : int, Publisher : str, publishedSince : str, Title : str, Description : str):
        super().__init__()
        
        maxHeight = 300
        containerBGColor = ft.Colors.GREEN
        textColor = ft.Colors.WHITE
        
        self.expand = True
        self.elevation = 15
        self.shadow_color = ft.colors.BLACK
        self.height = maxHeight
        self.width = pageWidth
        
        self.content=ft.Container(
            bgcolor=containerBGColor,
            border_radius=10,
            height=maxHeight,
            width=pageWidth,
            
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
                                ft.TextButton (
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.GREEN_600),
                                    content=ft.Container(content=ft.Icon(name=ft.Icons.BOOKMARK, color=ft.Colors.BLACK12))
                                ),
                                
                                ft.TextButton(
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.GREEN_600),
                                    content=ft.Row(
                                        controls=[
                                            ft.Container(content=ft.Icon(name=ft.Icons.CHAT, color=ft.Colors.BLACK12)),
                                            ft.Text("Add Response", color=ft.Colors.BLACK)
                                        ]
                                    )
                                ),
                                
                                
                            ]
                        ),
                    )
                ]
                )
        )

def createIcon(iconName : str, Label : str):
    return ft.Container(
        width=200,
        height=45,
        on_hover=None,
        content=ft.Row(
            controls=[
                ft.Icon(name=iconName, color=ft.Colors.GREY),
                ft.Text(Label, color=ft.Colors.GREY)
            ]
        )
        
    )
        
def main(page: ft.Page):
    page.title = "Servify"
    page.padding = 10
    page.bgcolor = ft.Colors.BLACK
    page.window.min_height = 700
    page.window.min_width = 1080
        
        
    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.BLACK,
        title=ft.Text("Servify", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=35),
    )
    
    page.add(
        ft.Row(
            expand=True,
            alignment=ft.alignment.center,
            spacing = 10,
            controls=[
                # sidebar
                ft.Container(
                    padding=ft.padding.only(top=30, left=30,right=30),
                    alignment=ft.alignment.center,
                    width=250,
                    height=page.height,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=20,
                    content=ft.Column(
                        controls=[
                            createIcon(ft.Icons.PERSON, "Profile") , 
                            ft.Divider(),
                            createIcon(ft.Icons.DASHBOARD, "Dashboard"),
                            createIcon(ft.Icons.FORMAT_LIST_BULLETED, "My Events"),
                            ft.Divider(),
                            createIcon(ft.Icons.LOGOUT, "Log Out")
                        ]
                    )
                ),
                
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
                    content=ft.Column(
                        expand=True,
                        scroll=True,
                        spacing=5,
                        controls=[
                            #Title
                            ft.Container(
                                margin=ft.margin.only(left=5),
                                content=ft.Row(
                                    controls=[
                                        ft.Text("Event Listings", weight=ft.FontWeight.BOLD, size=30),
                                        ft.Container(
                                            expand=1
                                        ),
                                        ft.TextButton(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(name=ft.Icons.ADD, color=ft.colors.BLACK),
                                                    ft.Text(value="Create New Entry", color=ft.colors.BLACK)
                                                ]
                                            )
                                        )
                                        ]
                                    )
                                ),
                            
                            #Events
                            Handout(page.width, "Ethan Guardian", "8h ago", "Lecture Rescheduling", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                            Handout(page.width, "Ethan Guardian", "5h ago", "Lecture Rescheduling", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                            Handout(page.width, "Ethan Guardian", "2h ago","Lecture Rescheduling", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                            Handout(page.width, "Ethan Guardian", "5m ago","Lecture Rescheduling", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
                        ]
                    )
                ),
            ]
        )
    )
    
if __name__ == '__main__':
    ft.app(target=main)