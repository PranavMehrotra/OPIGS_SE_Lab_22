# python manage.py test accounts.tests.test_models run this command to run this test
# This test will create objects in database, retrieve them from database and then verify them 
from django.test import TestCase,Client
from django.db import IntegrityError
from accounts.models import *

class TestModels(TestCase):
    user = ""
    stud = ""
    alum = ""
    comp = ""
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')#this ensures proper hashing of password
        self.user.is_student = True
        self.user.first_name = "First_Stud1"
        self.user.last_name = "Last_Stud1"
        self.user.contact_number= "9670547821"
        self.user.email = "stud1@test.com"
        self.user.save()
        self.user = User.objects.get(username="testuser")
        user2 = User.objects.create(username='testuser2')
        user2.set_password('12345')#this ensures proper hashing of password
        user2.is_alumni = True
        user2.first_name = "First_Alum1"
        user2.last_name = "Last_Alum1"
        user2.contact_number= "9670547821"
        user2.email = "alum1@test.com"
        user2.save()
        user2 = User.objects.get(username="testuser2")
        
        user3 = User.objects.create(username='testuser3')
        user3.set_password('12345')#this ensures proper hashing of password
        user3.is_company = True
        user3.contact_number= "9670547821"
        user3.email = "comp1@test.com"
        user3.save()
        user3 = User.objects.get(username="testuser3")
        
        self.stud = Student.objects.create(user=self.user)
        self.stud.roll_number = "20CS10085"
        self.stud.department = "Computer Science and Engineering"
        self.stud.SDprofile = True
        self.stud.save()

        self.alum = Alumni.objects.create(user=user2)
        self.alum.roll_number = "15CS10023"
        self.alum.department = "Computer Science and Engineering"
        self.alum.year_of_graduation = 2019
        self.alum.save()

        self.comp = Company.objects.create(user=user3)
        self.comp.company_name = "OPIGS Technologies Ltd."
        self.comp.address = "Demo Address"
        self.comp.profile = "SD"
        self.comp.overview = "Demo Overview"
        self.comp.work_environ = "Demo Work Environment"
        self.comp.job_desc = "Demo Job Description"
        self.comp.other_details = "Demo Other Details"
        self.comp.save()


    def test_all_data_correctly_assigned_to_user(self):
        self.assertTrue(self.user.is_student)
        print("### User is_student check completed ###")
        self.assertEquals(self.user.first_name,"First_Stud1")
        print("### User first_name check completed ###")
        self.assertEquals(self.user.last_name,"Last_Stud1")
        print("### User last_name check completed ###")
        self.assertEquals(self.user.contact_number,"9670547821")
        print("### User contact_number check completed ###")
        self.assertEquals(self.user.email,"stud1@test.com")
        print("### User email check completed ###")


    def test_all_data_correctly_assigned_to_student(self):
        self.assertEquals(self.stud.roll_number,"20CS10085")
        print("### Student roll_number check completed ###")
        self.assertEquals(self.stud.department,"Computer Science and Engineering")
        print("### Student department check completed ###")
        self.assertTrue(self.stud.SDprofile)
        print("### Student SDprofile check completed ###")

    def test_all_data_correctly_assigned_to_alumni(self):
        self.assertEquals(self.alum.roll_number,"15CS10023")
        print("### Alumni roll_number check completed ###")
        self.assertEquals(self.alum.department,"Computer Science and Engineering")
        print("### Alumni department check completed ###")
        self.assertEquals(self.alum.year_of_graduation,2019)
        print("### Alumni year_of_graduation check completed ###")


    def test_all_data_correctly_assigned_to_company(self):
        self.assertEquals(self.comp.company_name,"OPIGS Technologies Ltd.")
        print("### Company company_name check completed ###")
        self.assertEquals(self.comp.address,"Demo Address")
        print("### Company address check completed ###")
        self.assertEquals(self.comp.profile,"SD")
        print("### Company profile check completed ###")
        self.assertEquals(self.comp.overview,"Demo Overview")
        print("### Company overview check completed ###")
        self.assertEquals(self.comp.work_environ,"Demo Work Environment")
        print("### Company work_environ check completed ###")
        self.assertEquals(self.comp.job_desc,"Demo Job Description")
        print("### Company job_desc check completed ###")
        self.assertEquals(self.comp.other_details,"Demo Other Details")
        print("### Company other_details check completed ###")

