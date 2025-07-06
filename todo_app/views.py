from django.shortcuts import render, redirect
from .models import Task, UserDetail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Registration View
def register(request):
    error_message = ""
    success_message = ""

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if UserDetail.objects.filter(email=email).exists():
            error_message = "Email already registered! Please login."
        else:
            UserDetail.objects.create(name=name, email=email, password=password)
            success_message = "Registration successful! Please login."
            return redirect('/login/')

    return render(request, 'todo_app/register.html', {'error_message': error_message, 'success_message': success_message})

# Login View
def user_login(request):
    error_message = ""

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserDetail.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('/todo/')
        except UserDetail.DoesNotExist:
            error_message = "Invalid email or password!"

    return render(request, 'todo_app/login.html', {'error_message': error_message})

# Logout View
def user_logout(request):
    request.session.flush()
    return redirect('/login/')

# ToDo List - Only for logged-in users
def index(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')

    if not user_id:
        return redirect('/login/')

    tasks = Task.objects.filter(user_id=user_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title, user_id=user_id)
            return redirect('/todo/')

    return render(request, 'todo_app/index.html', {'tasks': tasks, 'user_name': user_name})

def delete_task(request, task_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')

    task = Task.objects.filter(id=task_id, user_id=user_id).first()
    if task:
        task.delete()
    return redirect('/todo/')

def complete_task(request, task_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')

    task = Task.objects.filter(id=task_id, user_id=user_id).first()
    if task:
        task.completed = True
        task.save()
    return redirect('/todo/')
