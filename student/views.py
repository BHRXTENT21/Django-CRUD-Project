from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    search = request.GET.get('search', '')
    if search:
        students = Student.objects.filter(name__icontains=search)
    else:
        students = Student.objects.all().order_by('name')


    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj, 'search': search})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Student.objects.filter(email=email).exists():
                messages.error(request, "Email already exists! Please use a different one.")
            else:
                form.save()
                messages.success(request, "Student added successfully!")
                return redirect('home')
    else:
        form = StudentForm()
    return render(request, 'add.html', {'form': form})


def edit_student(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('home')
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit.html', {'form': form})

def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    messages.error(request, "Student deleted successfully!")
    return redirect('home')
