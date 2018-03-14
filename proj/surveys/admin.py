from django.contrib import admin

# Register your models here.

from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, ResponseTE, ResponseMC, ResponseCB

admin.site.register(MCQuestion)
admin.site.register(TEQuestion)
admin.site.register(CBQuestion)
admin.site.register(Survey)
admin.site.register(ResponseTE)
admin.site.register(ResponseMC)
admin.site.register(ResponseCB)
admin.site.register(Question)

