from django.shortcuts import render,HttpResponse, redirect ,reverse ,render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, User
from django.shortcuts import get_object_or_404






# end of API

#Generic views practice
from django.views import generic 

@login_required(login_url="/management/login")
def dash(request):
    return render(request,"ManagementSystem/class-management.html")
    #return render(request,"ManagementSystem/dashboard.html")

def table(request):
    list = Class.objects.all()
    ContexDictionary = { 'classes': list}
    #return render(request,'ManagementSystem/tables.html',ContexDictionary)
    return class_management(request)
def table(request):
    list = Class.objects.all()
    ContexDictionary = { 'classes': list}
    #return render(request,'ManagementSystem/tables.html',ContexDictionary)
    return class_management(request)




"""
App Name
"""
app = 'ManagementSystem'
#----

# retrive user permisssions 
def getPermissionsList(user,model,app=app):
    permissions = []
    if user.has_perm(app+'.add_'+model):
        permissions.append("Add")
    if user.has_perm(app+'.change_'+model):
        permissions.append("Change")
    if user.has_perm(app+'.delete_'+model):
        permissions.append("Delete")
    if user.has_perm(app+'.view_'+model):
        permissions.append("View")
    print(permissions)
    return permissions

# Create your views here.
# Login view
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
            user = get_object_or_404(User, pk=request.user.id)
            user.get_all_permissions()
            if 'next' in request.POST:
                #some way to send invaldi details back
                return redirect(request.POST.get('next'))
            return redirect(reverse('user_profile'))
        else:
            error = "Invalid username or password"
            ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'Login_Form': form, 'ID_Error':error }
            return render(request, 'ManagementSystem/login.html', ContexDictionary)
    ContexDictionary ={'UC_Name': chapter[0].name, 'UC_Details':chapter[0].discription,'Login_Form':form}
    return render(request,'ManagementSystem/login.html', ContexDictionary)



def index(request):
    form = Login()
    chapter = UC_Chapter.objects.all()
    ContexDictionary ={'UC_Name': chapter[0].name, 'UC_Details':chapter[0].discription,'Login_Form':form}
    return render(request,'ManagementSystem/index.html', ContexDictionary)


@login_required(login_url="/management/login")
def profile(request):
    chapter = UC_Chapter.objects.all()
    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription}
    return render(request,'ManagementSystem/profile.html',ContexDictionary)


@login_required(login_url="/management/login")
def add_class(request):
    message = ''
    permissions = getPermissionsList(request.user,'class')
    if "Add" in permissions and "View" in permissions:    
        if request.method == 'POST':
            form = EditClass(request.POST)
            if form.is_valid():
                form.save()
                message = 'Class was added successfully.'
                form = EditClass()
                ContexDictionary = {'form': form,'message': message}
                return render(request, 'ManagementSystem/class-form.html', ContexDictionary)
            else:
                ContexDictionary = {'form': form,'message':message}
                return render(request, 'ManagementSystem/class-form.html', ContexDictionary)

        form = EditClass()
        ContexDictionary = {'form': form,'message':message}
        return render(request, 'ManagementSystem/class-form.html', ContexDictionary)
    return HttpResponse("You are not authorized for adding classes")



@login_required(login_url="/management/login")
def class_table_update(request):
    if request.method == 'POST':
        list = Class.objects.all().filter(name__icontains = request.POST['searchBox'])
        paginator = Paginator(list,request.POST['numberOfEntries']) 
        page = request.POST['page']
        list = paginator.get_page(page)
    
        permissions = getPermissionsList(request.user,'class')
        if "View" not in permissions:
            return HttpResponse("You are not authorised to view classes.")
        classFilter = ClassFilter(initial={'searchBox':request.POST['searchBox'],'numberOfEntries':request.POST['numberOfEntries']})
        ContexDictionary = { 'classes': list, 'permissions':permissions,'classFilter':classFilter}
        return render(request,'ManagementSystem/class-table.html',ContexDictionary)

@login_required(login_url="/management/login")
def class_management(request):
    permissions = getPermissionsList(request.user,'class')
    if "View" in permissions:
        chapter = UC_Chapter.objects.all()
        list = Class.objects.all()
        form = EditClass()
        
        
        paginator = Paginator(list, 5) # Show 25 contacts per page
        page = request.GET.get('page')
        print(page)
        list = paginator.get_page(page)
        classFilter = ClassFilter()
        ContexDictionary = {'classes': list,'form':form,'classFilter':classFilter, 'permissions':permissions}
        return render(request,'ManagementSystem/class-management.html',ContexDictionary)
    return HttpResponse("You are not Authorized.")




