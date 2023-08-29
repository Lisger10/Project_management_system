from django.shortcuts import render
from django.contrib.auth.models import User


def view_users(request):
    users = User.objects.all()
    return render(request, 'users_view.html', {'users':users})