from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def view_users(request):
    users = User.objects.all()
    paginator = Paginator(users, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "users_view.html", {"page_obj": page_obj})