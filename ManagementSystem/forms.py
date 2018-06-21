from django import forms
from . import models 
from django.db.models import Q 
from datetime import date

# Helper Functions
def name_Cleaner(name):
    lst_names = name.split(' ')
    str = ''
    for i in lst_names:
        if i != '':
            str += i.capitalize()
            str += ' '
    return str.strip(' ')




class ClassFilter(forms.Form):
    searchBox = forms.CharField(max_length=30, label='Search',required=False, widget= forms.TextInput(attrs={'class':'form-control'}))
    numberOfEntries = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Number of Entries', choices=[(5,5),(10,10),(50,50),(100,100)],required=False)

    def getFilteredClass(self):
     
        print(self.cleaned_data)
        
    




class Login(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label='ID')
    id_for_lable = 'text'
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}),label='Password')
    #error
    error = None

class deletetion(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label='ID', max_length=4)
    id_for_lable = 'text'
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}),label='Password',max_length=8)
    #error
    error = None


class EditClass(forms.ModelForm):
    class Meta:
        model = models.Class
        fields = '__all__'

        widgets = {
            'name': forms.TextInput({'class' : 'form-control field form-control-sm','placeholder':'Class Name'}),
            'section': forms.Select({'class' : 'form-control field form-control-sm','placeholder':'Section'}),
            'begindate': forms.SelectDateWidget({'class': 'form-control field form-control-sm'}),
            'enddate': forms.SelectDateWidget({'class': 'form-control field form-control-sm'}),

        }



    def clean_section(self):
        name_= self.cleaned_data.get('name')
        section_ = self.cleaned_data.get('section')
        if self.instance.id:
            if self.instance.name == name_ and self.instance.section == section_:
                return section_

        if models.Class.objects.filter(name= name_,section= section_).exists():

            raise forms.ValidationError("Class Name with this section already exists.")
        return section_


    def clean_enddate(self):
        b_date = self.cleaned_data.get('begindate')
        e_date = self.cleaned_data.get('enddate')
        if e_date <= b_date:
            raise forms.ValidationError("End Date Must be greater than Begin Date")
        return e_date

class EnrolmentForm(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields ='__all__'
        widgets = {
            'student' : forms.NumberInput({'class' : 'form-control field form-control-sm','placeholder':'Student ID'}),
            'clas' : forms.NumberInput({'class' : 'form-control field form-control-sm'})
        }
        # have to add enrollment clean logic 


def batch():
    return [('all','all')]+list(models.Batch.objects.all().values_list('year','year').order_by('-year'))
def clas():
    return [('all','all')]+list(models.Class.objects.all().values_list('id','name').order_by('-name'))


class StFilter(forms.Form):
    class_selector = forms.ChoiceField(widget=forms.Select({'class' : 'form-control '}),label='Class',choices=clas)
    batch_selector = forms.ChoiceField(widget=forms.Select({'class': 'form-control'}),label='Batch',choices=batch)


    def get_Students(self):
        Class = self.cleaned_data['class_selector']





class EditStudent(forms.ModelForm):
    class Meta:
        model= models.Students
        fields ='__all__'
        widgets = {
            'firstname' : forms.TextInput({'class' : 'form-control field form-control-sm','placeholder':"Student's First Name"}),
            'lastname'   : forms.TextInput({'class' : 'form-control field form-control-sm','placeholder':"Student's Last Name"}),
            'fathername' : forms.TextInput({'class' : 'form-control field form-control-sm','placeholder':"Father's Name"}),
            'fatherscnic' : forms.NumberInput({'class' : 'form-control field form-control-sm','placeholder':"Father's CNIC"}),
            'studentscnic' : forms.NumberInput({'class' : 'form-control field form-control-sm','placeholder':"Student's CNIC"}),
            'fathersnumber' : forms.NumberInput({'class' : 'form-control field form-control-sm','placeholder':"Fathers's Contact Number"}),
            'studentsnumber' : forms.NumberInput({'class' : 'form-control field form-control-sm','placeholder':"Student's Contact Number"}),
            'batch' : forms.Select({'class' : 'form-control field'}),
        }



    def clean_firstname(self):
        st_fN = self.cleaned_data.get('firstname')
        st_fN = name_Cleaner(st_fN)
        return st_fN

    def clean_lastname(self):
        st_lN = self.cleaned_data.get('lastname')
        st_lN = name_Cleaner(st_lN)
        return st_lN

    def clean_fathername(self):
        st_fN = self.cleaned_data.get('fathername')
        st_fN = name_Cleaner(st_fN)
        return st_fN


    def clean_fatherscnic(self):
        cnic = self.cleaned_data.get('fatherscnic')
        if len(str(cnic))!=13 :
            raise forms.ValidationError("Enter valid CNIC number.")
        return cnic

    def clean_studentscnic(self):
        cnic = self.cleaned_data.get('studentscnic')
        if len(str(cnic)) != 13:
            raise forms.ValidationError("Enter valid CNIC number.")
        return cnic
    def clean_studentsnumber(self):
        number = self.cleaned_data.get('studentsnumber')
        if len(str(number)) != 10:
            raise forms.ValidationError("Enter valid contact number.")
        return number


    def clean_fathersnumber(self):
        number = self.cleaned_data.get('fathersnumber')
        if len(str(number)) != 10:
            raise forms.ValidationError("Enter valid contact number.")
        return number



