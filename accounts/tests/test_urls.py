from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *
from pages.views import index

#python manage.py test accounts.tests.test_urls run this command to run this test file
#this test will check if proper function of views.py is called 

class TestUrls(SimpleTestCase):
    def test_student_register(self):
        url=reverse('student_register')#access the url corresponding to the name 'student_register
        print(resolve(url))#now resolve the url to get the details of the function called when this url is requested
        self.assertEquals(resolve(url).func.view_class, student_register)#check if the function called is the same as expected
        #for class use resolve(url).func.view_class
        #for functions use resolve(url).func
    
    def test_alumni_register(self):
        url = reverse('alumni_register')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,alumni_register)#test will pass only when the entities inside assert equals are equal
        
    
    def test_company_register(self):
        url = reverse('company_register')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,company_register)
    
    def test_company_info(self):
        url = reverse('company_info')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,company_info)
    
    def test_student_edit(self):
        url = reverse('student_edit')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,editStudProfile)
        

    def test_company_edit(self):
        url = reverse('company_edit')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,editCompProfile)
    
    def test_alumni_edit(self):
        url = reverse('alumni_edit')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,editAlumProfile)
    
    def test_request_feedback(self):
        url = reverse('request_feedback')
        print(resolve(url))
        self.assertEquals(resolve(url).func,request_feedback)
    
    def test_feedback(self):
        url = reverse('feedback')
        print(resolve(url))
        self.assertEquals(resolve(url).func,feedback)
    
    def test_apply_company(self):
        url = reverse('apply_company')
        print(resolve(url))
        self.assertEquals(resolve(url).func,apply_company)
    
    def test_company_details(self):
        url = reverse('company_details')
        print(resolve(url))
        self.assertEquals(resolve(url).func,company_details)
    
    def test_stud_chat(self):
        url = reverse('stud_chat')
        print(resolve(url))
        self.assertEquals(resolve(url).func,stud_chat)
    
    def test_list_of_students(self):
        url = reverse('list_of_students')
        print(resolve(url))
        self.assertEquals(resolve(url).func,list_of_students)
        
    def test_get_stud_cv(self):
        url = reverse('get_stud_cv')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_stud_cv)
        
    def test_get_cv(self):
        url = reverse('get_cv')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_cv)

    def test_index(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func,index)

    def test_login(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func,login_request)

    def test_logout(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func,logout_view)