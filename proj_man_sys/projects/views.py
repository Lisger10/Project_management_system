from django.shortcuts import render
from .forms import CreateProjectForm, ChooseValuesForm
from projects.models import Projects
from django.shortcuts import redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from plotly.offline import plot
from .forms import ChooseValuesForm
import plotly.graph_objects as go
from .models import Projects, Projects_Users
from tasks.models import Task
import plotly.figure_factory as ff
import numpy as np
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.paginator import Paginator


def add_proj(request):
    if request.method == "POST":
        form = CreateProjectForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            project = Projects.objects.latest("id")
            if project.admin == 'user':
                project.admin = request.user.last_name + " " + request.user.first_name
            project.save()
            answer = "Проект успешно создан"
            return render(
                request, "add_or_change_proj.html", {"form": form, "answer": answer}
            )
        else:
            answer = "Введите корректные данные"
            return render(
                request, "add_or_change_proj.html", {"form": form, "answer": answer}
            )
    else:
        form = CreateProjectForm()
    return render(request, "add_or_change_proj.html", {"form": form})


def view_proj(request):
    if not request.user.is_anonymous:
        projects = Projects.objects.all().filter(
        admin=request.user.last_name + " " + request.user.first_name )
        available_projects = Projects.objects.all().filter(users=request.user.username)
        return render(
        request,"projects_view.html", {"projects": projects,
                                        "available_projects": available_projects},)
    else:
        return redirect('add_or_change_proj')



def info_proj(request, id):
    if not request.user.is_anonymous:
        try:
            project = Projects.objects.get(id=id)
            users = User.objects.all().filter(projects__id=project.id)
            tasks = Task.objects.all().filter(project_id=project.id)
            if tasks.count() >= 1:
                gant_chart = create_gant(tasks)
            else:
                gant_chart = "Задачи отсутствуют"
            return render(
                request,
                "project_info.html",
                {
                    "project": project,
                    "tasks": tasks,
                    "users": users,
                    "gant_chart": gant_chart,
                },
            )
        except Projects.DoesNotExist:
            return HttpResponseNotFound("<h1 class = 'not-found'> Project is not found </h1>")
    else:
         return redirect('add_or_change_proj')

        


def change_proj(request, id):
    if not request.user.is_anonymous:
        try:
            project = Projects.objects.get(id=id)
            if request.method == "POST":
                form = CreateProjectForm(request.POST, instance=project)
                if form.is_valid():
                    form.save()
                    answer = "Данные успешно обновлены"
                    return render(
                        request, "add_or_change_proj.html", {"form": form, "answer": answer}
                    )
            if request.method == "GET":
                form = CreateProjectForm(instance=project)
                return render(request, "add_or_change_proj.html", {"form": form})
        except Projects.DoesNotExist:
            return HttpResponseNotFound("<h1 styles='text-align:center'> Проект не найден </h1>")
    else:
        return redirect('add_or_change_proj')


def delete_proj(request, id):
    if not request.user.is_anonymous:
        try:
            project = Projects.objects.get(id=id)
            project.delete()
            return redirect("view_proj")
        except Projects.DoesNotExist:
            return HttpResponseNotFound("<h1 styles='text-align:center'>Проект не найден</h1>")
    else:
        return redirect('add_or_change')


