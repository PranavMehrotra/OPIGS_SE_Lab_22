from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import *
from django.contrib.auth.forms import AuthenticationForm
from .models import Company, Student, User, Notification,Chat
from django.core.mail import send_mail
from django.conf import settings

def register(request):
    return render(request, '../templates/register.html')
    
class student_register(CreateView):
    form_class = StudentSignUpForm #student form specified
    template_name = '../templates/student_register.html' #template spcified

    def form_valid(self, form): #form valid check
        user = form.save() #save the form
        login(self.request, user) #login the user
        return redirect('/accounts/index') #redirect to main index page
    
class alumni_register(CreateView):
    model = User
    form_class = AlumniSignUpForm
    template_name = '../templates/alumni_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/accounts/index')
    
class company_register(CreateView):
    form_class = CompanySignUpForm
    template_name = '../templates/company_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/accounts/company_info')

class company_info(CreateView):
    model = Company
    form_class = CompanydescForm
    template_name = '../templates/company_info.html'

    def form_valid(self, form):
        # print(self.request.user)
        company = User.objects.get(username = (self.request.user))
        comp = Company.objects.get(user=company)
        # print(company)
        overvie,work_enviro,job_des,other_detail = form.save()
        e_mess_admin = "Company called <b>" + str(comp.company_name) + "</b> is trying to apply for recruitment process in your college.<br>Please visit the admin portal to see the details about the Company and the verification document uploaded by the Company Admin.<br><br><strong>After successful verification you can make the company status Active, so that company can participate in the placement process.</strong><br><br><br>Best,<br>OPIGS Team<br><br>"
        e_mess_comp = "Thanks <b>" + str(comp.company_name) + "</b> for applying for the recruitment process in our college.<br>We have recieved your data and the Institute administrator has been informed about your application.<br><br><strong>You will not be able to login into the portal until your application is in the verification process.<br>After successful verification from Institute Adminstrator, you will be able to login in to the portal and the students will be able to see your company details and apply for the jobs offered by your company.</strong><br><br>For any further queries, please contact the Institute Administrator.<br><br>Best,<br>OPIGS Team<br><br>"
        send_mail(
            "NEW COMPANY TRYING TO APPLY FOR PLACEMENT PROCESS", #subject
            "", #message
            "opigs.iitkgp@gmail.com", #from_email
            ["iitkgp.placement@gmail.com"], #to_email_list
            fail_silently=True,
            html_message= e_mess_admin
        )
        send_mail(
            "REQUEST FOR RECRUITING RECIEVED", #subject
            "", #message
            "opigs.iitkgp@gmail.com", #from_email
            [company.email], #to_email_list
            fail_silently=True,
            html_message= e_mess_comp
        )
        Company.objects.filter(user = (company)).update(overview= overvie,work_environ= work_enviro,job_desc=job_des,other_details=other_detail)#search for the company whose data has been enetered and then update the details there 
        company.is_active=False #company will be active only after manual verification by the admin
        company.save()
        # print(overvie,work_enviro,job_des,other_detail)
        return redirect('/accounts/index')

