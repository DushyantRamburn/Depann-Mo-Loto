import flet as ft

def BookingScreen(page, api, state, navigate):
    service = state.get("selected_service", {})

    make = ft.TextField(label="Car Make (e.g. Toyota)", bgcolor="white")
    model = ft.TextField(label="Car Model (e.g. Yaris)", bgcolor="white")
    year = ft.TextField(label="Year (e.g. 2020)", keyboard_type=ft.KeyboardType.NUMBER, bgcolor="white")
    plate = ft.TextField(label="License Plate", bgcolor="white")
    vehicle_type = ft.Dropdown(
        label="Vehicle Type",
        options=[
            ft.dropdown.Option("car", "Car"),
            ft.dropdown.Option("suv", "SUV"),
            ft.dropdown.Option("van", "Van"),
            ft.dropdown.Option("truck", "Truck"),
        ],
        value="car", bgcolor="white",
    )
    date_field = ft.TextField(label="Date (YYYY-MM-DD)", bgcolor="white")
    time_field = ft.TextField(label="Time (HH:MM)", value="09:00", bgcolor="white")
    first_name = ft.TextField(label="First Name", bgcolor="white")
    last_name = ft.TextField(label="Last Name", bgcolor="white")
    email = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL, bgcolor="white")
    phone = ft.TextField(label="Phone Number", keyboard_type=ft.KeyboardType.PHONE, bgcolor="white")
    password = ft.TextField(label="Create Password", password=True,
                            can_reveal_password=True, bgcolor="white")

    error_text = ft.Text("", color="#DC3545", size=13)
    content_area = ft.Column(scroll="auto", expand=True)

    def progress_bar(current_step):
        steps = ["1. Service", "2. Vehicle", "3. Date & Time", "4. Personal"]
        chips = []
        for i, s in enumerate(steps):
            step_num = i + 1
            if step_num < current_step:
                bg = "#28A745"
                color = "white"
            elif step_num == current_step:
                bg = "#FFE597"
                color = "#000000"
            else:
                bg = "#E9ECEF"
                color = "#6C757D"
            chips.append(
                ft.Container(
                    content=ft.Text(s, size=10, color=color, weight=ft.FontWeight.BOLD),
                    bgcolor=bg, border_radius=20,
                    padding=ft.padding.symmetric(horizontal=8, vertical=6),
                )
            )
        return ft.Container(
            content=ft.Row(chips, alignment=ft.MainAxisAlignment.CENTER, spacing=4),
            bgcolor="#F8F9FA", padding=12, border_radius=10,
        )

    def form_card(title, fields):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD,
                        color="#333333", text_align=ft.TextAlign.CENTER),
                ft.Divider(color="#E9ECEF"),
                *fields,
            ], spacing=12),
            bgcolor="white", border_radius=15, padding=20,
            margin=ft.margin.symmetric(horizontal=16),
        )

    def nav_buttons(back_fn, next_fn, next_label="Continue"):
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    "Back",
                    on_click=back_fn,
                    style=ft.ButtonStyle(
                        bgcolor="#6C757D", color="white",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                ft.ElevatedButton(
                    next_label,
                    on_click=next_fn,
                    style=ft.ButtonStyle(
                        bgcolor="#FFE597", color="#000000",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
        )

    def show_step1():
        content_area.controls.clear()
        content_area.controls.append(progress_bar(1))
        content_area.controls.append(ft.Container(height=8))
        content_area.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Selected Service", size=14, color="#666666",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text(service.get("name", ""), size=18,
                            weight=ft.FontWeight.BOLD, color="#333333",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text(f"Rs {service.get('price', '')}", size=16,
                            weight=ft.FontWeight.BOLD, color="#FFB800",
                            text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                bgcolor="#D4EDDA", border_radius=10,
                padding=16, margin=ft.margin.symmetric(horizontal=16),
                border=ft.border.all(1, "#C3E6CB"),
            )
        )
        content_area.controls.append(ft.Container(height=8))
        content_area.controls.append(
            nav_buttons(
                back_fn=lambda e: navigate("services"),
                next_fn=lambda e: show_step2(),
                next_label="Continue to Vehicle Details",
            )
        )
        page.update()

    def show_step2():
        content_area.controls.clear()
        content_area.controls.append(progress_bar(2))
        content_area.controls.append(ft.Container(height=8))
        content_area.controls.append(
            form_card("Vehicle Information", [make, model, year, plate, vehicle_type])
        )
        content_area.controls.append(error_text)
        content_area.controls.append(
            nav_buttons(
                back_fn=lambda e: show_step1(),
                next_fn=validate_step2,
                next_label="Continue to Date & Time",
            )
        )
        page.update()

    def validate_step2(e):
        if not all([make.value, model.value, year.value, plate.value]):
            error_text.value = "Please fill in all vehicle fields."
            page.update()
            return
        error_text.value = ""
        show_step3()

    def show_step3():
        content_area.controls.clear()
        content_area.controls.append(progress_bar(3))
        content_area.controls.append(ft.Container(height=8))
        content_area.controls.append(
            form_card("Select Date & Time", [date_field, time_field])
        )
        content_area.controls.append(error_text)
        content_area.controls.append(
            nav_buttons(
                back_fn=lambda e: show_step2(),
                next_fn=validate_step3,
                next_label="Continue to Personal Details",
            )
        )
        page.update()

    def validate_step3(e):
        if not all([date_field.value, time_field.value]):
            error_text.value = "Please fill in date and time."
            page.update()
            return
        error_text.value = ""
        show_step4()

    def show_step4():
        content_area.controls.clear()
        content_area.controls.append(progress_bar(4))
        content_area.controls.append(ft.Container(height=8))
        content_area.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Your Details", size=20, weight=ft.FontWeight.BOLD,
                            color="#1A1A1A", text_align=ft.TextAlign.CENTER),
                    ft.Divider(color="#E9ECEF"),
                    first_name,
                    last_name,
                    email,
                    phone,
                    ft.Divider(color="#E9ECEF"),
                    ft.Text("Create your account password",
                            size=12, color="#666666",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("You'll use this password to login later",
                            size=11, color="#AAAAAA",
                            text_align=ft.TextAlign.CENTER),
                    password,
                ], spacing=12),
                bgcolor="white", border_radius=15, padding=20,
                margin=ft.margin.symmetric(horizontal=16),
            )
        )
        content_area.controls.append(error_text)
        content_area.controls.append(
            nav_buttons(
                back_fn=lambda e: show_step3(),
                next_fn=submit_booking,
                next_label="Complete Booking",
            )
        )
        page.update()

    def submit_booking(e):
        if not all([first_name.value, last_name.value, email.value,
                    phone.value, password.value]):
            error_text.value = "Please fill in all fields including password."
            page.update()
            return

        if len(password.value) < 6:
            error_text.value = "Password must be at least 6 characters."
            page.update()
            return

        # Register or login user
        if not api.token:
            register_result = api.register(
                email=email.value,
                password=password.value,
                first_name=first_name.value,
                last_name=last_name.value,
            )
            if not register_result:
                # User might already exist, try logging in
                login_result = api.login(email.value, password.value)
                if not login_result:
                    error_text.value = "Email already registered. Check your password or use a different email."
                    page.update()
                    return

        # Create the booking
        booking_data = {
            "service_id": service.get("id"),
            "make": make.value,
            "model": model.value,
            "year": int(year.value),
            "license_plate": plate.value,
            "vehicle_type": vehicle_type.value,
            "booking_date": f"{date_field.value} {time_field.value}:00",
        }
        result, status_code = api.create_booking(booking_data)
        if status_code == 201:
            show_summary(result)
        else:
            error_text.value = result.get("error", "Booking failed. Please try again.")
            page.update()

    def show_summary(booking):
        content_area.controls.clear()
        content_area.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("✅", size=50, text_align=ft.TextAlign.CENTER),
                    ft.Text("Booking Confirmed!", size=22, weight=ft.FontWeight.BOLD,
                            color="#FFE597", text_align=ft.TextAlign.CENTER),
                    ft.Text(
                        "🎉 Congratulations! Your service has been successfully booked.",
                        size=13,
                        color="#FFE597",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(f"Reference: #{booking.get('id', '')}",
                            size=14, color="#666666", text_align=ft.TextAlign.CENTER),
                    ft.Divider(color="#E9ECEF"),
                    ft.Text("Service Details", size=16,
                            weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Text(f"Service: {booking.get('service_name', '')}",
                            size=13, color="#555555"),
                    ft.Text(f"Vehicle: {make.value} {model.value} ({year.value})",
                            size=13, color="#555555"),
                    ft.Text(f"Plate: {plate.value}", size=13, color="#555555"),
                    ft.Text(f"Date: {date_field.value} at {time_field.value}",
                            size=13, color="#555555"),
                    ft.Text(f"Status: {booking.get('status', 'Pending').upper()}",
                            size=13, color="#856404", weight=ft.FontWeight.BOLD),
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("💡 Login Tip", size=13,
                                    weight=ft.FontWeight.BOLD, color="#1A1A2E"),
                            ft.Text(f"Use {email.value} and your password to login anytime.",
                                    size=12, color="#555555",
                                    text_align=ft.TextAlign.CENTER),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                        bgcolor="#FFF9E6", border_radius=8, padding=12,
                        border=ft.border.all(1, "#FFE597"),
                    ),
                    ft.Container(height=16),
                    ft.Row([
                        ft.ElevatedButton(
                            "Back to Home",
                            on_click=lambda e: navigate("home"),
                            style=ft.ButtonStyle(
                                bgcolor="#FFE597", color="#000000",
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                        ft.ElevatedButton(
                            "Book Again",
                            on_click=lambda e: navigate("services"),
                            style=ft.ButtonStyle(
                                bgcolor="#6C757D", color="white",
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                bgcolor="white", border_radius=15, padding=24,
                margin=ft.margin.symmetric(horizontal=16),
            )
        )
        page.update()

    header = ft.Container(
        content=ft.Row([
            ft.TextButton(
                "← Back",
                on_click=lambda e: navigate("services"),
                style=ft.ButtonStyle(color="white"),
            ),
            ft.Text("Book a Service", size=18, weight=ft.FontWeight.BOLD, color="white"),
        ]),
        bgcolor="#1A1A2E",
        padding=ft.padding.symmetric(horizontal=8, vertical=12),
    )

    show_step1()
    page.add(header, content_area)