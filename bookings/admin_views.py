
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import Booking
import calendar
from datetime import datetime

@method_decorator(staff_member_required, name='dispatch')
class BookingCalendarView(TemplateView):
    template_name = 'admin/bookings/booking_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get month and year from request or use current
        year = int(self.request.GET.get('year', datetime.now().year))
        month = int(self.request.GET.get('month', datetime.now().month))
        
        # Create calendar
        cal = calendar.monthcalendar(year, month)
        
        # Get bookings for this month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        bookings = Booking.objects.filter(
            booking_date__gte=start_date,
            booking_date__lt=end_date
        ).select_related('user', 'vehicle', 'service')
        
        # Organize bookings by date
        bookings_by_date = {}
        for booking in bookings:
            date_key = booking.booking_date.strftime('%Y-%m-%d')
            if date_key not in bookings_by_date:
                bookings_by_date[date_key] = []
            bookings_by_date[date_key].append(booking)
        
        context.update({
            'calendar': cal,
            'month': month,
            'year': year,
            'month_name': calendar.month_name[month],
            'bookings_by_date': bookings_by_date,
            'prev_month': month - 1 if month > 1 else 12,
            'prev_year': year if month > 1 else year - 1,
            'next_month': month + 1 if month < 12 else 1,
            'next_year': year if month < 12 else year + 1,
        })
        return context
    
    