from django.shortcuts import render,HttpResponse, redirect ,reverse ,render_to_response
from .models import *
from .forms import *
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def main(request):
    form = Login()
    chapter = UC_Chapter.objects.all()


    print(chapter)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username= username, password= password)
        if (user!=None):
            login(request,user)
            if 'next' in request.POST:
                #some way to send invaldi details back
                return redirect(request.POST.get('next'))
            return redirect(reverse('user_profile'))
        else:
            error = "Invalid username or password"
            ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'Login_Form': form, 'ID_Error':error }
            return render(request, 'ManagementSystem/main.html', ContexDictionary)
    ContexDictionary ={'UC_Name': chapter[0].name, 'UC_Details':chapter[0].discription,'Login_Form':form}
    return render(request,'ManagementSystem/main.html', ContexDictionary)



def index(request):
    ContexDictionary ={'UC_Name': 'HABIB UNIVERSITY CHAPTER' 'UC_Details':'This is, what it is'}
    return render(request,'ManagementSystem/index.html', ContexDictionary)


@login_required(login_url="/management")
def profile(request):
    chapter = UC_Chapter.objects.all()
    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription}
    return render(request,'ManagementSystem/user-profile.html',ContexDictionary)


@login_required(login_url="/management")
def add_class(request):
    message = ''
    chapter = UC_Chapter.objects.all()
    if request.method == 'POST':
        form = EditClass(request.POST)
        if form.is_valid():
            form.save()
            message = 'Class was added successfully.'
            form = EditClass()
            ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'form': form,'message': message}
            return render(request, 'ManagementSystem/class-form.html', ContexDictionary)
        else:
            ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription,'form': form,'message':message}
            return render(request, 'ManagementSystem/class-form.html', ContexDictionary)

    form = EditClass()
    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'form': form,'message':message}
    return render(request, 'ManagementSystem/add-class.html', ContexDictionary)










@login_required(login_url="/management")
def class_management(request):
    chapter = UC_Chapter.objects.all()
    list = Class.objects.all()
    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'classes': list}
    return render(request,'ManagementSystem/class-management.html',ContexDictionary)






@login_required(login_url="/management")
def delete_class(request):
    response_list =[]
    if request.method == 'POST':
        for i in request.POST:
            if request.POST[i] == 'true':
                response_list.append(i)
    Class.objects.filter(pk__in=response_list).delete()
    list = Class.objects.all()
    ContexDictionary = {'classes': list}
    return render(request,'ManagementSystem/class-table.html',ContexDictionary)



@login_required(login_url="/management")
def view_class(request, ID):
    message= ''
    form = None
    clss = Class.objects.get(id=ID)
    chapter = UC_Chapter.objects.all()
    if request.method == 'POST':
        form = EditClass(request.POST,instance=clss)
        if form.is_valid():
            form.save()#not saving because name is used as primary key, saves another instance
            message ='Class was updated successfully'
            ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription,'form': form,'message': message}
            return render(request,'ManagementSystem/class-form.html', ContexDictionary)
        else:
            ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'form': form,
                                'message': message}
            return render(request, 'ManagementSystem/class-form.html', ContexDictionary)

    if form == None:
        form = EditClass(instance=clss)
        if clss == None:
            return HttpResponse('<h1> ERORR<h1>')

    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'form':form}
    return render(request,'ManagementSystem/update-class.html',ContexDictionary)




def student_filter(request):
    q = Students.objects.all()
    if request.method == 'POST':
        filterr = StFilter(request.POST)
        if filterr.is_valid():
            clas = filterr.cleaned_data['class_selector']
            batch = filterr.cleaned_data['batch_selector']
            print(clas,batch)
            if batch != 'all':
                q = q.filter(batch = batch)
            if clas != 'all':
                q = q.filter(enrollment__clas = clas)
            return list(q)





@login_required(login_url="/management")
def student_management(request):
    list = []
    chapter = UC_Chapter.objects.all()
    lst = student_filter(request)
    if lst!=None:
        clas =None
        for students in lst:
            try:
                clas = Class.objects.get(enrollment__student=students.id)
            except Class.DoesNotExist:
                Clas = None

            list.append([students, clas])
        ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'students': list}
        return render_to_response('ManagementSystem/student-table.html',context=ContexDictionary)

    filterr = StFilter()
    lst = Students.objects.all()
    clas = Class.objects.all()
    for students in lst:
        try:
            stClass = clas.get(enrollment__student=students.id)
        except Class.DoesNotExist:
            stClass = None
        list.append([students,stClass])

    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'students': list,'filter':filterr}
    return render(request,'ManagementSystem/student-management.html',ContexDictionary)






@login_required(login_url="/management")
def add_student(request):
    message = ''
    chapter = UC_Chapter.objects.all()
    if request.method == 'POST':
        form = EditStudent(request.POST)

        if form.is_valid():
            form.save()
            message = 'Student was created successfully.'
            form = EditStudent()
            return render(request, 'ManagementSystem/student-form.html', {'form': form, 'message': message})
        else:
            return render(request, 'ManagementSystem/student-form.html', {'form': form, 'message': message})

    form = EditStudent()
    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'form': form,'message':message}
    return render(request, 'ManagementSystem/add-student.html', ContexDictionary)


@login_required(login_url="/management")
def update_student(request, ID):
    message= ''
    form = None
    std = Students.objects.get(id=ID)
    chapter = UC_Chapter.objects.all()
    if request.method == 'POST':
        form = EditStudent(request.POST,instance=std)
        if form.is_valid():
            form.save()
            message ='Class was updated successfully'
            ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription,'form': form,'message': message}
            return render(request,'ManagementSystem/student-form.html', ContexDictionary)
        else:
            ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'form': form,
                                'message': message}
            return render(request, 'ManagementSystem/student-form.html', ContexDictionary)

    if form == None:
        form = EditStudent(instance=std)
        if std == None:
            return HttpResponse('<h1> ERORR<h1>')

    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'form':form}
    return render(request,'ManagementSystem/update-student.html',ContexDictionary)


@login_required(login_url="/management")
def delete_student(request):

    response_list =[]
    if request.method == 'POST':
        print(request.POST)
        for i in request.POST:
            if request.POST[i] == 'true':
                response_list.append(i)
    Students.objects.filter(pk__in=response_list).delete()
    lst = Students.objects.all()
    list =[]
    for students in lst:
        try:
            clas = Class.objects.get(enrollment__student=students.id)
        except Class.DoesNotExist:
            Clas = None

        list.append([students, clas])
    ContexDictionary = {'students': list}
    return render(request,'ManagementSystem/student-table.html',ContexDictionary)









def logout(request):
    auth.logout(request)
    return redirect("/management")

def test_view(request):
    if request.method=='POST':
        print(request.POST['test'])
    list=[]
    lst = Students.objects.all()

    for students in lst:
        list.append([students.getFullName(), students.fathername])
    return render_to_response('ManagementSystem/student-table.html',context={'students':list})

def test_view(request):
    if request.method=='POST':
        x=EditClass(request.POST)

    return render_to_response('ManagementSystem/student-table.html',context={'students':list})