@login_required(login_url="/management/login")
def delete_class(request):
    permissions = getPermissionsList(request.user,'class')
    if "View" in permissions and "Delete" in permissions:
        response_list = []
        if request.method == 'POST':
            for i in request.POST:
                if request.POST[i] == 'true':
                    response_list.append(i)
        Class.objects.filter(pk__in=response_list).delete()
        # class filters
        return class_table_update(request)
        return render(request,'ManagementSystem/class-table.html',ContexDictionary)
    return HttpResponse("You are not authorized delete classes.")
    

@login_required(login_url="/management/login")
def view_class_modal(request, ID):
    message= ''
    form = None
    permissions = getPermissionsList(request.user,'class')
    if "View" not in permissions:
        return HttpResponse("You are not authorized for viewing classes.")

    clss = Class.objects.get(id=ID)
    if request.method == 'POST':
        if "Change" in permissions:
            form = EditClass(request.POST,instance=clss)
            if form.is_valid():
                form.save()#not saving because name is used as primary key, saves another instance
                message ='Class was updated successfully'
                ContexDictionary = {'form': form,'message': message}
                return render(request,'ManagementSystem/class-form.html', ContexDictionary)
            else:
                ContexDictionary = { 'form': form, 'message': message}
                return render(request, 'ManagementSystem/class-form.html', ContexDictionary)
        return HttpResponse("You are not authorized for editting classes")

    if form == None:
        form = EditClass(instance=clss)
        if clss == None:
            return HttpResponse('<h1> ERORR<h1>')
    st = Students.objects.filter(enrollment__clas_id = clss.id)
    
    ContexDictionary = {'form':form,'enrolmentForm':EnrolmentForm(initial={'clas' : clss.id}) , 'students':st,"permissions":permissions}
    return render(request, 'ManagementSystem/view-class-modal.html', ContexDictionary)


@login_required(login_url="/management/login")
def enrol_from_class_view(request):
    ContexDictionary = None
    enroledStudents = Students.objects.filter(enrollment__clas_id = request.POST['clas'])
    if request.method == 'POST':
        print(request.POST)
        form = EnrolmentForm(request.POST)
        if form.is_valid():
            form.save()#save
            message ='Enrollement was updated successfully'
            enroledStudents = Students.objects.filter(enrollment__clas_id = request.POST['clas'])
            ContexDictionary = {'enrolmentForm': form,'message': message,'students':enroledStudents}
            form = EnrolmentForm()
            return render(request,'ManagementSystem/view-enroled-students.html', ContexDictionary)
        else:
            enroledStudents = Students.objects.filter(enrollment__clas_id = request.POST['clas'])
            ContexDictionary = {'enrolmentForm': form,'students':enroledStudents}
            #return HttpResponse("Error !")
            return render(request, 'ManagementSystem/view-enroled-students.html', ContexDictionary)

@login_required(login_url="/management/login")
def enrol_from_student_view(request):
    ContexDictionary = None
    enroledClasses = Class.objects.filter(enrollment__student_id = request.POST['student'])
    if request.method == 'POST':
        print(request.POST)
        form = EnrolmentForm(request.POST)
        if form.is_valid():
            form.save()#save
            message ='Enrollement was updated successfully'
            enroledClasses = Class.objects.filter(enrollment__student_id  = request.POST['student'])
            ContexDictionary = {'enrolmentForm': form,'message': message,'classes':enroledClasses}
            form = EnrolmentForm()
            return render(request,'ManagementSystem/view-students-enrolments.html', ContexDictionary)
        else:
            enroledClasses = Class.objects.filter(enrollment__student_id = request.POST['student'])
            ContexDictionary = {'enrolmentForm': form,'classes':enroledClasses}
            #return HttpResponse("Error !")
            return render(request, 'ManagementSystem/view-students-enrolments.html', ContexDictionary)





