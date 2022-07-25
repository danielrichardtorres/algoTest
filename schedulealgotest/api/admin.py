from django.contrib import admin
from .models import (
    Student,
    Teacher,
    Subject,
    appInstance,
    reoccuringApp,
    TimeSlot,
)

# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(appInstance)
admin.site.register(reoccuringApp)
admin.site.register(TimeSlot)
