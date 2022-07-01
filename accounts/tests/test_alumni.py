from django.test import TestCase
from accounts.form import AlumniSignUpForm
#python manage.py test accounts.tests.test_alumni run this command to run this test file
# this tests object creation with different scenarios (i.e. test of alumni sign up feature)


class TestForms(TestCase):
    
    def test_company_form(self):
        form = AlumniSignUpForm(data={'email': "s2@test.com",'contact_number':"9999999999",'roll_number':"18CS30054",'year_of_graduation':2020, 'first_name':"saransh",'last_name' :"sharma",'password1':"placement",'password2':"placement",'department':"Computer Science and Engineering"})
        print("### Successful Sign up ###")
        print("\n")
        self.assertTrue(form.is_valid())#test will pass only when the entity inside assert true is true 
    
        form = AlumniSignUpForm(data={'email': "s2@",'contact_number':"9999999999",'roll_number':"18CS30054",'year_of_graduation':2020, 'first_name':"saransh",'last_name' :"sharma",'password1':"placement",'password2':"placement",'department':"Computer Science and Engineering"})
        print("### Invalid email format Sign up failure ###")
        print(form.errors)#prints the fields having error
        print("\n")
        self.assertFalse(form.is_valid())#test will pass only when the entity inside assert false is false
        
        form = AlumniSignUpForm(data={'email': "s2@test.com",'contact_number':"",'roll_number':"18CS30054",'year_of_graduation':2020, 'first_name':"saransh",'last_name' :"sharma",'password1':"placement",'password2':"placement",'department':"Computer Science and Engineering"})
        print("### Empty field sign up failure ###")
        print(form.errors)
        print("\n")
        self.assertFalse(form.is_valid())
        
        form = AlumniSignUpForm(data={'email': "s2@test.com",'contact_number':"9999999999",'roll_number':"18CS30054",'year_of_graduation':2020, 'first_name':"saransh",'last_name' :"sharma",'password1':"placement",'password2':"plac",'department':"Computer Science and Engineering"})
        print("### Password mismatch sign up failure ###")
        print(form.errors)
        print("\n")
        self.assertFalse(form.is_valid())