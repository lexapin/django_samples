from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

from django.contrib.auth.models import User
from .models import Interview, Reply, UserAnswer
from tests.models import TestGroup, TestUnit, Question, Answer


@login_required
def open_interview(request, testunit_id):
    """
    Промежуточное представление:
    - Открывает тест для опроса пользователя
    - смотрит не выполнял ли пользователь данный тест.
    - Если опрос еще не был пройден пользователем - создает опрос
    - Если опрос уже пройден - скидывает пользователя к результатам
    :param request:
    :return:
    """
    testunit = TestUnit.objects.get(pk=testunit_id)
    user = request.user
    try: # Как Вы относитесь к блокам try-except в своих релизах?
        interview = Interview.objects.get(
                                  user = user,
                                  testunit = testunit,
                                )
    except Interview.DoesNotExist:
        interview = Interview(user = user, testunit = testunit)
        interview.save()

    if interview.is_complete:
        return HttpResponseRedirect(reverse('interview:report', args=(interview.id,)))
    else:
        return HttpResponseRedirect(reverse('interview:question', args=(interview.id,)))


@login_required
def question(request, interview_id):
    """
    Выводит текукщий вопрос
    :param request:
    :param interview_id:
    :return:
    """
    try:
        interview = Interview.objects.get(id = interview_id, user = request.user)
    except Interview.DoesNotExist:
        return HttpResponse('Вау!!!')
    question_for_reply = interview.get_next_question()
    if question_for_reply is None:
        return HttpResponseRedirect(reverse('interview:report', args=(interview.id,)))
    if request.method == 'POST':
        for answer in question_for_reply.question.answer_set.all():
            if str(answer.id) in request.POST:
                question_for_reply.useranswer_set.create(answer = answer)
        if question_for_reply.useranswer_set.count():
            question_for_reply.is_reply = True
            question_for_reply.save()
            return HttpResponseRedirect(reverse('interview:question', args=(interview.id,)))
        else:
            print('Не выбраны ответы')
    context = {
        'question': question_for_reply.question,
    }
    return render(request, "interviews/question.html", context)


@login_required
def report(request, interview_id):
    try:
        interview = Interview.objects.get(id = interview_id, user = request.user)
    except Interview.DoesNotExist:
        return HttpResponse('Вау!!!')
    count_right = 0
    count_all = interview.reply_set.count()
    detail = []
    for index, reply in enumerate(interview.reply_set.all()):
        if reply.question.right_answers==reply.user_answers:
            count_right+=1
            detail.append((index+1, True))
        else:
            detail.append((index+1, False))
    context = {
        'name': interview.testunit.name,
        'count_all': count_all,
        'count_right': count_right,
        'right_percent': round(count_right/count_all*100),
        'detail': detail,
    }
    return render(request, "interviews/report.html", context)