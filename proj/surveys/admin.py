from django.contrib import admin

# Register your models here.
from .models import Question, MCQuestion, TEQuestion, CBQuestion, Survey, Response, User

admin.site.register(Question)
admin.site.register(MCQuestion)
admin.site.register(TEQuestion)
admin.site.register(CBQuestion)
admin.site.register(Survey)
admin.site.register(Response)
admin.site.register(User)
