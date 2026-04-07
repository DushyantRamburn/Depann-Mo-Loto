import flet as ft
from screens.navbar import NavBar

def HomeScreen(page, api, state, navigate):

    def section_title(text):
        return ft.Container(
            content=ft.Text(text, size=20, weight=ft.FontWeight.BOLD, color="#333333",
                           text_align=ft.TextAlign.CENTER),
            padding=ft.padding.only(top=16, bottom=8),
            alignment=ft.alignment.center,
        )

    def service_preview_card(emoji, title, desc):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(emoji, size=28, text_align=ft.TextAlign.CENTER),
                    bgcolor="#FF8D8D",
                    border_radius=30,
                    padding=10,
                    width=55,
                    height=55,
                ),
                ft.Text(title, size=13, weight=ft.FontWeight.BOLD, color="#222222",
                        text_align=ft.TextAlign.CENTER),
                ft.Text(desc, size=11, color="#555555", text_align=ft.TextAlign.CENTER),
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="white",
            border_radius=12,
            padding=16,
            width=175,
            height=160,
            border=ft.border.all(2, "#E9ECEF"),
        )

    def location_card(address, branch):
        return ft.Container(
            content=ft.Column([
                ft.Text("📍", size=24),
                ft.Text(branch, size=12, weight=ft.FontWeight.BOLD, color="#333333"),
                ft.Text(address, size=11, color="#666666", text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
            bgcolor="white",
            border_radius=10,
            padding=16,
            border=ft.border.all(1, "#E9ECEF"),
            width=175,
        )

    # Combined banner + hero in one container
    combined_header = ft.Container(
        content=ft.Column([
            # Divider line at top for style
            ft.Container(
                height=4,
                bgcolor="#FFE597",
                border_radius=2,
                width=60,
            ),
            ft.Container(height=8),
            # Car emoji
            ft.Text("🚗", size=50, text_align=ft.TextAlign.CENTER),
            # Business name
            ft.Text(
                "Depann Mo Loto",
                size=30, weight=ft.FontWeight.BOLD,
                color="white", text_align=ft.TextAlign.CENTER,
            ),
            # Yellow divider under name
            ft.Container(
                height=3,
                bgcolor="#FFE597",
                border_radius=2,
                width=80,
            ),
            ft.Container(height=12),
            # Tagline
            ft.Text(
                "Professional Car Servicing\nand Maintenance",
                size=18, color="#DDDDDD",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Quality Service you can trust",
                size=13, color="#AAAAAA",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=20),
            # CTA Button
            ft.ElevatedButton(
                "🔧  Book Service Now",
                on_click=lambda e: navigate("services"),
                style=ft.ButtonStyle(
                    bgcolor="#FFE597", color="#000000",
                    shape=ft.RoundedRectangleBorder(radius=25),
                ),
                width=220,
            ),
            ft.Container(height=8),
            # Sub text
            ft.Text(
                "Trusted by thousands across Mauritius",
                size=11, color="#888888",
                text_align=ft.TextAlign.CENTER,
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
        bgcolor="#1A1A2E",
        padding=ft.padding.symmetric(horizontal=20, vertical=40),
    )

    services_row1 = ft.Row([
        service_preview_card("🔧", "Car Servicing", "Complete vehicle maintenance"),
        service_preview_card("🔋", "Battery Check", "Testing & replacement"),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=12)

    services_row2 = ft.Row([
        service_preview_card("⚙️", "Mechanical Repair", "Engine & component repairs"),
        service_preview_card("🛞", "Tyre Replacement", "Installation & balancing"),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=12)

    services_row3 = ft.Row([
        service_preview_card("❄️", "AC Service", "Diagnostics & gas refilling"),
        service_preview_card("🎯", "Preventive Maintenance", "Prevent breakdowns"),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=12)

    why_us = ft.Container(
        content=ft.Column([
            ft.Text("Why Choose Depann Mo Loto?",
                    size=18, weight=ft.FontWeight.BOLD,
                    color="white", text_align=ft.TextAlign.CENTER),
            ft.Container(height=8),
            ft.Text(
                "With years of experience in automotive repair and maintenance, "
                "we provide reliable, professional service to keep your vehicle running smoothly.",
                size=13, color="#CCCCCC", text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=12),
            ft.Row([
                ft.ElevatedButton(
                    "Contact Us",
                    on_click=lambda e: navigate("contact"),
                    style=ft.ButtonStyle(
                        bgcolor="#FFE597", color="#000000",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#1A1A2E",
        padding=24,
        margin=ft.margin.symmetric(horizontal=16, vertical=8),
        border_radius=12,
    )

    locations_row1 = ft.Row([
        location_card("21 Royal Road, Vacoas\n(+230) 5434 5678", "Vacoas Branch"),
        location_card("Jules Koenig, Port Louis\n(+230) 5345 6789", "Port Louis Branch"),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=12)

    locations_row2 = ft.Row([
        location_card("78 Central Flacq\n(+230) 5456 7890", "Flacq Branch"),
        location_card("12 Main Road, Goodlands\n(+230) 5567 8901", "Goodlands Branch"),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=12)


    page.add(
        combined_header,
        section_title("Our Services"),
        ft.Container(content=services_row1, padding=ft.padding.symmetric(horizontal=16)),
        ft.Container(height=12),
        ft.Container(content=services_row2, padding=ft.padding.symmetric(horizontal=16)),
        ft.Container(height=12),
        ft.Container(content=services_row3, padding=ft.padding.symmetric(horizontal=16)),
        why_us,
        section_title("Our Locations"),
        ft.Container(content=locations_row1, padding=ft.padding.symmetric(horizontal=16)),
        ft.Container(height=16),
        ft.Container(content=locations_row2, padding=ft.padding.symmetric(horizontal=16)),
        ft.Container(height=16),
        NavBar(page, navigate, active="home"),
    )