from flet import *
from Components import IconText

class UI(Container):
    def __init__(self, page):
        super().__init__()
        
        self.padding=padding.only(top=30, left=30,right=30)
        self.alignment=alignment.center
        self.width=250
        self.height=page.height
        self.bgcolor=Colors.GREY_900
        self.border_radius=20
        self.content=(
                Column(
                    controls=[
                        IconText.createIconWithText(Icons.PERSON, "Profile", lambda _: page.go('/Dashboard/Profile')) , 
                        Divider(),
                        IconText.createIconWithText(Icons.DASHBOARD, "Dashboard", lambda _: page.go('/Dashboard')),
                        IconText.createIconWithText(Icons.FORMAT_LIST_BULLETED, "My Service Records", lambda _: page.go('/Dashboard/ServiceRecords')),
                        Divider(),
                        IconText.createIconWithText(Icons.LOGOUT, "Log Out", lambda _: page.go('/'))
                    ]
                )
            )
    