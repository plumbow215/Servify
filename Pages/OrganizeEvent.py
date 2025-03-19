import flet as ft
import httpx, json, datetime
import UIComponents.Sidebar as Sidebar
import UIComponents.GreenBackground as GreenBackground
import UIComponents.IconText as IconText
import UIComponents.Handout as Handout
import Misc.interests as interests
import Misc.skills as skills
import UIComponents.Page as Page

class Theme(ft.ElevatedButton):
    def __init__(self, page: ft.Page, themeName : str, onThemeChanged):
        super().__init__()

        self.width = 250
        self.style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_800, shape=ft.RoundedRectangleBorder(radius=0))
        self.content=ft.Text(themeName, color=ft.Colors.BLACK)
        self.on_click = lambda e: onThemeChanged(themeName)

class OrganizeEventUI(ft.Container):
    def __init__(self, page):
        super().__init__()
        
        self.title = "Placeholder"
        self.venue ="Placeholder"
        self.description = "Placeholder"
        self.date = "1 Jan 2025"
        self.maxParticipants = 0
        
        self.selected_skills = []
        self.selected_theme = None
        self.eventTheme = ft.Text(value="Event theme: None", weight=ft.FontWeight.BOLD)
        self.skills_text = ft.Text(value="Skills needed: None", weight=ft.FontWeight.BOLD)
        
        self.page = page
        self.width = 980
        greenBackground = GreenBackground.getBackground(page)
        self.content = greenBackground
        
        #participants
        self.participants = ft.ListView()
        
        #publisher
        self.publisher = [
            ft.CircleAvatar(
                width=50,
                height=50,
                content=ft.Text("FF", color=ft.Colors.ORANGE)
                ),
            ft.Column(
                controls=[
                    ft.Text(value="User", weight=ft.FontWeight.BOLD, size=20),
                    ft.Text(value="Published x time ago", size=12)
                ]
                ),
        ]
        
        #title
        self.eventTitle = ft.Column(
            controls=[
                ft.TextField(label="Title", hint_text=self.title, text_size=25, on_change=self.onTextFieldChanged),
                ft.TextField(label="Venue", hint_text=self.venue, text_size=15, on_change=self.onTextFieldChanged)
            ]
        )
        
        #description
        self.eventDescription = ft.TextField(label="Description", hint_text=self.venue, text_size=15, on_change=self.onTextFieldChanged )
        
        self.maxParticipantsButton = ft.TextField(
            label="Max Participants", hint_text="No. of Participants", text_size=15, on_change=self.onTextFieldChanged, width=200
        )
        
        current_year = datetime.datetime.now().year
        self.datePicker = ft.DatePicker(
                    first_date=datetime.datetime(year=current_year, month=1, day=1),
                    last_date=datetime.datetime(year=current_year+1, month=12, day=31),
                    on_change=self.onDateChanged
                )
        
        self.pickDate = ft.ElevatedButton(
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.GREEN_700),
            content=ft.Text("Pick Date", color=ft.Colors.BLACK),  
            on_click=lambda e: page.open(
                self.datePicker
            )
        )
        
        #edit purpose buttons
        self.createEvent = ft.Container(
            border_radius=10,
            bgcolor=ft.Colors.BLACK,
            width=100,
            height=40,
            alignment=ft.alignment.center,
            content=ft.Text("Create Event", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            on_click=self.onCreateEvent
        )
        
        
        
        self.setTheme = ft.SubmenuButton(
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.GREEN_700),
            content=ft.Text("Customize Event Theme"),
            controls=[
                Theme(page, interest, self.onThemeChanged) for interest in interests.interests
            ]
        )
        
        self.setSkills = ft.SubmenuButton(
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.GREEN_700),
            content=ft.Text("Add Skills", text_align=ft.TextAlign.CENTER),
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.GREEN_700,
                    width=250,
                    content=ft.Column(
                        controls=[
                            ft.ListView(
                                controls=[
                                    ft.Checkbox(label=skill, value = False, on_change=self.onCheckboxChanged) for skill in skills.skills  
                                ]
                            )
                        ]
                    )
                )
            ]
        )
        
        greenBackground.content=ft.Row(
                    controls=[
                        ft.Container(
                            width=800,
                            padding=20,
                            content=ft.Column(
                                    controls=[
                                        ft.Row(controls=self.publisher),
                                        self.eventTitle,
                                        self.eventDescription,
                                        self.eventTheme,
                                        self.skills_text,
                                        ft.Divider(color=ft.Colors.BLACK),
                                        ft.Row(controls=[self.maxParticipantsButton, self.pickDate,self.setSkills , self.setTheme, self.createEvent]),
                                    ]
                                ),
                            ),
                        ft.Column(
                            controls=[
                                ft.Text(value="Participants", weight=ft.FontWeight.BOLD, size=20),
                                ft.Divider(color=ft.Colors.BLACK),
                                ft.Container(
                                    expand=True,
                                    width=150,
                                    content=self.participants
                                ),
                            ]
                        )
                    ]
                )
    
    async def onCreateEvent(self, e):
        # Read data from JSON file
        with open("Backend/event_data.json", "r") as file:
            event_data = json.load(file)

        # Send HTTP request to FastAPI backend
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8000/community-service/create_event", json=event_data)

        if response.status_code == 200:
            print("Event successfully created!")
        else:
            print(f"Failed to create event: {response.text}")
    
    def saveToJson(self):
        data = {
            "title": self.title,
            "venue": self.venue,
            "description": self.description,
            "selected_skills": self.selected_skills,
            "selected_theme": self.selected_theme,
            "date": self.date,
            "maxParticipants": self.maxParticipants
        }
        
        with open("Backend/event_data.json", "w") as file:
            json.dump(data, file, indent=4)
    
    def onDateChanged(self, e):
        selected_date = e.control.value.strftime("%d %b %Y")
        self.date = selected_date
        self.saveToJson()  # Save to JSON file
        self.page.update()
        
    def onTextFieldChanged(self, e):
        if e.control.label == "Title":
            self.title = e.control.value
        elif e.control.label == "Venue":
            self.venue = e.control.value
        elif e.control.label == "Description":
            self.description = e.control.value
        elif e.control.label == "Max Participants":
            self.maxParticipants = int(e.control.value)
            
        self.saveToJson()
    
    def onThemeChanged(self, theme_name):
        self.selected_theme = theme_name
        self.eventTheme.value = f"Event theme: {self.selected_theme}"
        
        self.saveToJson()
        
        self.page.update()
        
    def onCheckboxChanged(self, e):
        checkbox = e.control
        skill = checkbox.label
        
        if checkbox.value:
            if skill not in self.selected_skills:
                self.selected_skills.append(skill)
        else:
            if skill in self.selected_skills:
                self.selected_skills.remove(skill)

        self.skills_text.value = f"Skills needed: {', '.join(self.selected_skills) if self.selected_skills else 'None'}"
        
        self.saveToJson()
        
        self.page.update()
                    
    
class Page(Page.View):
    def __init__(self, page):
        super().__init__(page)
        
        self.Row.controls.append(OrganizeEventUI(page))
        self.route = "/Organizer/Dashboard/OrganizeEvent"