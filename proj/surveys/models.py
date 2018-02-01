from django.db import models
import uuid


class User(models.Model):
        user_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
        username = models.CharField(max_length=45)
        email = models.CharField(max_length=255)
        password = models.CharField(max_length=32)
        create_time = models.DateTimeField(auto_now=True)
        first_name = models.CharField(max_length=45)
        last_name = models.CharField(max_length=45)
        role = models.CharField(max_length=1)

class Survey(models.Model):
	survey_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	creator_Id = models.ForeignKey(User, on_delete=models.PROTECT)

class Question(models.Model):
	question_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	question_survey_Id = models.ForeignKey(Survey, on_delete=models.PROTECT)
	question_type = models.CharField(max_length=50)
	question_text = models.CharField(max_length=400)

class Response(models.Model):
	response_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	response_question_Id = models.ForeignKey(Question, on_delete=models.PROTECT)
	#response_question_type = models.ForeignKey(Questions, on_delete=models.PROTECT)
	response_survey_Id 	= models.ForeignKey(Survey, on_delete=models.PROTECT)
	response_user_Id = models.ForeignKey(User, on_delete=models.PROTECT)
	response_text = models.CharField(max_length=400)