@login_required(login_url="/management/login")
def view_class(request, ID):
    message= ''
    form = None
    permissions = getPermissionsList(request.user,'class')
    if "View" not in permissions:
        return HttpResponse("You are not authorized for viewing classes.")

    clss = Class.objects.get(id=ID)
    if request.method == 'POST':
        if "Change" in permissions:
            form = EditClass(request.POST,instance=clss)
            if form.is_valid():
                form.save()#not saving because name is used as primary key, saves another instance
                message ='Class was updated successfully'
                ContexDictionary = {'form': form,'message': message}
                return render(request,'ManagementSystem/class-form.html', ContexDictionary)
            else:
                ContexDictionary = { 'form': form, 'message': message}
                return render(request, 'ManagementSystem/class-form.html', ContexDictionary)
        return HttpResponse("You are not authorized for editting classes")

    if form == None:
        form = EditClass(instance=clss)
        if clss == None:
            return HttpResponse('<h1> ERORR<h1>')
    st = Students.objects.filter(enrollment__clas_id = clss.id)
    
    ContexDictionary = {'form':form, 'students':st}
    return render(request, 'ManagementSystem/class-form.html', ContexDictionary)




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



@login_required(login_url="/management/login")
def view_student_modal(request, ID):
    try:
        student = Students.objects.get(id=ID)
    except Students.DoesNotExist:
        return HttpResponse('<h1>This Student Is No longer Valid.</h1>')

    form = EditStudent(instance=student)
    classes = Class.objects.filter(enrollment__student_id = ID)
    enroledClasses = Class.objects.filter(enrollment__student_id = ID)
    ContexDictionary = {'student': student,'enrolmentForm':EnrolmentForm(initial={'student' : ID}),'classes':enroledClasses,'studentForm':form}
    
    return render(request,'ManagementSystem/view-student-modal.html',ContexDictionary)




@login_required(login_url="/management/login")
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

    list = Students.objects.all()
    page = request.GET.get('page')
    list = Paginator(list,5).get_page(page)#10 entries
    filterr = StFilter()
    
    
    form = EditStudent()
    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'students': list,'filter':filterr,'studentForm':form}
    return render(request,'ManagementSystem/student-management.html',ContexDictionary)




@login_required(login_url="/management/login")
def student_table_update(request):
    list = Students.objects.all()
    page = request.POST.get('page')
    list = Paginator(list,5).get_page(page)#10 entries
    print(request.POST)
    ContexDictionary = { 'students': list}
    return render(request,'ManagementSystem/student-table.html',ContexDictionary)






@login_required(login_url="/management/login")
def add_student(request):
    message = ''
    chapter = UC_Chapter.objects.all()
    if request.method == 'POST':
        form = EditStudent(request.POST)

        if form.is_valid():
            form.save()
            message = 'Student was created successfully.'
            form = EditStudent()
            return render(request, 'ManagementSystem/student-form.html', {'studentForm': form, 'message': message})
        else:
            return render(request, 'ManagementSystem/student-form.html', {'studentForm': form, 'message': message})

    form = EditStudent()
    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'studentForm': form,'message':message}
    return render(request, 'ManagementSystem/student-form.html', ContexDictionary)







@login_required(login_url="/management/login")
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
            ContexDictionary = {'studentForm': form,'message': message}
            return render(request,'ManagementSystem/student-form.html', ContexDictionary)
        else:
            ContexDictionary = { 'studentForm': form,'message': message}
            return render(request, 'ManagementSystem/student-form.html', ContexDictionary)
    if form == None:
        form = EditStudent(instance=std)
        if std == None:
            return HttpResponse('<h1> ERORR<h1>')
    ContexDictionary = {'UC_Name': chapter[0].name, 'UC_Details': chapter[0].discription, 'studentForm':form}
    return render(request,'ManagementSystem/student-form.html',ContexDictionary)


@login_required(login_url="/management/login")
def delete_student(request):
    response_list =[]
    
    if request.method == 'POST':
        print(request.POST)
        for i in request.POST:
            if request.POST[i] == 'true':
                response_list.append(i)
        
        Students.objects.filter(pk__in=response_list).delete()
        list = Students.objects.all()
        page = request.POST['page']
        list = Paginator(list,5).get_page(page)#10 entries
        ContexDictionary = {'students': list}
        return render(request,'ManagementSystem/student-table.html',ContexDictionary)
    return HttpResponse("<h1>Only Accepts POST Method.</h1>");







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


print(Students.objects.filter(enrollment__clas_id = 1))
