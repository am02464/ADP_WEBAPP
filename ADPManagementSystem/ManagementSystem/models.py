from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=4,null=False)
    password = models.CharField(max_length=4,null=False)



class UC_Chapter(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    name = models.TextField()
    discription = models.TextField()


    def __str__(self):
        return str(self.name)

class Section(models.Model):
    name = models.CharField(max_length=30,verbose_name='Section Name', help_text='add section name here')
    def __str__(self):
        return str(self.id)

class Class(models.Model):
    name = models.CharField(max_length=30,verbose_name='Class Name', help_text='add class name here')
    section = models.ForeignKey(Section,on_delete=models.SET_NULL,null=True,blank=True)#.IntegerField(verbose_name='Section',help_text='add section name here')
    begindate = models.DateField(null=False,blank=False,verbose_name= 'Begin Date',help_text='add begin date here')
    enddate = models.DateField(null=False,blank=False,verbose_name= 'End Date',help_text='add end date here')

    def __str__(self):
        return self.name

class Batch(models.Model):
    year = models.IntegerField(primary_key=True)
    def __str__(self):
        return str(self.year)




class Students(models.Model):
    firstname = models.CharField(max_length=30,verbose_name='First Name', help_text='add first name here',null=False,blank=False)
    lastname = models.CharField(max_length=30,verbose_name='Last Name', help_text='add last name here',null=False,blank=False)
    fathername = models.CharField(max_length=30,verbose_name='Father\'s Name', help_text='add last name here',null=False,blank=False)
    fatherscnic = models.BigIntegerField(max_length=13,verbose_name='Guardian\'s CNIC Number',help_text='Guardian\'s CNIC Number here',blank=False,null=False)
    studentscnic = models.BigIntegerField(max_length=13,verbose_name='Guardian\'s CNIC Number',help_text='Guardian\'s CNIC Number here',blank=False,null=False)
    fathersnumber = models.BigIntegerField(max_length=11,verbose_name='Guardian\'s CNIC Number',help_text='Guardian\'s CNIC Number here',blank=False,null=False)
    studentsnumber = models.BigIntegerField(max_length=11,verbose_name='Guardian\'s CNIC Number',help_text='Guardian\'s CNIC Number here',blank=False,null=False)
    batch = models.ForeignKey(Batch,on_delete=models.SET_NULL,null=True)
    def getFullName(self):
        return str(self.firstname +' '+ self.lastname)

    def __str__(self):
        return self.getFullName()


class Enrollment(models.Model):
    student = models.ForeignKey(Students,on_delete=models.CASCADE,primary_key=True)
    clas = models.ForeignKey(Class,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return str(self.student_id)













