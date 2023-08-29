from django.shortcuts import render
from .forms import CreateLaborForm
from .models import Labor, Task
from projects.models import Projects
from django.shortcuts import redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.models import User


def create_labor_costs(request):
    if request.method == "POST":
        form = CreateLaborForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            labor = Labor.objects.latest("id")
            labor.executor = request.user.last_name + " " + request.user.first_name
            labor.save()
            return redirect("view_labor_costs")
    if request.method == "GET":
        form = CreateLaborForm()
        form.fields["task"].queryset = Task.objects.filter(users=request.user)
        return render(request, "add_or_change_labor.html", {"form": form})


def view_labor_costs(request):
    labor_costs = Labor.objects.all()
    admin = request.user.last_name + " " + request.user.first_name
    return render(
        request,
        "labor_costs_view.html",
        {"labor_costs": labor_costs, "admin": admin},
    )


def delete_labor(request, id):
    try:
        labor = Labor.objects.get(id=id)
        labor.delete()
        return redirect("view_labor_costs")
    except Labor.DoesNotExist:
        return HttpResponseNotFound("<h1>Ресурс не найден</h1>")
