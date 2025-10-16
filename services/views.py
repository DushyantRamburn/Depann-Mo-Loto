from django.shortcuts import render

def services_list(request):
    # For now, just render the template - we'll add data later
    return render(request, 'services/service_list.html')