class editStudProfile(CreateView):
    model = Student
    form_class = StudentEditForm
    template_name = '../templates/edit_details.html'

    def get(self,request):
        if(self.request.user.is_authenticated):#if request is from an authenticated user
            user = User.objects.get(username = (self.request.user))#get the user using the username
            student = Student.objects.get(user = user)#get the student object from database by passing user as parameter
            values = {#initialise values with the existing data
                'email':user.email,
                'contact_number':user.contact_number,
                'roll_number':student.roll_number,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'department':student.department,
                'SDprofile':student.SDprofile,
                'DAprofile':student.DAprofile,
                'cvprof': "NO",
                'CV_DA': None
            }
            form = StudentEditForm(values)
            form.fields['email'].widget.attrs['readonly']  =True#set the read only fields which cannot be altered
            form.fields['roll_number'].widget.attrs['readonly']  =True
            form.fields['first_name'].widget.attrs['readonly']  =True
            form.fields['last_name'].widget.attrs['readonly']  =True
            form.fields['department'].widget.attrs['readonly']  =True
            # print(values)
            return render(request,'../templates/edit_details.html',{'whereto':'student_edit','form':form})#display the form in the edit_details.html
        return redirect('/accounts/index')

    def form_valid(self,form):#form valid function
        if(self.request.user.is_authenticated):
            user = User.objects.get(username = (self.request.user))
            student = Student.objects.get(user = user)
            contact_number, SDprofile,DAprofile,prof,cv = form.save()#get data from form
            user.contact_number=contact_number
            student.SDprofile=SDprofile
            student.DAprofile=DAprofile
            # print(cv)
            # print(cv.size)
            if(prof=="SD" and cv!=None):
                if(student.CV_SD):
                    student.CV_SD.delete()#delete the previously stored file
                student.CV_SD = cv#store the new file
            elif(prof=="DA" and cv!=None):
                if(student.CV_DA):
                    student.CV_DA.delete()
                student.CV_DA = cv
            elif(prof=="DL"):#delete both the CV's
                if(student.CV_SD):
                    student.CV_SD.delete()
                if(student.CV_DA):
                    student.CV_DA.delete()
                    
                student.CV_SD = None
                student.CV_DA = None
            user.save()
            student.save()
        return redirect('/accounts/index')

class editCompProfile(CreateView):
    model = Company
    form_class = CompanyEditForm
    template_name = '../templates/edit_details.html'

    def get(self,request):
        if(self.request.user.is_authenticated):
            user = User.objects.get(username = (self.request.user))
            company = Company.objects.get(user = user)
            values = {
                'email':user.email,
                'contact_number':user.contact_number,
                'company_name' : company.company_name,
                'address' : company.address,
                'profile' : company.profile,
                'overview' : company.overview,
                'work_environ' : company.work_environ,
                'job_desc' : company.job_desc,
                'other_details' : company.other_details
            }
            form = CompanyEditForm(values)
            form.fields['email'].widget.attrs['readonly']  =True
            form.fields['company_name'].widget.attrs['readonly']  =True
            # print(values)
            return render(request,'../templates/edit_details.html',{'whereto':'company_edit','form':form})
        return redirect('/accounts/index')

    def form_valid(self,form):
        if(self.request.user.is_authenticated):
            user = User.objects.get(username = (self.request.user))
            company = Company.objects.get(user = user)
            contact_number, address,profile,overview,work_environ,job_desc,other_details = form.save()
            user.contact_number=contact_number
            company.profile = profile
            company.address = address
            company.overview = overview
            company.work_environ = work_environ
            company.job_desc = job_desc
            company.other_details =other_details
            user.save()
            company.save()
        return redirect('/accounts/index')


class editAlumProfile(CreateView):
    model = Alumni
    form_class = AlumniEditForm
    template_name = '../templates/edit_details.html'

    def get(self,request):
        if(self.request.user.is_authenticated):
            user = User.objects.get(username = (self.request.user))
            alumni = Alumni.objects.get(user = user)
            values = {
                'email':user.email,
                'contact_number':user.contact_number,
                'roll_number':alumni.roll_number,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'department':alumni.department,
                'year_of_graduation':alumni.year_of_graduation
            }
            form = AlumniEditForm(values)
            form.fields['email'].widget.attrs['readonly']  =True
            form.fields['roll_number'].widget.attrs['readonly']  =True
            form.fields['first_name'].widget.attrs['readonly']  =True
            form.fields['last_name'].widget.attrs['readonly']  =True
            form.fields['department'].widget.attrs['readonly']  =True
            form.fields['year_of_graduation'].widget.attrs['readonly']  =True
            # print(values)
            return render(request,'../templates/edit_details.html',{'whereto':'alumni_edit','form':form})
        return redirect('/accounts/index')

    def form_valid(self,form):
        if(self.request.user.is_authenticated):
            user = User.objects.get(username = (self.request.user))
            alumni = Alumni.objects.get(user = user)
            contact_number = form.save()
            user.contact_number=contact_number
            user.save()
        return redirect('/accounts/index')



