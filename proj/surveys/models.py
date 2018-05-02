from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.contrib.contenttypes.models import ContentType
import uuid

import json
from uuid import UUID
from json import JSONEncoder

MAX_OPTIONS = 20


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class Survey(models.Model):
    survey_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    creator_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    num_questions = models.SmallIntegerField(default=0)

    def __str__(self):
        return 'Survey ID: %s, Title: %s, %s' % (self.survey_Id, self.title, self.creator_Id)

    def decrement_questions(self, to_delete):
        questions = self.question_set.all()
        for q in questions:
            if q.question_num >= to_delete:
                q.question_num -= 1
                q.save()

    def delete(self):
        questions = self.question_set.all()
        for q in questions:
            #if q.question_type == 'CB':
            q.delete()
        super(Survey, self).delete()

QUESTION_CHOICES = (
    ('CB', 'CheckBox'),
    ('MC', 'MultipleChoice'),
    ('TE', 'TextEntry'),
    ('DD', 'Dropdown'),
    ('LK', 'Likert'),
)


class Question(PolymorphicModel):
    question_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    question_survey_Id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=2, choices=QUESTION_CHOICES)
    question_num = models.SmallIntegerField()
    question_title = models.CharField(max_length=400)

    def __str__(self):
        return 'Question ID: %s, %s' % (self.question_Id, self.question_title)

    # def save(self):
    #
    #     super(Question, self).save()
    #
    # def delete(self):
    #     survey = question_survey_Id
    #     questions = survey.question_set.all()
    #     x = question_num
    #     print(x)
    #     bignums = questions.filter(question_num__gt=self.question_num)
    #     for q in bignums:
    #         q.decrement_number
    #     print(bignums)
    #     #self.question_survey_Id.num_questions -= 1
    #     #super(Question, self).delete()
    #
    # def decrement_number(self):
    #     #self.question_num -= 1
    #     print(self.question_num)

    # def save(self):
    #     survey = self.question_survey_Id
    #     num = survey.num_questions+1
    #     survey.update(num_questions=num)
    #     self.question_num = num
    #     super(Question, self).save()
    #
    # def delete(self):
    #     survey = self.question_survey_Id

    #
    #     survey.num_questions -= 1
    #     super(Question, self).delete()


class MCQuestion(Question):
    question_text = models.CharField(max_length=400)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100, blank=True, null=True)
    option_4 = models.CharField(max_length=100, blank=True, null=True)
    option_5 = models.CharField(max_length=100, blank=True, null=True)

    def get_options(self):
        options = [(self.option_1, self.option_1), (self.option_2, self.option_2)]
        if self.option_3: options.append((self.option_3, self.option_3))
        if self.option_4: options.append((self.option_4, self.option_4))
        if self.option_5: options.append((self.option_5, self.option_5))
        print(options)
        return tuple(options)

    def get_responses(self):
        return self.responsemc_set.all()

# Drop Down Question Model
class DDQuestion(Question):
    question_text = models.CharField(max_length=400)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100, blank=True, null=True)
    option_4 = models.CharField(max_length=100, blank=True, null=True)
    option_5 = models.CharField(max_length=100, blank=True, null=True)

    def get_options(self):
        options = [(self.option_1, self.option_1), (self.option_2, self.option_2)]
        if self.option_3: options.append((self.option_3, self.option_3))
        if self.option_4: options.append((self.option_4, self.option_4))
        if self.option_5: options.append((self.option_5, self.option_5))
        print(options)
        return tuple(options)

    def get_responses(self):
        return self.responsedd_set.all()


class TEQuestion(Question):
    question_text = models.CharField(max_length=400)

    def get_responses(self):
        return self.responsete_set.all()


class LKQuestion(Question):
    question_text = models.CharField(max_length=400)

    def get_responses(self):
        return self.responselk_set.all()


class CBQuestion(Question):
    question_text = models.CharField(max_length=400)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100, blank=True, null=True)
    option_4 = models.CharField(max_length=100, blank=True, null=True)
    option_5 = models.CharField(max_length=100, blank=True, null=True)
    #num_options = models.PositiveSmallIntegerField(default=0, max_value=MAX_OPTIONS)

    def get_options(self):
        options = [(self.option_1, self.option_1), (self.option_2, self.option_2)]
        if self.option_3: options.append((self.option_3, self.option_3))
        if self.option_4: options.append((self.option_4, self.option_4))
        if self.option_5: options.append((self.option_5, self.option_5))
        print(options)
        return tuple(options)

    def get_responses(self):
        return self.responsecb_set.all()


class ResponseMC(models.Model):
    # increment number of questions in survey and set current question number
    response_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    response_question_Id = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    # response_question_type = models.ForeignKey(MCQuestions, on_delete=models.PROTECT)
    response_survey_Id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    response_user_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=400, null=True)

    def get_choices(self):
        return self.response_question_Id.get_options()

class ResponseDD(models.Model):
    # increment number of questions in survey and set current question number
    response_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    response_question_Id = models.ForeignKey(DDQuestion, on_delete=models.CASCADE)
    response_survey_Id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    response_user_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=400, null=True)

    def get_choices(self):
        return self.response_question_Id.get_options()




class ResponseTE(models.Model):
    # increment number of questions in survey and set current question number
    response_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    response_question_Id = models.ForeignKey(TEQuestion, on_delete=models.CASCADE)
    # response_question_type = models.ForeignKey(MCQuestions, on_delete=models.PROTECT)
    response_survey_Id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    response_user_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=400, null=True)


class ResponseCB(models.Model):
    # increment number of questions in survey and set current question number
    response_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    response_question_Id = models.ForeignKey(CBQuestion, on_delete=models.CASCADE)
    response_survey_Id = models.ForeignKey(Survey, on_delete=models.PROTECT)
    response_user_Id = models.ForeignKey(User, on_delete=models.PROTECT)
    response_text = models.CharField(max_length=400, null=True)

    def get_choices(self):
        return self.response_question_Id.get_options()

OPTION_CHOICES = (
    ('CB', 'CheckBox'),
    ('MC', 'MultipleChoice'),
)


class Option(models.Model):
    option_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
    option_num = models.SmallIntegerField()
    type_of_question = models.CharField(max_length=2, choices=OPTION_CHOICES)
    mc_question_Id = models.ForeignKey(MCQuestion, null=True, blank=True, on_delete=models.CASCADE)
    cb_question_Id = models.ForeignKey(CBQuestion, null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def save(self):
        if type_of_question == 'CB':
            self.cb_question_Id.num_options += 1
            self.option_num = self.cb_question_Id.num_options
        else:
            self.mc_question_Id.num_options += 1
            self.option_num = self.mc_question_Id.num_options
        super(Option, self).save()

    def delete(self):
        if type_of_question == 'CB':
            self.cb_question_Id.num_options -= 1
        else:
            self.mc_question_Id.num_options -= 1
        super(Option, self).delete()

    # def make_cb_option(self):
    #     type_of_question = 'CB'
    #     self.save()
    #
    # def make_mc_option(self):
    #     type_of_question = 'MC'
    #     self.save()

    # def save(self, type):
    #     self.add_to_opt_num()
    #     if type == 'CB':
    #         type_of_question = 'CB'
    #     else:
    #         type_of_question = 'MC'
    #     super(Option, self).save()
