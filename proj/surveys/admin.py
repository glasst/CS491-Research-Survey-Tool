from django.contrib import admin

# Register your models here.
from .models import Question, Survey, Response, User

admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Response)
admin.site.register(User)