def login_request(request):
    if request.method=='POST':#all requests withing the software are post and requests betwenn user and software is get
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():#if form is valid
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)#chcek if the entered details are correct
            if user is not None :#if a user with the credential exists
                login(request,user)#login to that user
                return redirect('/accounts/index')#redirect to the main page
            else:
                messages.error(request,"Invalid username or password")#else display error message
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',#return to the template
    context={'form':AuthenticationForm()})

def logout_view(request):#logout request
    logout(request)#logout 
    return redirect('/accounts/index')#redirect to accounts/index that will call index function


def get_cv(request):
    if (request.method == 'GET'):
        if(request.user.is_authenticated):#if user is authenticated that is request made after logging in
            user = User.objects.get(username = (request.user))
            student = Student.objects.get(user = user)#get the user first corresponding to that credential and then extract the student using this user
            cvs = {#extract cv
                'sd' : student.CV_SD,
                'da' : student.CV_DA
            }
            """ print(student.CV_SD)
            print(type(student.CV_SD))
             """
            notif = Notification.objects.all().order_by('-Date')
            return render(request,'../templates/index.html',{'cvs':cvs,'student':student,'notif':notif})#pass the extracted cv and other parameters required to index.html
        return redirect('/accounts/index')

def str_to_lis(s):#to convert a string with comma seperated emails to a list of emails
    if(s==""):
        a=[]
        return a
    return s.split(',')

def lis_to_str(b):#convert a list of emails to a string of comma sepearted string
    if len(b)==0:
        return ""
    a = str(b[0])
    for x in b:
        if(x==b[0]):
            continue
        else:
            a+= ',' + x
    return a

def remove_alum_pend(alumni_username,student_username):#to remove alumni from pending list
    
    alumni = User.objects.get(username=alumni_username)
    alumni = Alumni.objects.get(user = alumni)#first extract alumni using user with alumni_username
    student = User.objects.get(username=student_username)
    student = Student.objects.get(user = student)#extract student using user with student_username
    
    alu= str_to_lis(alumni.list_of_stud_pend)#extract list of students pending from alumni database
    stu= str_to_lis(student.list_of_alum_pend)#extract list of alumni pending from student database

    for x in alu:
        if(x == student.user.username):
            alu.remove(x)#remove from pending list
            
    for x in stu:
        if(x == alumni.user.username):
            stu.remove(x)#remove from student list
            
    alumni.list_of_stud_pend = lis_to_str(alu)#update the list
    student.list_of_alum_pend = lis_to_str(stu)#update the list

    alumni.save()
    student.save()
    return student.list_of_alum_pend, alumni.list_of_stud_pend


def add_alum_pend(alumni_user_id,student_user_id):#add to pending list
    alumni_user = User.objects.get(username = (alumni_user_id))
    student_user = User.objects.get(username = (student_user_id))
    alumni = Alumni.objects.get(user=alumni_user)#extract alumni object
    student = Student.objects.get(user=student_user)#extract student object
    
    alu= str_to_lis(alumni.list_of_stud_pend)
    stu= str_to_lis(student.list_of_alum_pend)
    
    alu_username = alumni_user.username
    stu_username = student_user.username
    if stu_username not in alu:
        alu.append(stu_username) #append the username to the list
    if alu_username not in stu:
        stu.append(alu_username)
    alumni.list_of_stud_pend = lis_to_str(alu)#convert the list to comma sepearted string 
    student.list_of_alum_pend = lis_to_str(stu)
    
    alumni.save()
    student.save()
    return

def add_alum(alumni_user_id,student_user_id):
    alumni_user = User.objects.get(username = (alumni_user_id))
    student_user = User.objects.get(username = (student_user_id))
    alumni = Alumni.objects.get(user=alumni_user)
    student = Student.objects.get(user=student_user)
    alu= str_to_lis(alumni.list_of_stud)#list of student is students with which the alumni has already talked
    stu= str_to_lis(student.list_of_alum)
    alu_username = alumni_user.username
    stu_username = student_user.username
    if stu_username not in alu:
        alu.append(stu_username)
    if alu_username not in stu:
        stu.append(alu_username)
    # print(alu,stu)
    
    alumni.list_of_stud = lis_to_str(alu)
    student.list_of_alum = lis_to_str(stu)
    
    alumni.save()
    student.save()
    return

