import flet as ft

def NavBar(page, navigate, active="home"):
    def nav_btn(emoji, label, screen):
        is_active = active == screen
        return ft.TextButton(
            content=ft.Column(
                [
                    ft.Text(emoji, size=20, text_align=ft.TextAlign.CENTER),
                    ft.Text(label, size=10,
                            color="#FFE597" if is_active else "#888888",
                            weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            on_click=lambda e, s=screen: navigate(s),
        )

    return ft.Container(
        content=ft.Row(
            [
                nav_btn("🏠", "Home", "home"),
                nav_btn("🔧", "Services", "services"),
                nav_btn("👤", "Login", "login"),
                nav_btn("📍", "Contact", "contact"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor="#1A1A2E",
        padding=ft.padding.symmetric(vertical=8),
        border=ft.border.only(top=ft.BorderSide(1, "#333355")),
    )