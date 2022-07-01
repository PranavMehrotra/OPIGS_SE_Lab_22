from django.contrib import admin
from .models import User,Alumni,Company,Student,Chat,Notification

admin.site.register(User)#register a model to get is displayed at admin's portal
admin.site.register(Student)
admin.site.register(Alumni)
admin.site.register(Company)
admin.site.register(Chat)
admin.site.register(Notification)
