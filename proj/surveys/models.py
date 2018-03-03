from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
import uuid

import json
from uuid import UUID
from json import JSONEncoder


NUM_OPTIONS = 10


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


'''
class User(models.Model):
        user_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
        username = models.CharField(max_length=45)
        #username = models.CharField(primary_key=True, max_length=45)
        email = models.CharField(max_length=255)
        password = models.CharField(max_length=32)
        create_time = models.DateTimeField(auto_now=True)
        first_name = models.CharField(max_length=45)
        last_name = models.CharField(max_length=45)
        role = models.CharField(max_length=1)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=1)

    def __str__(self):
        u = self.user
        return 'Username: %s, Name: %s %s' % (u.username, u.first_name, u.last_name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''


class Survey(models.Model):
    survey_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    creator_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    num_questions = models.IntegerField(default=0)

    def __str__(self):
        return 'Survey ID: %s, Title: %s, %s' % (self.survey_Id, self.title, self.creator_Id)


class Question(models.Model):
    question_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    question_survey_Id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20)
    question_text = models.CharField(max_length=400, default="Add question text")

    def __str__(self):
                return 'Question ID: %s, %s' % (self.question_Id, self.question_survey_Id)

class MCQuestion(models.Model):
    question_survey_Id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    question_text = models.CharField(max_length=400)
    question_num = models.IntegerField()
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)
    option_5 = models.CharField(max_length=100)

    # increment number of questions in survey and set current question number
    def save(self):
        question_survey_Id.num_questions += 1
        self.question_num = question_survey_Id.num_questions
        super(MCQuestion, self).save()

    def delete(self):
        question_survey_Id.num_questions -= 1
        super(MCQuestion, self).delete()


class TEQuestion(models.Model):
    question_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    question_survey_Id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=400)
    question_num = models.IntegerField()

    # increment number of questions in survey and set current question number
    def save(self):
        question_survey_Id.num_questions += 1
        self.question_num = question_survey_Id.num_questions
        super(MCQuestion, self).save()

    def delete(self):
        question_survey_Id.num_questions -= 1
        super(MCQuestion, self).delete()

class CBQuestion(models.Model):
    question_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    question_survey_Id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=400)
    question_num = models.IntegerField()
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)
    option_5 = models.CharField(max_length=100)


    def save(self):
        question_survey_Id.num_questions += 1
        self.question_num = question_survey_Id.num_questions
        super(MCQuestion, self).save(


    def delete(self):
        question_survey_Id.num_questions -= 1
        super(MCQuestion, self).delete()


class ResponseTE(models.Model):
    # increment number of questions in survey and set current question number
    response_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    response_question_Id = models.ForeignKey(MCQuestion, on_delete=models.PROTECT)
   # response_question_type = models.ForeignKey(MCQuestions, on_delete=models.PROTECT)
    response_survey_Id  = models.ForeignKey(Survey, on_delete=models.PROTECT)
    response_user_Id = models.ForeignKey(User, on_delete=models.PROTECT)
    response_text = models.CharField(max_length=400)

'''
OPTION_CHOICES = (
    ('CB', 'CheckBox'),
    ('MC', 'MultipleChoice'),
)

class Option(models.Model):
    option_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    type_of_question = models.CharField(max_length=2, choices=OPTION_CHOICES)
    mc_question_Id = models.ForeignKey(MCQuestion, on_delete=models.PROTECT)
    cb_question_Id = models.ForeignKey(CBQuestion, on_delete=models.PROTECT)
    #question_Id = models.GenericForeignKey()
