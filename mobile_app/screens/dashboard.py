import flet as ft
from screens.navbar import NavBar

def DashboardScreen(page, api, state, navigate):
    user = state.get("user", {})
    bookings = api.get_bookings()

    def logout(e):
        state["user"] = None
        api.token = None
        navigate("home")

    def status_color(status):
        colors = {
            "PENDING": "#745804",
            "CONFIRMED": "#155724",
            "IN_PROGRESS": "#0c5460",
            "COMPLETED": "#28A745",
            "CANCELLED": "#DC3545",
        }
        return colors.get(status.upper(), "#666666")

    def status_bg(status):
        bgs = {
            "PENDING": "#F8DB84",
            "CONFIRMED": "#D4EDDA",
            "IN_PROGRESS": "#D1ECF1",
            "COMPLETED": "#C3E6CB",
            "CANCELLED": "#F8D7DA",
        }
        return bgs.get(status.upper(), "#F8F9FA")

    def booking_card(b):
        s = b.get("status", "pending").upper()
        border_color = "#FFE597" if s == "PENDING" else "#333355"
        vehicle = b.get("vehicle", {})
        vehicle_str = (
            f"{vehicle.get('make', '')} {vehicle.get('model', '')} "
            f"({vehicle.get('year', '')})"
        ) if vehicle else "N/A"

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Text("🔧", size=22),
                        bgcolor="#2A2A4A",
                        border_radius=25,
                        padding=8,
                        width=42,
                        height=42,
                    ),
                    ft.Column([
                        ft.Text(b.get("service_name", "Service"),
                                size=15, weight=ft.FontWeight.BOLD,
                                color="white"),
                        ft.Text(vehicle_str, size=11, color="#AAAAAA"),
                        ft.Text(str(b.get("booking_date", ""))[:10],
                                size=11, color="#888888"),
                    ], expand=True, spacing=2),
                    ft.Container(
                        content=ft.Text(s, size=10,
                                        color=status_color(s),
                                        weight=ft.FontWeight.BOLD),
                        bgcolor=status_bg(s),
                        border_radius=20,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    ),
                ], spacing=12),
            ]),
            bgcolor="#16213E",
            border_radius=12,
            padding=16,
            margin=ft.margin.symmetric(horizontal=16, vertical=4),
            border=ft.border.all(1, border_color),
        )

    booking_controls = []
    if bookings:
        for b in bookings:
            booking_controls.append(booking_card(b))
    else:
        booking_controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("📋", size=40, text_align=ft.TextAlign.CENTER),
                    ft.Text("No bookings yet", size=14, color="#AAAAAA",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Book a service to get started!",
                            size=12, color="#666666",
                            text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=30,
            )
        )

    page.add(
        # Hero banner
        ft.Container(
        content=ft.Column([
            ft.Text("👤", size=50, text_align=ft.TextAlign.CENTER),
            ft.Text(
                f"Welcome, {user.get('first_name', 'User')}!",
                size=24, weight=ft.FontWeight.BOLD,
                color="white", text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=3, bgcolor="#FFE597", border_radius=2, width=60),
            ft.Container(height=4),
            ft.Text(
                user.get("email", ""),
                size=13,
                color="#AAAAAA",
                text_align=ft.TextAlign.CENTER
            ),
            # ✅ NEW BUTTON (shortcut)
            ft.Container(height=8),
            ft.Button(
                "🔧 Book a Service",
                on_click=lambda e: navigate("services"),
                width=220,
                style=ft.ButtonStyle(
                    bgcolor="#FFE597",
                    color="#000000",
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
            ),

    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            bgcolor="#1A1A2E",
            padding=ft.padding.symmetric(vertical=30, horizontal=16),
        ),

        # Account info card
        ft.Container(
            content=ft.Column([
                ft.Text("Account Info", size=16, weight=ft.FontWeight.BOLD,
                        color="white", text_align=ft.TextAlign.CENTER),
                ft.Container(height=3, bgcolor="#FFE597", border_radius=2, width=50),
                ft.Container(height=8),
                ft.Container(
                    content=ft.Row([
                        ft.Text("👤", size=16),
                        ft.Text("Name", size=13, color="#AAAAAA", expand=True),
                        ft.Text(
                            f"{user.get('first_name', '')} {user.get('last_name', '')}",
                            size=13, color="white", weight=ft.FontWeight.BOLD,
                        ),
                    ], spacing=8),
                    bgcolor="#2A2A4A", border_radius=8, padding=12,
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Text("✉️", size=16),
                        ft.Text("Email", size=13, color="#AAAAAA", expand=True),
                        ft.Text(user.get("email", ""), size=13,
                                color="white", weight=ft.FontWeight.BOLD),
                    ], spacing=8),
                    bgcolor="#2A2A4A", border_radius=8, padding=12,
                ),
                ft.Container(height=8),
                ft.ElevatedButton(
                    "🚪  Logout",
                    on_click=logout,
                    width=280,
                    style=ft.ButtonStyle(
                        bgcolor="#DC3545", color="white",
                        shape=ft.RoundedRectangleBorder(radius=25),
                    ),
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            bgcolor="#16213E",
            border_radius=12,
            padding=20,
            margin=ft.margin.symmetric(horizontal=16, vertical=12),
            border=ft.border.all(1, "#333355"),
        ),

        # My Bookings title
        ft.Container(
            content=ft.Column([
                ft.Text("My Bookings", size=20, weight=ft.FontWeight.BOLD,
                        color="#1A1A2E", text_align=ft.TextAlign.CENTER),
                ft.Container(height=3, bgcolor="#FFE597", border_radius=2, width=60),
                ft.Text(f"{len(bookings)} booking(s) found",
                        size=12, color="#888888",
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            padding=ft.padding.symmetric(vertical=16, horizontal=16),
        ),

        *booking_controls,

        ft.Container(height=8),
        ft.Container(
            content=ft.Row(
                [
                    ft.ElevatedButton(
                        "🔧  Book a New Service",
                        on_click=lambda e: navigate("services"),
                        width=280,
                        style=ft.ButtonStyle(
                            bgcolor="#FFE597", color="#000000",
                            shape=ft.RoundedRectangleBorder(radius=25),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=16),
        ),
        ft.Container(height=16),
        NavBar(page, navigate, active="login"),
    )