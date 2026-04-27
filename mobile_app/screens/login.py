import flet as ft
from screens.navbar import NavBar

def LoginScreen(page, api, state, navigate):
    email_field = ft.TextField(
        label="Email Address",
        keyboard_type=ft.KeyboardType.EMAIL,
        bgcolor="white",
        border_color="#FFE597",
        focused_border_color="#FFE597",
        label_style=ft.TextStyle(color="#313131"),
        width=320,
    )
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        bgcolor="white",
        border_color="#FFE597",
        focused_border_color="#FFE597",
        label_style=ft.TextStyle(color="#313131"),
        width=320,
    )
    error_text = ft.Text("", color="#FF6B6B", size=13,
                         text_align=ft.TextAlign.CENTER)

    def handle_login(e):
        result = api.login(email_field.value, password_field.value)
        if result:
            state["user"] = result
            navigate("dashboard")  # ← changed from "home" to "dashboard"
        else:
            error_text.value = "Invalid email or password. Please try again."
            page.update()

    page.add(
        # Hero banner
        ft.Container(
            content=ft.Column([
                ft.Text("👤", size=50, text_align=ft.TextAlign.CENTER),
                ft.Text("Welcome Back", size=26, weight=ft.FontWeight.BOLD,
                        color="white", text_align=ft.TextAlign.CENTER),
                ft.Container(height=3, bgcolor="#FFE597", border_radius=2, width=60),
                ft.Container(height=6),
                ft.Text("Login to access your bookings\nand manage your vehicles",
                        size=13, color="#AAAAAA", text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            bgcolor="#1A1A2E",
            padding=ft.padding.symmetric(vertical=30, horizontal=16),
        ),

        # Login form card
        ft.Container(
            content=ft.Column([
                ft.Container(height=8),
                email_field,
                ft.Container(height=8),
                password_field,
                ft.Container(height=8),
                error_text,
                ft.Container(height=12),
                ft.ElevatedButton(
                    "Login",
                    on_click=handle_login,
                    width=320,
                    style=ft.ButtonStyle(
                        bgcolor="#FFE597", color="#000000",
                        shape=ft.RoundedRectangleBorder(radius=25),
                    ),
                ),
                ft.Container(height=20),
                ft.Divider(color="#E9ECEF"),
                ft.Container(height=12),
                ft.Text("Don't have an account?", size=13,
                        color="#666666", text_align=ft.TextAlign.CENTER),
                ft.Container(height=4),
                ft.TextButton(
                    "Book a service to create one",
                    on_click=lambda e: navigate("services"),
                    style=ft.ButtonStyle(color="#FFB800"),
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            bgcolor="white",
            border_radius=16,
            padding=24,
            margin=ft.margin.symmetric(horizontal=16, vertical=16),
            border=ft.border.only(top=ft.BorderSide(4, "#1A1A2E")),
        ),

        NavBar(page, navigate, active="login"),
    )