def list_of_students(request):
    if(request.method == 'GET'):
        if(request.user.is_authenticated):
            if(request.user.is_company):
                user = User.objects.get(username = (request.user))
                comp = Company.objects.get(user = user) #extract company of user = request.user
                lis_of_studs = str_to_lis(comp.list_of_students)#list of students
                list_of_short_studs = str_to_lis(comp.list_of_short_students)#list of shortlisted students
                list_of_studs = []
                stud_detail = {}
                for stud in lis_of_studs:#iterate over list
                    suser = User.objects.get(username = stud) #get student
                    stud_detail['first_name']= suser.first_name
                    stud_detail['last_name']= suser.last_name
                    stud_detail['id']= suser.username
                    list_of_studs.append(stud_detail.copy())#add the relevant details to the list
                return render(request,'../templates/list_of_students.html',{'whereto':'list_of_students','list_of_studs':list_of_studs,'list_of_short_studs':list_of_short_studs})
        return redirect('/accounts/index')
    if(request.method == 'POST'):
        if(request.user.is_authenticated):
            if(request.user.is_company):#if request made by student
                user = User.objects.get(username = (request.user))
                comp = Company.objects.get(user = user)
                lis_of_studs = str_to_lis(comp.list_of_students)
                list_of_short_studs = str_to_lis(comp.list_of_short_students)
                list_of_studs = []
                stud_detail = {}
                for stud in lis_of_studs:
                    suser = User.objects.get(username = stud)
                    stud_detail['first_name']= suser.first_name
                    stud_detail['last_name']= suser.last_name
                    stud_detail['id']= suser.username
                    list_of_studs.append(stud_detail.copy())
                stud_username = request.POST.get("stud_id")
                if (stud_username!=None):
                    stud_user = User.objects.get(username = (stud_username))
                    student = Student.objects.get(user = stud_user)
                    if(comp.profile == "SD"):
                        if(student.CV_SD):
                            return redirect(student.CV_SD.url)
                        else:
                            flag=student.user.username
                            return render(request,'../templates/list_of_students.html',{'whereto':'list_of_students','list_of_studs':list_of_studs,'list_of_short_studs':list_of_short_studs,'flag':flag})
                    elif(comp.profile == "DA"):
                        if(student.CV_DA):
                            return redirect(student.CV_DA.url)
                        else:
                            flag=student.user.username
                            return render(request,'../templates/list_of_students.html',{'whereto':'list_of_students','list_of_studs':list_of_studs,'list_of_short_studs':list_of_short_studs,'flag':flag})
        
                else:
                    stud_username = request.POST.get("stud_shortlist_id") #to send email to shortlisted students
                    if (stud_username!=None):
                        stud_user = User.objects.get(username = (stud_username))
                        student = Student.objects.get(user = stud_user)
                        list_of_short_studs = str_to_lis(comp.list_of_short_students)
                        if stud_username not in list_of_short_studs:
                            list_of_short_studs.append(stud_username)
                            comp.list_of_short_students = lis_to_str(list_of_short_studs)
                            comp.save()
                            e_mess_stud = "Congrats <b>" + str(stud_user.first_name) + ", "+str(student.roll_number) + "</b> you have been shortlisted by a company named <b>"+str(comp.company_name)+"</b><br>Further information about the further rounds of placement process will be conveyed by the Company Administrator via Email.<br><br>For any queries, you can contact the Institute Admin or you can also contact the Company Admin at <b>"+str(user.email)+"</b><br><br>Best,<br>OPIGS Team<br><br>"
                            send_mail(
                                "SHORTLISTED BY A COMPANY", #subject
                                "", #message
                                "opigs.iitkgp@gmail.com", #from_email
                                [stud_user.email], #to_email_list
                                fail_silently=True,
                                html_message= e_mess_stud
                            )
                list_of_short_studs = str_to_lis(comp.list_of_short_students)
                return render(request,'../templates/list_of_students.html',{'whereto':'list_of_students','list_of_studs':list_of_studs,'list_of_short_studs':list_of_short_studs})
        return redirect('/accounts/index')


