import json
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Student,Alumni,Company
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


Dep_choices = (# tuple of (what appears in the backend,what appears in frontend)
    ("Computer Science and Engineering","Computer Science and Engineering"),
    ("Electronics and Electrical Communications Engineering","Electronics and Electrical Communications Engineering"),
    ("Electrical Engineering","Electrical Engineering"),
    ("Mechanical Engineering","Mechanical Engineering"),
)

Profiles_choices =(
    ("SD","Software Develepment"),
    ("DA","Data Analytics"),
)

Profiles_edit_choices =(
    ("NO","No new CV to upload"),
    ("SD","Software Develepment"),
    ("DA","Data Analytics"),
    ("DL","Delete my uploaded CVs"),
)

class StudentSignUpForm(UserCreationForm):#form and formfields defined
    roll_number =forms.CharField(required=True)
    department = forms.ChoiceField(choices=Dep_choices)#choice filed will give a set of choices to user to choose from
    SDprofile = forms.BooleanField(initial=True,label="Software Development",required=False)#required = False denotes that it is not a required filed 
    DAprofile = forms.BooleanField(initial=False,label="Data Analytics",required=False)
    cvprof = forms.ChoiceField(choices=Profiles_choices,label="Choose a Profile to Upload the CV for")
    cv = forms.FileField(label="Upload CV",required=False) 

    class Meta(UserCreationForm.Meta):#Model Meta is basically used to change the behavior of your model fields like changing order options,verbose_name and lot of other options.
        model = User
        # Order of Fields in the Form
        fields = ['email','contact_number','roll_number','department']
    
    def clean_roll_number(self,*args,**kwargs):
        roll_number = self.cleaned_data.get('roll_number').upper()#get the data from form which would be stored in self.cleaned and store it in upper case
        email = self.cleaned_data.get('email') #extract email from form
        # print(email)
        f = open('./accounts/student.json','r')#open json
        inp = json.load(f)

        for x in inp.values():#iterate over json
            if(roll_number == x['roll_number'].upper()):#if roll_number of any object literal matches with the input roll_number
                rolls = Student.objects.all()#extract all student objects to check if the roll_number already exists
                for stu in rolls:
                    if(roll_number==stu.roll_number):
                        raise forms.ValidationError(_("This Roll Number already exist"),code='duplicate_entry')
                if(email!=x['email']):#if the entered email doesn't match with the email id present inside the json file
                    raise forms.ValidationError(_("The Entered data does not match with the records assciated with this Roll Number, please verify the entered details"),code='data_mismatch')
                return roll_number
        raise forms.ValidationError(_("This Roll number does not exist"),code='not_exist')
    flag=0
    
    def clean_SDprofile(self,*args,**kwargs):
        sd = self.cleaned_data.get('SDprofile')#if sd profile is chosen
        # da = self.cleaned_data.get('DAprofile')
        if sd:#if sd profile is chosen
            self.flag=1#set flag=1
        return sd
    def clean_DAprofile(self,*args,**kwargs):
        # sd = self.cleaned_data.get('SDprofile')
        da = self.cleaned_data.get('DAprofile')#check if da is chosen
        if not da and self.flag==0:#if da as well as sd is not chosen 
            raise forms.ValidationError(_("You have to atleast select one Profile"),code="noprofile")
        return da

    def clean_cv(self,*args,**kwargs):
        prof = self.cleaned_data.get('cvprof')
        cv = self.cleaned_data.get('cv')
        sd = self.cleaned_data.get('SDprofile')
        da = self.cleaned_data.get('DAprofile')
        # print(cv,sd,sep="\n")
        if ((prof=='SD' and not sd) or (prof=='DA' and not da)):#if profile chosen and uploaded file's profile mismatches
            raise forms.ValidationError(_("If you want to upload the CV for this profile, then please first select this profile from the checkboxes above"),code="profile_CV_mismatch")
        return cv

    @transaction.atomic  #if an exception occurs changes are not saved
    def save(self):
        user = super().save(commit=False)#before saving save the details
        user.is_student = True
        roll_number = self.cleaned_data.get('roll_number').upper()
        f = open('./accounts/student.json','r')
        inp = json.load(f)

        for x in inp.values():
            if(roll_number == x['roll_number'].upper()):
                user.first_name = x['first_name']#get first_name from json
                user.last_name = x['last_name']#get last_name
        f.close()
        user.contact_number=self.cleaned_data.get('contact_number')
        user.email = self.cleaned_data.get('email')
        user.username = user.email#username will be equal to user's registered id
        user.save()
        
        student = Student.objects.create(user=user)#instance created
        student.department=self.cleaned_data.get('department')
        student.SDprofile = self.cleaned_data.get('SDprofile')
        student.DAprofile = self.cleaned_data.get('DAprofile')
        student.roll_number=self.cleaned_data.get('roll_number').upper()
        prof = self.cleaned_data.get('cvprof')
        
        if(prof=="SD"):
            student.CV_SD = self.cleaned_data.get('cv')
        else:
            student.CV_DA = self.cleaned_data.get('cv')
        
        student.save()
        return user

class StudentEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=12,required=True)
    roll_number =forms.CharField(required=True)
    first_name = forms.CharField(required=True) 
    last_name = forms.CharField(required=True)
    department = forms.CharField(required=True)
    SDprofile = forms.BooleanField(initial=True,label="Software Development",required=False)
    DAprofile = forms.BooleanField(initial=False,label="Data Analytics",required=False)
    cvprof = forms.ChoiceField(choices=Profiles_edit_choices,label="Choose a Profile to Upload CV for(choose No File to Upload, if don't want to upload new CV)",required=True)
    cv = forms.FileField(label="Upload CV",required=False)

    class Meta():
        model = Student
        fields = ['email','contact_number','first_name','last_name','department','SDprofile','DAprofile','cvprof','cv']


    @transaction.atomic  #if an exception occurs changes are not saved
    def save(self):
        prof = self.cleaned_data.get('cvprof')
        return self.cleaned_data.get('contact_number'),self.cleaned_data.get('SDprofile'),self.cleaned_data.get('DAprofile'),prof,self.cleaned_data.get('cv')

class AlumniSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True) 
    last_name = forms.CharField(required=True)
    department = forms.ChoiceField(choices=Dep_choices)
    roll_number =forms.CharField(required=True)
    year_of_graduation = forms.IntegerField(required=True,min_value=1951,max_value=2021)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email','contact_number','roll_number','first_name','last_name','department','year_of_graduation']
    
    @transaction.atomic#if an exception occurs changes are not saved
    def save(self):
        user = super().save(commit=False)#before saving save the details
        user.is_alumni = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.contact_number=self.cleaned_data.get('contact_number')
        user.email = self.cleaned_data.get('email')
        user.username = user.email
        user.save()
        alumni = Alumni.objects.create(user=user)#instance created
        alumni.department=self.cleaned_data.get('department')
        alumni.roll_number=self.cleaned_data.get('roll_number').upper()
        alumni.year_of_graduation=int(self.cleaned_data.get('year_of_graduation'))
        alumni.save()
        return user

class AlumniEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=12,required=True)
    roll_number =forms.CharField(required=True)
    first_name = forms.CharField(required=True) 
    last_name = forms.CharField(required=True)
    department = forms.CharField(required=True)
    year_of_graduation = forms.IntegerField(required=True,min_value=1951,max_value=2021)

    class Meta():
        model = Alumni
        fields = ['email','contact_number','first_name','last_name','department','year_of_graduation']

    @transaction.atomic  #if an exception occurs changes are not saved
    def save(self):
        return self.cleaned_data.get('contact_number')

class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email (Email will be your username for Logging in the portal)")
    contact_number = forms.CharField(max_length=12)
    # first_name = forms.CharField(required=True) 
    # last_name = forms.CharField(required=True)
    profile = forms.CharField(required=True)
    company_name =forms.CharField(required=True)
    address = forms.CharField(required=True)
    profile = forms.ChoiceField(choices=Profiles_choices)
    # overview = forms.Textarea(attrs={"cols": "35", "rows": "10"})
    # work_environ = forms.Textarea(attrs={"cols": "35", "rows": "10"})
    # job_desc = forms.Textarea(attrs={"cols": "35", "rows": "10"})
    # other_details = forms.Textarea(attrs={"cols": "35", "rows": "10"})
    verify_doc = forms.FileField(label="Upload your Verification Documents(Single PDF)",required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email','contact_number','company_name','address','profile'] 
    
    @transaction.atomic#if an exception occurs changes are not saved
    def save(self):
        user = super().save(commit=False)#before saving save the details
        user.is_company = True
        user.contact_number=self.cleaned_data.get('contact_number')
        user.email = self.cleaned_data.get('email')
        user.username = user.email
        user.save()
        company = Company.objects.create(user=user)#instance created
        company.profile=self.cleaned_data.get('profile')
        company.company_name=self.cleaned_data.get('company_name')
        company.address=self.cleaned_data.get('address')
        company.verify_doc = self.cleaned_data.get('verify_doc')
        company.save()
        return user


class CompanydescForm(forms.ModelForm):
    overview = forms.Textarea(attrs={"cols": "35", "rows": "10"})
    work_environ = forms.Textarea(attrs={"cols": "35", "rows": "10"})
    job_desc = forms.Textarea(attrs={"cols": "35", "rows": "10","required": False})
    other_details = forms.Textarea(attrs={"cols": "35", "rows": "10"})

    class Meta:
        model = Company
        fields = ['overview','work_environ','job_desc','other_details']


    @transaction.atomic#if an exception occurs changes are not saved
    def save(self):
        return self.cleaned_data.get('overview'),self.cleaned_data.get('work_environ'),self.cleaned_data.get('job_desc'),self.cleaned_data.get('other_details')

class CompanyEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=12,required=True)
    company_name =forms.CharField(required=True)
    address = forms.CharField(required=True)
    profile = forms.ChoiceField(choices=Profiles_choices)
    overview = forms.Textarea(attrs={"cols": "35", "rows": "10"})
    work_environ = forms.Textarea(attrs={"cols": "35", "rows": "10"})
    job_desc = forms.Textarea(attrs={"cols": "35", "rows": "10"})
    other_details = forms.Textarea(attrs={"cols": "35", "rows": "10"})

    class Meta():
        model = Company
        fields = ['email','contact_number','company_name','address','profile','overview','work_environ','job_desc','other_details']

    @transaction.atomic  #if an exception occurs changes are not saved
    def save(self):
        return self.cleaned_data.get('contact_number'),self.cleaned_data.get('address'),self.cleaned_data.get('profile'),self.cleaned_data.get('overview'),self.cleaned_data.get('work_environ'),self.cleaned_data.get('job_desc'),self.cleaned_data.get('other_details')