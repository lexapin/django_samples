from django.db import models
from django.conf import settings
from tests.models import TestUnit, Question, Answer

# Create your models here.

class Interview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    testunit = models.ForeignKey(TestUnit, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

    def get_next_question(self):
        question_number = self.reply_set.count()
        return Reply(interview=self, question=self.testunit.question_set.all()[question_number])


class Reply(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class UserAnswer(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=1)