def request_feedback(request):#funct to request feedback from alumni
    if(request.method == 'GET'):
        if(request.user.is_authenticated):
            alum_users = User.objects.filter(is_alumni = True)#extract all alumni
            return render(request,'../templates/request_feedback.html',{'whereto':'request_feedback','alum_users':alum_users})#return the list of alums in case of get request
        return redirect('/accounts/index')

    if(request.method == 'POST'):#post request would be made once user clicks on button
        if(request.user.is_authenticated):
            alum_users = User.objects.filter(is_alumni = True)
            alum_username = request.POST.get("alum_id")#get the id of the alum using the button clicked
            add_alum_pend(alum_username,request.user)#add it to pending list
            return render(request,'../templates/request_feedback.html',{'whereto':'request_feedback','alum_users':alum_users})
        return redirect('/accounts/index')

def feedback(request):#func to give feedback
    if(request.method == 'GET'):
        if(request.user.is_authenticated):
            stud = User.objects.get(username = request.user)
            alum=Alumni.objects.get(user=stud)
            stud_list=str_to_lis(alum.list_of_stud_pend)
            list_of_studs = []
            stud_detail = {}
            for stud in stud_list:
                suser = User.objects.get(username = stud)
                student = Student.objects.get(user = suser)
                stud_detail['first_name']= suser.first_name
                stud_detail['last_name']= suser.last_name
                stud_detail['id']= suser.username
                if(student.CV_SD):
                    stud_detail['sd']= student.CV_SD.url
                if(student.CV_DA):
                    stud_detail['da']= student.CV_DA.url
                list_of_studs.append(stud_detail.copy())
                stud_detail.clear()
            return render(request,'../templates/feedback.html',{'whereto':'feedback','stud_list':list_of_studs})#display list of students and related information in case of get request
        return redirect('/')

    if(request.method == 'POST'):
        if(request.user.is_authenticated):
            stud_username = request.POST.get("alum_id")#get the student corresponding to whom the button is clicked
            message = request.POST.get("feed")
            chat=Chat.objects.create()#create a chat to store this feedback
            chat.stud_username = stud_username
            chat.alum_username = request.user.username
            chat.Sender = 'A'#chat of sender alumni
            chat.chat = message
            chat.save()
            stud,alum = remove_alum_pend(request.user,stud_username)
            add_alum(request.user.username,stud_username)
            stud = User.objects.get(username = request.user)
            alum=Alumni.objects.get(user=stud)
            stud_list=str_to_lis(alum.list_of_stud_pend)
            list_of_studs = []
            stud_detail = {}
            for stud in stud_list:
                suser = User.objects.get(username = stud)
                student = Student.objects.get(user = suser)
                stud_detail['first_name']= suser.first_name
                stud_detail['last_name']= suser.last_name
                stud_detail['id']= suser.username
                if(student.CV_SD):
                    stud_detail['sd']= student.CV_SD.url
                if(student.CV_DA):
                    stud_detail['da']= student.CV_DA.url
                list_of_studs.append(stud_detail.copy())
                stud_detail.clear()
            return render(request,'../templates/feedback.html',{'whereto':'feedback','stud_list':list_of_studs})
        return redirect('/')

def get_stud_cv(request):#to get cv
     if(request.method == 'POST'):
        if(request.user.is_authenticated):
            stud_username = request.POST.get("alum_id")#get the username of student using the button
            stud_user = User.objects.get(username = (stud_username))
            student = Student.objects.get(user = stud_user)
            if(student.CV_SD):
                return redirect(student.CV_SD.url)
            else:
                flag=student.user.username

