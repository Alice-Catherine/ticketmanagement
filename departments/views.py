from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm


@login_required
def department_list(request):
    departments = Department.objects.all().order_by('name')
    return render(request, 'departments/department_list.html', {'departments': departments})


@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    categories = department.categories.all()
    tickets = department.tickets.all().order_by('-created_at')
    return render(request, 'departments/department_detail.html', {
        'department': department,
        'categories': categories,
        'tickets': tickets,
    })


@login_required
def department_create(request):
    if request.user.role != 'admin':
        messages.error(request, "Only Administrators can create departments.")
        return redirect('departments:department_list')

    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully.")
            return redirect('departments:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form})