def analytics_proj(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = ChooseValuesForm(request.POST)
            current_user = request.user.last_name + " " + request.user.first_name
            if form.is_valid():
                month = form.cleaned_data["month"]
                year = form.cleaned_data["year"]
                (
                    project_val,
                    project_end_data,
                    projects,
                    project_day,
                    project_color,
                    project_symbol,
                ) = get_projects_data(month, year, current_user)
                graph = create_graph(
                    project_day, project_val, project_symbol, project_color, month
                )
                completed_projects_num = projects.filter(
                    perfomance_status="Выполнен"
                ).count()
                not_completed_projects_num = projects.filter(
                    perfomance_status="Не выполнен"
                ).count()
                rejected_projects_num = projects.filter(
                    perfomance_status="Отклонен"
                ).count()

                pie_chart = create_pie_chart(
                    completed_projects_num,
                    not_completed_projects_num,
                    rejected_projects_num,
                )
                return render(
                    request,
                    "projects_analytics.html",
                    {
                        "month": month,
                        "year": year,
                        "graph": graph,
                        "form": form,
                        "pie_chart": pie_chart,
                    },
                )
        else:
            form = ChooseValuesForm()
            return render(request, "projects_analytics.html", {"form": form})
    return redirect('add_or_change_proj')


def get_projects_data(month, year, current_user):
    month_value = {
        "Январь": 1,
        "Февраль": 2,
        "Март": 3,
        "Апрель": 4,
        "Май": 5,
        "Июнь": 6,
        "Июль": 7,
        "Aвгуст": 8,
        "Сентябрь": 9,
        "Октябрь": 10,
        "Ноябрь": 11,
        "Декабрь": 12,
    }

    for i in month_value.keys():
        if i == month:
            chosen_month = month_value[i]

    chosen_year = int(year)

    project_val = list(
        Projects.objects.all()
        .filter(admin=current_user)
        .filter(end_date__month=chosen_month, end_date__year=chosen_year)
        .values_list("name", flat=True)
    )
    project_end_data = list(
        Projects.objects.all()
        .filter(admin=current_user)
        .values_list("end_date", flat=True)
        .filter(end_date__month=chosen_month, end_date__year=chosen_year)
    )
    projects = (
        Projects.objects.all()
        .filter(admin=current_user)
        .filter(end_date__month=chosen_month, end_date__year=chosen_year)
    )
    project_day = []
    project_color = []
    project_symbol = []

    for project in projects:
        if project.perfomance_status == "Отклонен":
            project_color.append("red")
            project_symbol.append("x")
        elif project.perfomance_status == "Выполнен":
            project_color.append("green")
            project_symbol.append("circle")
        elif project.perfomance_status == "Не выполнен":
            project_color.append("orange")
            project_symbol.append("circle")
    for i in project_end_data:
        project_day.append(i.day)

    return (
        project_val,
        project_end_data,
        projects,
        project_day,
        project_color,
        project_symbol,
    )


def create_graph(project_day, project_val, project_symbol, project_color, month):
    fig = go.Figure(
        data=[
            go.Scatter(
                x=project_day,
                y=project_val,
                mode="markers",
                marker=dict(
                    symbol=project_symbol,
                    color=project_color,
                    size=[20 for x in range(len(project_val))],
                ),
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=80, r=80, t=80, b=80),
        width=1000,
        title={"text": "Выполнение проектов", "xanchor": "center", "yanchor": "bottom"},
        title_x=0.5,
        dragmode="pan",
        xaxis=dict(
            title=month,
            gridcolor="white",
            gridwidth=2,
            tickvals=[0, 5, 10, 15, 20, 25, 30],
            range=[0, 31],
        ),
        yaxis=dict(
            title="Проекты",
            gridcolor="white",
            gridwidth=2,
            tickvals=[x for x in range(len(project_val))],
            ticktext=project_val,
        ),
        paper_bgcolor="rgb(243, 243, 243)",
        plot_bgcolor="rgb(243, 243, 243)",
    )

    config = {"displaylogo": False}

    fig.update_layout(
        modebar_remove=["select", "zoom", "LassoSelect", "lasso2d", "plotly-logomark"],
    )
    graph = plot(fig, output_type="div", config=config)
    return graph


def create_pie_chart(
    completed_projects_num, not_completed_projects_num, rejected_projects_num
):
    labels = [
        "Выполненные проекты",
        "Невыполненные проекты",
        "Отклоненные проекты",
    ]
    values = [completed_projects_num, not_completed_projects_num, rejected_projects_num]
    colors = ["green", "orange", "red", "MediumBlue", "black"]
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo="percent",
                textfont_size=16,
                insidetextorientation="radial",
                textfont=dict(
                    color="white",
                ),
                marker=dict(colors=colors, line=dict(color="#000000", width=1)),
            )
        ]
    )

    pie_chart = plot(fig, output_type="div")
    return pie_chart


def create_gant(tasks):
    gant = []
    for task in tasks:
        gant.append(
            dict(
                Task=task.name,
                Start=task.start_date,
                Finish=task.end_date,
                Status=task.status,
            )
        )
        df = gant
        colors = {'Открыта': 'rgb(220, 0, 0)',
            'Закрыта': 'rgb(0, 220, 0)'}


        fig = ff.create_gantt(
            df,
            colors=colors,
            index_col="Status",
            show_colorbar=True,
            group_tasks=True,
        )

        fig.update_layout(
            modebar_remove=["select", "zoom", "LassoSelect", "lasso2d", "plotly-logomark"],
            title=dict(
                text="Диаграмма Ганта",
                font=dict(size=24),
                x=0.5,
            ),
        )
        gant_chart = plot(fig, output_type="div")
    return gant_chart
