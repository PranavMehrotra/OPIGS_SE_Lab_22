from django.test import TestCase
from accounts.form import StudentSignUpForm
# python manage.py test accounts.tests.test_student run this command to run this test file
# this tests object creation with different scenarios (i.e. test of student sign up feature)


class TestForms(TestCase):

    
    def test_student_form(self):
        form = StudentSignUpForm(data={'email': "s2@test.com",'contact_number':"98", 'roll_number' :"20cs10006", 'department' :"Computer Science and Engineering",'SDprofile' : True, 'DAprofile' : False,'cvprof' : "SD",'password1':"placement",'password2':"placement"})
        print("### Successful Sign up ###")
        print("\n")
        self.assertTrue(form.is_valid())#test will pass only when the entity inside assert true is true
        
        form = StudentSignUpForm(data={'email': "s2@test.com",'contact_number':"98", 'roll_number' :"20cs10006", 'department' :"Computer Science and Engineering",'SDprofile' : True, 'DAprofile' : False,'cvprof' : "SD",'password1':"place",'password2':"placement"})
        print("### Password mismatch Sign up ###")
        print(form.errors)#prints the point of error
        print("\n")
        self.assertFalse(form.is_valid())#form isn't valid
        
        form = StudentSignUpForm(data={'email': "",'contact_number':"", 'roll_number' :"", 'department' :"",'SDprofile' : True, 'DAprofile' : False,'cvprof' : "SD",'password1':"placement",'password2':"placement"})
        print("### Empty field Sign up ###")
        print(form.errors)
        print("\n")
        self.assertFalse(form.is_valid())
        
        form = StudentSignUpForm(data={'email': "s2@test.com",'contact_number':"9999999999", 'roll_number' :"20cs10085",'department' :"Computer Science and Engineering",'SDprofile' : True, 'DAprofile' : False,'cvprof' : "SD",'password1':"placement",'password2':"placement"})
        print("### Roll number doesn't exist in json file Sign up ###")
        print(form.errors)#prints the point of error
        print("\n")
        self.assertFalse(form.is_valid())#form isn't valid
        
        form = StudentSignUpForm(data={'email': "s3@test.com",'contact_number':"9999999999", 'roll_number' :"20cs10006",'department' :"Computer Science and Engineering",'SDprofile' : True, 'DAprofile' : False,'cvprof' : "SD",'password1':"placement",'password2':"placement"})
        print("### Email doesn't match with the registered email id Sign up ###")
        print(form.errors)#prints the point of error
        print("\n")
        self.assertFalse(form.is_valid())#form isn't valid
    
       