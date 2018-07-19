from django.db import models
from django.conf import settings
from tests.models import TestUnit, Question, Answer


# Create your models here.


class Interview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    testunit = models.ForeignKey(TestUnit, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

    def get_next_question(self):
        reply = self.reply_set.last()
        if reply is None:
            reply = Reply(interview=self, question=self.testunit.question_set.first())
            reply.save()
            return reply
        if reply.is_reply:
            question_number = self.reply_set.count()
            if question_number==self.testunit.question_set.count():
                return None
            else:
                reply = Reply(interview=self, question=self.testunit.question_set.all()[question_number])
                reply.save()
                return reply
        return reply


class Reply(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_reply = models.BooleanField(default=False)

    @property
    def user_answers(self):
        return sorted([u_answer. answer for u_answer in self.useranswer_set.all()], key=lambda answer: answer.id)


class UserAnswer(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=1)