from django.contrib import admin

# Register your models here.
<<<<<<< HEAD
#from .models import  Profile, Survey, Question, MCQuestion, TEQuestion, CBQuestion, Response

from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, Response


=======
from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, Response
>>>>>>> 7b46930f847049ae4292da3ca3b820177ec1816b



admin.site.register(MCQuestion)
admin.site.register(TEQuestion)
admin.site.register(CBQuestion)
admin.site.register(Survey)
admin.site.register(Response)
<<<<<<< HEAD

#admin.site.register(Profile)

=======
>>>>>>> 7b46930f847049ae4292da3ca3b820177ec1816b
admin.site.register(Question)
