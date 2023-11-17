from django.shortcuts import render
from .forms import CreateChangeTaskForm,ChangeTaskForm
from .models import Task, Projects, Tasks_Users
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.contrib.auth.models import User


def create_task(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = CreateChangeTaskForm(request.POST or None, request.FILES or None, request = request)
            if form.is_valid():
                form.save()
                task = Task.objects.latest("id")
                task.admin = request.user.last_name + " " + request.user.first_name
                task.save()
                answer = "Задача успешно создана"
                return render(
                    request, "add_or_change_task.html", {"form": form, "answer": answer}
                )
            else:
                answer = 'Некорретные данные'
                return render ( request, "add_or_change_task.html", {"form": form, "answer": answer })
        if request.method == "GET":
            form = CreateChangeTaskForm(request=request)
        return render(request, "add_or_change_task.html", {"form": form})
    else:
        return redirect('add_or_change_proj')

def change_admin_task(request,id):
        if not request.user.is_anonymous:
            try:
                task = Task.objects.get(id=id)
                if request.method == "POST":
                    form = CreateChangeTaskForm(request.POST, instance=task, request=request)
                    if form.is_valid():
                        form.save()
                        answer = "Данные успешно обновлены"
                        return render(
                        request, "add_or_change_task.html", {"form": form, "answer": answer}
                    )
                if request.method == "GET":
                    form = CreateChangeTaskForm(instance=task, request=request)
                    return render(request, "add_or_change_task.html", {"form": form})
            except Task.DoesNotExist:
                return HttpResponseNotFound("<h1>Задача не найдена</h1>")
        else:
             return redirect('add_or_change_proj')
    



def change_task(request, id):
    if not request.user.is_anonymous:
        try:
            task = Task.objects.get(id=id)
            if request.method == "POST":
                form = ChangeTaskForm(request.POST, instance=task, request=request)
                if form.is_valid():
                    form.save()
                    answer = "Данные успешно обновлены"
                    return render(
                    request, "change_task.html", {"form": form, "answer": answer}
                )
            if request.method == "GET":
                form = ChangeTaskForm(instance=task, request=request)
                return render(request, "change_task.html", {"form": form})
        except Task.DoesNotExist:
            return HttpResponseNotFound("<h1 >Задача не найдена</h1>")
    else:
        return redirect('add_or_change_proj')

def view_created_tasks(request):
    if not request.user.is_anonymous:
        created_tasks = Task.objects.all().filter(admin=request.user.last_name + " " + request.user.first_name)
        return render(
            request,
            "tasks_view.html",
            {"created_tasks": created_tasks},
        )
    else:
        return redirect('add_or_change_proj')

def view_available_tasks(request):
    if not request.user.is_anonymous:
        available_tasks = Task.objects.all().filter(project__users__username = request.user.username)
        return render (
            request,
            'tasks_view.html',
            {'available_tasks': available_tasks}
        )
    else:
        return redirect('add_or_change_proj')
    
def view_appointed_tasks(request):
    if not request.user.is_anonymous:
        appointed_tasks = Task.objects.all().filter(users__username = request.user.username)
        return render (
            request,
            'tasks_view.html',
            {'appointed_tasks': appointed_tasks}
        )
    else:
        return redirect('add_or_change_proj')
    
def info_task(request, id):
    if not request.user.is_anonymous:
        try:   
            task = Task.objects.get(id=id)
            users = User.objects.all().filter(task__id=task.id)
            return render(request, 'task_info.html', {'task': task, 'users': users})
        except Task.DoesNotExist:
            return HttpResponseNotFound("<h1>Такой задачи не существует</h1>")
    else:
        return redirect('add_or_change_proj')

def delete_task(request, id):
    if not request.user.is_anonymous:
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return redirect('view_created_tasks')
        except Task.DoesNotExist:
            return HttpResponseNotFound("<h1>Такой задачи не существует </h1>")
    else:
        return redirect('add_or_change_proj')
