# python manage.py test accounts.tests.test_view run this command to run tests
#this test will check if templates corresponding to views are proper rendered and on mimicking request views.py functions are working properly(using status_code)


from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Student,User
import json
from django.contrib.auth import login

class TestViews(TestCase):
    def setUp(self):
        self.client=Client()#client set up is used for testing in django
        user = User.objects.create(username='testuser')
        user.set_password('12345')#this ensures proper hashing of password
        user.save()
    
    def test_student_register_GET(self):
        response = self.client.get(reverse('student_register'))
        
        print("### student_register page status and template checked ###")
        self.assertEquals(response.status_code,200)#status 200 indicates that a page has been rendered #test will pass only when the entities inside assert equals are equal
        self.assertTemplateUsed(response,'../templates/student_register.html' )#check if proper template is rendered
    
    def test_company_register_GET(self):
        response = self.client.get(reverse('company_register'))
        
        print("### company_register page status and template checked ###")
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'../templates/company_register.html' )
        
    def test_alumni_register_GET(self):
        response = self.client.get(reverse('alumni_register'))
        
        print("### alumni_register page status and template checked ###")
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'../templates/alumni_register.html' )
        
    def test_company_info_GET(self):
        response = self.client.get(reverse('company_info'))
        
        print("### company_info page status and template checked ###")
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'../templates/company_info.html' )
    
    def test_student_edit_GET(self):
        response = self.client.get(reverse('student_edit'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        print("### get page redirect and status checked ###")
        self.assertEquals(last_url,'//')
        self.assertEquals(response.status_code,200)
        
        
    def test_company_edit_GET(self):
        response = self.client.get(reverse('company_edit'), follow=True)
        last_url, status_code = response.redirect_chain[-1]#helps in extraction of redirected link
        print("### get page redirect and status checked ###")
        self.assertEquals(last_url,'//')
        self.assertEquals(response.status_code,200)#since follow=true, status_code=200 even though it is a redirected page
        
    def test_alumni_edit_GET(self):
        response = self.client.get(reverse('alumni_edit'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        print("### get page redirect and status checked ###")
        self.assertEquals(last_url,'//')
        self.assertEquals(response.status_code,200)
        
    def test_request_feedback_GET(self):
        response = self.client.get(reverse('request_feedback'))
        
        print("### request_feedback page status checked ###")
        self.assertEquals(response.status_code,302)#if page is redirected the status_code should be 302
        
    def test_feedback_GET(self):
        response = self.client.get(reverse('feedback'))
        
        print("### feedback page status checked ###")
        self.assertEquals(response.status_code,302)
        
    def test_apply_company(self):
        response = self.client.get(reverse('apply_company'))
        
        print("### apply_company page status checked ###")
        self.assertEquals(response.status_code,302)
        
    
    def test_company_details(self):
        response = self.client.get(reverse('company_details'))
        
        print("### company_details page status checked ###")
        self.assertEquals(response.status_code,302)
    
    
    def test_list_of_students(self):
        response = self.client.get(reverse('list_of_students'))
        
        print("### list of students page status checked ###")
        self.assertEquals(response.status_code,302)
        
    
    
    def test_index(self):
        response = self.client.get(reverse('index'))
        
        print("### feedback page status checked ###")
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'../templates/index.html' )
    
    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        print("### Successful login checked ###")
        if logged_in is True:
            print("--- Successful Login ---")
        else:
            print("--- Invalid Username or Password ---")
        
        d = Client()
        logged_in = d.login(username='testuser', password='12')
        print("### Failed login checked ###")
        
        if logged_in is True:
            print("--- Successful Login ---")
        else:
            print("--- Invalid Username or Password ---")
        
        