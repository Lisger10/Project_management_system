from django.shortcuts import render
from .forms import CreateChangeTaskForm,ChangeTaskForm
from .models import Task, Projects, Tasks_Users
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.contrib.auth.models import User

def create_task(request):
    if request.method == "POST":
        form = CreateChangeTaskForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            task = Task.objects.latest("id")
            task.admin = request.user.last_name + " " + request.user.first_name
            task.save()
            answer = "Задача успешно создана"
            return render(
                request, "add_or_change_task.html", {"form": form, "answer": answer}
            )
    if request.method == "GET":
        form = CreateChangeTaskForm()
    return render(request, "add_or_change_task.html", {"form": form})

def change_admin_task(request,id):
    try:
        task = Task.objects.get(id=id)
        if request.method == "POST":
            form = CreateChangeTaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                answer = "Данные успешно обновлены"
                return render(
                request, "add_or_change_task.html", {"form": form, "answer": answer}
            )
        if request.method == "GET":
            form = CreateChangeTaskForm(instance=task)
            return render(request, "add_or_change_task.html", {"form": form})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h1>Задача не найдена</h1>")
    



def change_task(request, id):
    try:
        task = Task.objects.get(id=id)
        if request.method == "POST":
            form = ChangeTaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                answer = "Данные успешно обновлены"
                return render(
                request, "change_task.html", {"form": form, "answer": answer}
            )
        if request.method == "GET":
            form = ChangeTaskForm(instance=task)
            return render(request, "change_task.html", {"form": form})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h1>Задача не найдена</h1>")


def view_created_tasks(request):
    created_tasks = Task.objects.all().filter(admin=request.user.last_name + " " + request.user.first_name)
    return render(
        request,
        "tasks_view.html",
        {"created_tasks": created_tasks},
    )

def view_available_tasks(request):
    available_tasks = Task.objects.all().filter(project__users__username = request.user.username)
    return render (
        request,
        'tasks_view.html',
        {'available_tasks': available_tasks}
    )

def view_appointed_tasks(request):
    appointed_tasks = Task.objects.all().filter(users__username = request.user.username)
    return render (
        request,
        'tasks_view.html',
        {'appointed_tasks': appointed_tasks}
    )

def info_task(request, id):
    try:   
        task = Task.objects.get(id=id)
        users = User.objects.all().filter(task__id=task.id)
        return render(request, 'task_info.html', {'task': task, 'users': users})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h1>Такой задачи не существует</h1>")

def delete_task(request, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return redirect('view_created_tasks')
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h1>Такой задачи не существует </h1>")
