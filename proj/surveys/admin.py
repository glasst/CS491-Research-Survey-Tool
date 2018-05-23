from django.contrib import admin

# Register your models here.

from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, ResponseTE, ResponseMC, ResponseCB, DDQuestion, ResponseDD, ResponseLK, LKQuestion
admin.site.register(MCQuestion)
admin.site.register(TEQuestion)
admin.site.register(CBQuestion)
admin.site.register(Survey)
admin.site.register(ResponseTE)
admin.site.register(ResponseMC)
admin.site.register(ResponseCB)
admin.site.register(ResponseLK)
admin.site.register(Question)
admin.site.register(DDQuestion)
admin.site.register(ResponseDD)
admin.site.register(LKQuestion)
