from flet import *

def createIconWithText(iconName : str, Label : str, function=None):
    return Container(
        width=200,
        height=45,
        on_hover=None,
        on_click=function,
        content=Row(
            controls=[
                Icon(name=iconName, color=Colors.GREY),
                Text(Label, color=Colors.GREY)
            ]
        )
    )