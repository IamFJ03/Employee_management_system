from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, ListView
from employees.models import Employee
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

def user_login(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username = username,
            password = password
        )
        
        if user is not None:
            login(request, user)
            return redirect("employee_list")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "employees/login.html")

def Register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(
        request,
        "employees/register.html",
        {"form": form}
    )

def create_employee(request):
    if request.method == "POST":
        Employee.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            department=request.POST.get("department"),
            salary=request.POST.get("salary"),
            joining_date=request.POST.get("joining_date"),
            is_active=request.POST.get("is_active")=="on"
        )
        return redirect("employee_list")

    return render(request, "employees/create_employee.html")


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employees"

class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = "__all__"
    template_name = "employees/update_employee.html"
    context_object_name = "employee"
    success_url = reverse_lazy("employee_list")

def delete_employee(request, id:None):
    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        employee.delete()
        return redirect("employee_list")

    return render(
        request,
        "employees/delete_employee.html",
        {"employee": employee}
    )

def home(request):
    return render(request, "employees/home.html")

def user_logout(request):

    logout(request)

    return redirect("login")