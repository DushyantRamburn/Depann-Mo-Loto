import flet as ft
import math
from screens.navbar import NavBar

def ContactScreen(page, api, state, navigate):

    branches = [
        {"name": "Vacoas Branch", "address": "123 Royal Road, Vacoas",
         "phone": "+230 686 1234", "lat": -20.3176, "lng": 57.4845},
        {"name": "Port Louis Branch", "address": "456 Sir William Newton St, Port Louis",
         "phone": "+230 212 5678", "lat": -20.1654, "lng": 57.4896},
        {"name": "Flacq Branch", "address": "789 Royal Road, Centre de Flacq",
         "phone": "+230 413 9012", "lat": -20.1833, "lng": 57.7167},
        {"name": "Goodlands Branch", "address": "321 Royal Road, Goodlands",
         "phone": "+230 283 4567", "lat": -19.9833, "lng": 57.6500},
    ]

    status_text = ft.Text(
        "Tap 'Find Nearest Branch' to use your GPS location",
        size=12, color="#AAAAAA", text_align=ft.TextAlign.CENTER
    )
    nearest_text = ft.Text(
        "", size=14, weight=ft.FontWeight.BOLD,
        color="#28A745", text_align=ft.TextAlign.CENTER
    )
    branch_list = ft.Column(spacing=10)

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        return R * 2 * math.asin(math.sqrt(a))

    def branch_card(b):
        dist_label = f"  •  {b['distance']:.1f} km away" if "distance" in b else ""
        is_nearest = b.get("is_nearest", False)
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Text("📍", size=24),
                        bgcolor="#2A2A4A",
                        border_radius=25,
                        padding=8,
                        width=45,
                        height=45,
                    ),
                    ft.Column([
                        ft.Row([
                            ft.Text(b["name"], size=16, weight=ft.FontWeight.BOLD,
                                    color="white"),
                            ft.Container(
                                content=ft.Text("Nearest", size=10,
                                                color="#1A1A2E",
                                                weight=ft.FontWeight.BOLD),
                                bgcolor="#28A745", border_radius=10,
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                visible=is_nearest,
                            ),
                        ], spacing=8),
                        ft.Text(b["address"] + dist_label, size=11, color="#AAAAAA"),
                        ft.Text(b["phone"], size=12, color="#FFE597"),
                    ], spacing=2, expand=True),
                ], spacing=12),
            ]),
            bgcolor="#2A2A4A" if is_nearest else "#16213E",
            border_radius=12,
            padding=16,
            margin=ft.margin.symmetric(horizontal=16, vertical=4),
            border=ft.border.all(2, "#28A745" if is_nearest else "#333355"),
        )

    def render_branches(user_lat=None, user_lon=None):
        sorted_branches = [dict(b) for b in branches]
        if user_lat is not None and user_lon is not None:
            for b in sorted_branches:
                b["distance"] = haversine(user_lat, user_lon, b["lat"], b["lng"])
            sorted_branches.sort(key=lambda x: x.get("distance", 9999))
            sorted_branches[0]["is_nearest"] = True
            nearest_text.value = f"📍 Nearest: {sorted_branches[0]['name']}"
        branch_list.controls.clear()
        for b in sorted_branches:
            branch_list.controls.append(branch_card(b))
        page.update()

    def get_location(e):
        status_text.value = "Using your approximate location (Curepipe)..."
        page.update()
        render_branches(-20.3176, 57.5263)

    render_branches()

    # Map container — opens OpenStreetMap in browser on click
    map_container = ft.Container(
        content=ft.Column([
            ft.Text("🗺️  Branch Locations Map", size=14,
                    weight=ft.FontWeight.BOLD, color="white",
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=8),
            ft.Container(
                content=ft.Column([
                    ft.Text("🗺️", size=50, text_align=ft.TextAlign.CENTER),
                    ft.Text("View All Branches on Map", size=14,
                            color="#FFE597", weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Tap the button below to open\nthe map in your browser",
                            size=11, color="#AAAAAA",
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "🗺️  Open Map",
                        url=(
                            "https://www.google.com/maps/dir/"
                            "-20.3176,57.4845/"
                            "-20.1654,57.4896/"
                            "-20.1833,57.7167/"
                            "-19.9833,57.6500/"
                        ),
                        style=ft.ButtonStyle(
                            bgcolor="#FFE597", color="#000000",
                            shape=ft.RoundedRectangleBorder(radius=25),
                        ),
                        width=220,
                    ),
                    ft.Text(
                        "📍 Vacoas  📍 Port Louis  📍 Flacq  📍 Goodlands",
                        size=11, color="#AAAAAA",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
                bgcolor="#2A2A4A",
                border_radius=10,
                padding=20,
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#16213E",
        border_radius=12,
        padding=16,
        margin=ft.margin.symmetric(horizontal=16, vertical=8),
        border=ft.border.all(1, "#333355"),
    )

    hours_card = ft.Container(
        content=ft.Column([
            ft.Text("🕐  Business Hours", size=16,
                    weight=ft.FontWeight.BOLD, color="white",
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=3, bgcolor="#FFE597", border_radius=2, width=60),
            ft.Container(height=12),
            ft.Row([
                ft.Text("Monday - Friday", size=13, color="#AAAAAA", expand=True),
                ft.Text("8:00 AM - 6:00 PM", size=13,
                        color="#FFE597", weight=ft.FontWeight.BOLD),
            ]),
            ft.Container(height=1, bgcolor="#333355"),
            ft.Row([
                ft.Text("Saturday", size=13, color="#AAAAAA", expand=True),
                ft.Text("8:00 AM - 4:00 PM", size=13,
                        color="#FFE597", weight=ft.FontWeight.BOLD),
            ]),
            ft.Container(height=1, bgcolor="#333355"),
            ft.Row([
                ft.Text("Sunday", size=13, color="#AAAAAA", expand=True),
                ft.Text("Emergency Only", size=13,
                        color="#FF8C00", weight=ft.FontWeight.BOLD),
            ]),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        bgcolor="#16213E",
        border_radius=12,
        padding=20,
        margin=ft.margin.symmetric(horizontal=16, vertical=8),
        border=ft.border.all(1, "#333355"),
    )

    page.add(
        # Hero banner
        ft.Container(
            content=ft.Column([
                ft.Text("📍", size=50, text_align=ft.TextAlign.CENTER),
                ft.Text("Contact Us", size=26, weight=ft.FontWeight.BOLD,
                        color="white", text_align=ft.TextAlign.CENTER),
                ft.Container(height=3, bgcolor="#FFE597", border_radius=2, width=60),
                ft.Container(height=6),
                ft.Text("Get in touch for all your car servicing needs",
                        size=13, color="#AAAAAA", text_align=ft.TextAlign.CENTER),
                ft.Container(height=16),
                ft.Divider(color="#333355"),
                ft.Container(height=12),
                ft.ElevatedButton(
                    "📍  Find Nearest Branch",
                    on_click=get_location,
                    style=ft.ButtonStyle(
                        bgcolor="#FFE597",
                        color="#000000",
                        shape=ft.RoundedRectangleBorder(radius=25),
                    ),
                    width=280,
                ),
                status_text,
                nearest_text,
                ft.Container(height=8),
                ft.Divider(color="#333355"),
                ft.Container(height=8),
                ft.Text("Our Locations", size=18, weight=ft.FontWeight.BOLD,
                        color="white", text_align=ft.TextAlign.CENTER),
                ft.Container(
                    height=3, bgcolor="#FFE597",
                    border_radius=2, width=50,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            bgcolor="#1A1A2E",
            padding=ft.padding.symmetric(vertical=30, horizontal=16),
        ),

        ft.Container(height=8),
        branch_list,
        ft.Container(height=8),
        map_container,
        hours_card,
        ft.Container(height=16),
        NavBar(page, navigate, active="contact"),
    )