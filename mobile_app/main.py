import flet as ft
from screens.home import HomeScreen
from screens.services import ServicesScreen
from screens.booking import BookingScreen
from screens.login import LoginScreen
from screens.contact import ContactScreen
from screens.dashboard import DashboardScreen
from api.client import APIClient

api = APIClient()

def main(page: ft.Page):
    page.title = "Depann Mo Loto"
    page.padding = 0
    page.bgcolor = "#F8F9FA"
    page.scroll = "auto"

    state = {"user": None, "selected_service": None}

    def navigate(screen_name, **kwargs):
        page.controls.clear()
        if screen_name == "home":
            HomeScreen(page, api, state, navigate)
        elif screen_name == "services":
            ServicesScreen(page, api, state, navigate)
        elif screen_name == "booking":
            BookingScreen(page, api, state, navigate)
        elif screen_name == "login":
            if state.get("user"):
                DashboardScreen(page, api, state, navigate)
            else:
                LoginScreen(page, api, state, navigate)
        elif screen_name == "dashboard":
            DashboardScreen(page, api, state, navigate)
        elif screen_name == "contact":
            ContactScreen(page, api, state, navigate)
        page.update()

    navigate("home")

ft.app(target=main, view="web_browser")