from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Представление приложения Интервью
# Состоит из трех представлений
# - open_interview создает опрос по выбронному пользователем тесту
#     - создает опрос если он не создан
#     - не имеет собственного представления
#     - перенаправляет пользователя на другие представления приложения
# - question
#     - отображает текущий вопрос теста
#     - по зовершении теста перенаправляет к представлению report
# - report
#     - отображает краткий и детальный отчет по выполненному тесту


from .models import Interview
from tests.models import TestGroup, TestUnit, Question, Answer


@login_required
def open_interview(request, testunit_id):
    """
    Промежуточное представление:
    - Открывает тест для опроса пользователя
    - смотрит не выполнял ли пользователь данный тест.
    - Если опрос ранее не был создан - создает опрос и перенаправляет на первый вопрос
    - Если опрос уже создан, но еще не был пройден пользователем до конца - перенаправляет на вопрос
    - Если опрос уже пройден - скидывает пользователя к результатам выполненного ранее теста
    :param request: объект запроса
    :param testunit_id: идентификатор теста
    :return: ссылка для перенаправления на представление Вопроса (question) или Отчета (report)
    """
    testunit = get_object_or_404(TestUnit, id=testunit_id)
    try: # Как Вы относитесь к блокам try-except в своих релизах?
        interview = Interview.objects.get(user = request.user, testunit = testunit,)
    except Interview.DoesNotExist:
        interview = Interview(user = request.user, testunit = testunit)
        interview.save()

    if interview.is_complete:
        return HttpResponseRedirect(reverse('interview:report', args=(interview.id,)))
    else:
        return HttpResponseRedirect(reverse('interview:question', args=(interview.id,)))


@login_required
def question(request, interview_id):
    """
    Представление ВОПРОС
    Отображает форму для выбора одного или нескольких ответов
    :param request: объект запроса
    :param interview_id: идентификатор интервью
    :return:
    Выводит текукщий вопрос
        - Если вопросов в тесте больше нет - перенаправляет на результаты
            - Метод GET:
                - Выводит представление модели Question
            - Метод POST:
                - Для каждого выбранного ответа Answer создает объект UserAnswer и связывает его с Reply
                    - Считается что пользователь дал ответ - ставится флаг is_reply = True
                - Пользователь перенаправляется на страницу со следующим вопросом
                - Если пользователь не дал ответов - перенаправление на текущий вопрос.
    """
    interview = get_object_or_404(Interview, id = interview_id, user = request.user)
    question_for_reply = interview.get_next_question()
    if question_for_reply is None:
        interview.is_complete = True
        interview.save()
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
            pass
            #TODO: Добавить сообщение на форме о том, что ответы не выбраны
    context = {
        'question': question_for_reply.question,
    }
    return render(request, "interviews/question.html", context)


@login_required
def report(request, interview_id):
    """
    Представление отчет
    После завершения теста (interview.get_next_question() is None)
    Собирает и сопоставляет ответы пользователя на вопросы теста
    :param request: объект запроса
    :param interview_id: идентификатор интервью
    :return: Возвращает результаты выполненного теста
    """
    interview = get_object_or_404(Interview, id=interview_id, user=request.user, is_complete=True)
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