def chats(request):
     if(request.user.is_student):
        if(request.method == 'GET'):#if student wants to chat
            user=User.objects.get(username = request.user.username)
            student=Student.objects.get(user = user)
            clist=str_to_lis(student.list_of_alum)
            list_of_alums = []
            stud_detail = {}
            for stud in clist:
                suser = User.objects.get(username = stud)
                student = Alumni.objects.get(user = suser)
                stud_detail['first_name']= suser.first_name
                stud_detail['last_name']= suser.last_name
                stud_detail['id']= suser.username
                list_of_alums.append(stud_detail.copy())
                stud_detail.clear()
            # print(list_of_alums)
            return render(request,"../templates/list_of_chats.html",{'whereto':'stud_chat','list_of_alums':list_of_alums})#show the list of alums he has talked with
     if(request.user.is_alumni):
        if(request.method == 'GET'):
            user=User.objects.get(username = request.user.username)
            student=Alumni.objects.get(user = user)
            clist=str_to_lis(student.list_of_stud)
            list_of_alums = []
            stud_detail = {}
            for stud in clist:
                suser = User.objects.get(username = stud)
                student = Student.objects.get(user = suser)
                stud_detail['first_name']= suser.first_name
                stud_detail['last_name']= suser.last_name
                stud_detail['id']= suser.username
                list_of_alums.append(stud_detail.copy())
                stud_detail.clear()
            # print(list_of_alums)
            return render(request,"../templates/list_of_chats.html",{'whereto':'stud_chat','list_of_alums':list_of_alums})#show the list of students he has talked with
        
def stud_chat(request):
    if(request.user.is_student):
        if(request.method == 'GET'):#in case of getv request
            if(request.user.is_authenticated):
                user=User.objects.get(username = request.user.username)
                student=Student.objects.get(user = user)
                alum_username = request.GET.get("alum_id")
                clist=str_to_lis(student.list_of_alum)
                plist=[]
                for x in clist:
                    if x==alum_username:
                        plist.append(x)
                chat=Chat.objects.filter(stud_username = request.user.username)
            return render(request,"../templates/stud_chat.html",{'whereto':'stud_chat','chat':chat,'alum':plist})
        
        if(request.method == 'POST'):
            if(request.user.is_authenticated):
                alum_username = request.POST.get("alum_id")
                
                message = request.POST.get("feed")
                
                chat=Chat.objects.create()#create a new chat object
                chat.stud_username = request.user.username
                chat.alum_username = alum_username
                chat.Sender = 'S'
                chat.chat = message
                if len(message) != 0:
                    chat.save()
                user=User.objects.get(username = request.user.username)
                student=Student.objects.get(user = user)
                clist=str_to_lis(student.list_of_alum)
                plist=[]
                for x in clist:
                    if x==alum_username:
                        plist.append(x)
                chat= Chat.objects.filter(stud_username = request.user.username)
                return render(request,'../templates/stud_chat.html',{'whereto':'stud_chat','chat':chat,'alum':plist})
            
    if(request.user.is_alumni):#if laumni wants to contact
            if(request.method == 'GET'):
                if(request.user.is_authenticated):
                    user=User.objects.get(username = request.user.username)
                    alumni=Alumni.objects.get(user = user)
                    stud_username = request.GET.get("alum_id")
                    clist=str_to_lis(alumni.list_of_stud)
                    plist=[]
                    for x in clist:
                        if x==stud_username:
                            plist.append(x)
                    chat=Chat.objects.filter(alum_username = request.user.username)
                return render(request,"../templates/stud_chat.html",{'whereto':'stud_chat','chat':chat,'alum':plist})
            
            if(request.method == 'POST'):
                if(request.user.is_authenticated):
                    stud_username = request.POST.get("alum_id")
                    
                    message = request.POST.get("feed")
                    
                    chat=Chat.objects.create()
                    chat.stud_username = stud_username
                    chat.alum_username = request.user.username
                    chat.Sender = 'A'
                    chat.chat = message
                    if len(message) != 0:
                        chat.save()
                    user=User.objects.get(username = request.user.username)
                    alumni=Alumni.objects.get(user = user)
                    clist=str_to_lis(alumni.list_of_stud)
                    plist=[]
                    for x in clist:
                        if x==stud_username:
                            plist.append(x)
                    chat= Chat.objects.filter(alum_username = request.user.username)
                    return render(request,'../templates/stud_chat.html',{'whereto':'stud_chat','chat':chat,'alum':plist})


