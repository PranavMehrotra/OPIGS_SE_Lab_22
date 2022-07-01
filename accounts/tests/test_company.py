from django.test import TestCase
from accounts.form import CompanySignUpForm
#python manage.py test accounts.tests.test_company run this command to run this test file
# this tests object creation with different scenarios (i.e. test of company sign up feature)

class TestForms(TestCase):
    
    def test_company_form(self):
        form = CompanySignUpForm(data={'email': "s2@test.com",'contact_number':"9999999999", 'address' :"Mundra,Kutch",'profile' :"SD",'password1':"placement",'password2':"placement",'company_name':'tata'})
        print("### Successful Sign up ###")
        print("\n")
        print(form.errors)
        self.assertTrue(form.is_valid())#test will pass only when the entity inside assert true is true
    
        form = CompanySignUpForm(data={'email': "s2@",'contact_number':"9999999999", 'address' :"Mundra,Kutch",'profile' :"SD",'password1':"placement",'password2':"placement",'company_name':'tata'})
        print("### invalid Email format Sign up ###")
        print(form.errors)
        print("\n")
        self.assertFalse(form.is_valid())
 
        form = CompanySignUpForm(data={'email': "s2@test.com",'contact_number':"9999999999", 'address' :"Mundra,Kutch",'profile' :"SD",'password1':"place",'password2':"placement",'company_name':'tata'})
        print("### Password mismatch sign up failure ###")
        print(form.errors)
        print("\n")
        self.assertFalse(form.is_valid())
 
        form = CompanySignUpForm(data={'email': "s2@test.com",'contact_number':"9999999999", 'address' :"",'profile' :"SD",'password1':"placement",'password2':"placement",'company_name':'tata'})
        print("### Empty field sign up failure ###")
        print(form.errors)
        print("\n")
        self.assertFalse(form.is_valid())
 
        
       