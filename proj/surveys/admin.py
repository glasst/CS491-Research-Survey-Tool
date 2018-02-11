from django.contrib import admin

# Register your models here.
from .models import Question, Survey, Response

admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Response)
