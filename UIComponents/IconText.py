import flet as ft

def createIconWithText(iconName : str, Label : str, function=None):
    return ft.Container(
        width=200,
        height=45,
        on_hover=None,
        on_click=function,
        content=ft.Row(
            controls=[
                ft.Icon(name=iconName, color=ft.Colors.GREY),
                ft.Text(Label, color=ft.Colors.GREY)
            ]
        )
    )
    
def createProfileWithText(username : str):
    return ft.Container(
        width=200,
        height=45,
        content=ft.Row(
            controls=[
                ft.CircleAvatar(width=35,height=35,content=ft.Text(username[0].upper(), color=ft.Colors.ORANGE)),
                ft.Text(username, weight=ft.FontWeight.BOLD, size=17)
            ]
        )
    )
    
def createButtonWithIcon(icon : str, label : str):
    return ft.TextButton(
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.GREEN_600),
        content=ft.Row(
            controls=[
                ft.Icon(name=icon, color=ft.Colors.BLACK12),
                ft.Text(label, color=ft.Colors.BLACK)
            ]
        )
    ),