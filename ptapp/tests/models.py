from django.db import models
from django.conf import settings


# Create your models here.


class TestGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{name} ({description})".format(name=self.name, description=self.description)


class TestUnit(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_group = models.ForeignKey(TestGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name} ({description})".format(name=self.name, description=self.description)


class Question(models.Model):
    text = models.TextField(blank=True)
    test_unit = models.ForeignKey(TestUnit, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    right = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return "Answer {name} is {right} for {question} ".format(
                        name=self.name,
                        question=self.question,
                        right = 'right' if self.right else 'wrong',
        )