def add_stu_to_comp(company_user_id,student_user_id):
    company_user = User.objects.get(username = (company_user_id))
    student_user = User.objects.get(username = (student_user_id))
    company = Company.objects.get(user=company_user)
    student = Student.objects.get(user=student_user)
    comp= str_to_lis(company.list_of_students)
    stu= str_to_lis(student.list_of_comp)
    comp_username = company_user.username
    stu_username = student_user.username
    if stu_username not in comp:
        comp.append(stu_username)
    if comp_username not in stu:
        stu.append(comp_username)
    company.list_of_students = lis_to_str(comp)
    student.list_of_comp = lis_to_str(stu)
    company.save()
    student.save()
    return


def apply_company(request):
    if(request.method == 'GET'):
        if(request.user.is_authenticated):
            user = User.objects.get(username = (request.user))
            student = Student.objects.get(user = user)
            # comp_users = User.objects.filter(is_company = True)
            if (student.SDprofile  and student.DAprofile):
                # print("SD and DA")
                comps = Company.objects.filter(user__is_active=True)
            elif(student.SDprofile):
                # print("SD")
                comps = Company.objects.filter(user__is_active=True , profile = "SD")
            
            elif(student.DAprofile):
                # print("DA")
                comps = Company.objects.filter(user__is_active=True ,profile = "DA")
            else:
                comps = Company.objects.none()

            applied_comps = str_to_lis(student.list_of_comp)
            return render(request,'../templates/apply_company.html',{'whereto':'apply_company','comps':comps,'applied_comps':applied_comps})
        return redirect('/accounts/index')

    if(request.method == 'POST'):
        if(request.user.is_authenticated):
            comp_username = request.POST.get("comp_id")
            add_stu_to_comp(comp_username,request.user)
            user = User.objects.get(username = (request.user))
            student = Student.objects.get(user = user)
            # comp_users = User.objects.filter(is_company = True)
            if (student.SDprofile  and student.DAprofile):
                # print("SD and DA")
                comps = Company.objects.filter(user__is_active=True)
            elif(student.SDprofile):
                # print("SD")
                comps = Company.objects.filter(user__is_active=True ,profile = "SD")
            
            elif(student.DAprofile):
                # print("DA")
                comps = Company.objects.filter(user__is_active=True ,profile = "DA")
            else:
                comps = Company.objects.none()

            applied_comps = str_to_lis(student.list_of_comp)
            return render(request,'../templates/apply_company.html',{'whereto':'apply_company','comp_details_page':'company_details','comps':comps,'applied_comps':applied_comps})
        return redirect('/accounts/index')

def company_details(request):
    if(request.method == 'POST'):
        if(request.user.is_authenticated):
            comp_username = request.POST.get("comp_id")
            user = User.objects.get(username = comp_username)
            comp = Company.objects.get(user=user)
            return render(request,'../templates/company_details.html',{'comp':comp})
        return redirect('/accounts/index')
    else:
        return redirect('/accounts/index')


def index(request): # to return homepage depending upon the logged in user
    if(request.method == 'GET'):
        if(request.user.is_authenticated):
            if(request.user.is_student):
                user = User.objects.get(username = request.user.username)
                student = Student.objects.get(user = user)
                notif = Notification.objects.all().order_by('-Date')
                return render(request,'../templates/index.html',{'student':student,'notif':notif,'status':1})
            elif(request.user.is_company):
                user = User.objects.get(username = request.user.username)
                company = Company.objects.get(user = user)
                return render(request,'../templates/index.html',{'company':company,'status':1})
            elif(request.user.is_alumni):
                user = User.objects.get(username = request.user.username)
                alumni= Alumni.objects.get(user = user)
                list=str_to_lis(alumni.list_of_stud_pend)
                return render(request,'../templates/index.html',{'alumni':alumni,'stud':list,'status':1})
        return render(request,"../templates/index.html")    
