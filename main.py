from flet import *
from Pages import *


def main(page: Page) -> None:
    page.title = "Servify"
    page.bgcolor = Colors.BLACK
    page.window.min_height = 700
    page.window.min_width = 1080
        
    page.appbar = AppBar(
        bgcolor=Colors.BLACK,
        title=Text("Servify", color=Colors.WHITE, weight=FontWeight.BOLD, size=35),
    )
    
    loginUI = Container(
            expand=True,
            width=page.width,
            height=page.height,
            bgcolor=Colors.BLACK12,
            alignment=Alignment(0,-.35),
            content=Login.Login(page)
        )
    
    def routeChange(e) -> None:
        page.views.clear()
        
        #Dashboard
        if page.route == "/Dashboard/ServiceRecords":
            page.views.append(
                ServiceRecords.Page(page)
            )
        
        if page.route == "/Dashboard/Profile":
            page.views.append(
                Profile.Page(page)
            )
        
        if page.route == "/Dashboard":
            page.views.append(
                Dashboard.Page(page)
            )
        
        if page.route == "/":
            page.views.append(
                Login.Page(page)
            )
            
        
        page.update()
    
    page.add(
        loginUI
    )
    
    page.on_route_change = routeChange
    
if __name__ == '__main__':
    app(target=main)