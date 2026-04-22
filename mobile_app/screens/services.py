import flet as ft
from screens.navbar import NavBar

def ServicesScreen(page, api, state, navigate):

    # Fetch real services from API
    api_services = api.get_services()

    # Emoji map for display
    emoji_map = {
        "Car Servicing": "🔧",
        "Mechanical Repair": "⚙️",
        "Battery Check": "🔋",
        "Tyre Replacement": "🛞",
        "AC Service": "❄️",
        "Preventive Maintenance": "🎯",
    }

    # Fallback if API fails
    fallback = [
        {"id": 1, "name": "Car Servicing", "description": "Complete maintenance, oil changes, filter replacements and inspections.", "price": "2500"},
        {"id": 2, "name": "Mechanical Repair", "description": "Expert diagnostic and repair for engine problems and mechanical components.", "price": "1500"},
        {"id": 3, "name": "Battery Check", "description": "Comprehensive battery testing and replacement services.", "price": "800"},
        {"id": 4, "name": "Tyre Replacement", "description": "Professional tyre installation, balancing, and alignment services.", "price": "3000"},
        {"id": 5, "name": "AC Service", "description": "Air conditioning diagnostics, cleaning, repair and gas refilling.", "price": "1200"},
        {"id": 6, "name": "Preventive Maintenance", "description": "Regular servicing to prevent breakdowns and keep your vehicle healthy.", "price": "3000"},
    ]

    services_data = api_services if api_services else fallback

    def book_now(service):
        state["selected_service"] = service
        navigate("booking")

    def service_card(s):
        emoji = emoji_map.get(s.get("name", ""), "🔧")
        price = s.get("price", "")
        display_price = f"From Rs {price}" if price else ""

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Text(emoji, size=28,
                                       text_align=ft.TextAlign.CENTER),
                        bgcolor="#2A2A4A",
                        border_radius=30,
                        padding=10,
                        width=55,
                        height=55,
                    ),
                    ft.Column([
                        ft.Text(s.get("name", ""), size=16,
                                weight=ft.FontWeight.BOLD, color="#1A1A2E"),
                        ft.Text(display_price, size=14,
                                weight=ft.FontWeight.BOLD, color="#FFB800"),
                    ], spacing=4, expand=True),
                ], spacing=12),
                ft.Container(height=8),
                ft.Text(s.get("description", s.get("desc", "")),
                        size=12, color="#666666"),
                ft.Container(height=12),
                ft.ElevatedButton(
                    "Book Now",
                    on_click=lambda e, svc=s: book_now(svc),
                    style=ft.ButtonStyle(
                        bgcolor="#FFE597", color="#000000",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    width=320,
                ),
            ]),
            bgcolor="white",
            border_radius=12,
            padding=20,
            margin=ft.margin.symmetric(horizontal=16, vertical=6),
            border=ft.border.only(
                left=ft.BorderSide(4, "#1A1A2E"),
                top=ft.BorderSide(1, "#E9ECEF"),
                right=ft.BorderSide(1, "#E9ECEF"),
                bottom=ft.BorderSide(1, "#E9ECEF"),
            ),
        )

    # Hero banner
    hero = ft.Container(
        content=ft.Column([
            ft.Text("Our Services", size=26, weight=ft.FontWeight.BOLD,
                    color="white", text_align=ft.TextAlign.CENTER),
            ft.Container(height=3, bgcolor="#FFE597", border_radius=2, width=60),
            ft.Container(height=6),
            ft.Text("Professional automotive solutions across Mauritius.",
                    size=13, color="#AAAAAA", text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
        bgcolor="#1A1A2E",
        padding=ft.padding.symmetric(vertical=30, horizontal=16),
    )

    def feature_item(emoji, label):
        return ft.Container(
            content=ft.Column([
                ft.Text(emoji, size=32, text_align=ft.TextAlign.CENTER),
                ft.Container(height=6),
                ft.Text(label, size=12, text_align=ft.TextAlign.CENTER,
                        color="white", weight=ft.FontWeight.BOLD),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            bgcolor="#2A2A4A",
            border_radius=12,
            padding=16,
            width=100,
            height=110,
            border=ft.border.all(1, "#FFE597"),
        )

    why_us = ft.Container(
        content=ft.Column([
            ft.Text("Why Choose Our Services?",
                    size=22, weight=ft.FontWeight.BOLD, color="#FFE597",
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=3, bgcolor="#FFE597", border_radius=2, width=60),
            ft.Container(height=16),
            ft.Row([
                feature_item("✅", "Certified\nTechnicians"),
                feature_item("⚡", "Quick\nService"),
                feature_item("🏆", "Quality\nGuarantee"),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#1A1A2E",
        padding=24,
        margin=ft.margin.symmetric(horizontal=16, vertical=8),
        border_radius=12,
    )

    page.add(
        hero,
        ft.Container(height=8),
        *[service_card(s) for s in services_data],
        ft.Container(height=8),
        why_us,
        ft.Container(height=16),
        NavBar(page, navigate, active="services"),
    )