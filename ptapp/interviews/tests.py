from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from tests.models import TestGroup, TestUnit
from .models import Interview

# Create your tests here.
# Тестирование представлений
# - все представления требуют login_required (тестирование с анонимным пользователем и аутентифицированным)
#   - представление interview/test/<test_id>
#   - представление interview/<interview_id>/question
#   - представление interview/<interview_id>/report
# - представление interview/test/<test_id>
#   - если тест не задан в базе данных -> 404
#   - если тест завершен -> redirect(report)
#   - если тест новый -> redirect(question)
#   - если тест не завершен -> redirect(question)
# - представление interview/<interview_id>/question
#   - интервью отсутствует в базе данных -> 404
#   - интервью есть в базе данных - получениие вопроса
#   - интервью - после последнего вопроса (опрос завершен) перенаправление на report
# - представление interview/<interview_id>/report
#   - если интервью отсутствует в базе данных -> 404
#   - если интервью закончено - отображение результатов
#   - если интервью не закончено -> 404


def create_test(test_owner):
    tg = TestGroup.objects.create(
            name = 'testing group',
            description = 'group for testing interview',
    )
    tu = tg.testunit_set.create(
            name = 'test unit',
            description = 'test in group',
            owner = test_owner,
    )
    q = tu.question_set.create(
        text = 'test question text',
    )
    q.answer_set.create(
            name = 'question answer 1',
            right = True,
    )
    q.answer_set.create(
            name = 'question answer 2',
            right = False,
    )
    return tu


def create_user(**test_data):
    user = User.objects.create_user(**test_data)
    return user


class TestLoginRequried(TestCase):
    def setUp(self):
        self.user = create_user(
            username='testuser',
            password='password',
        )
        self.testunit = create_test(self.user)

    def test_anonymous_interviews_open(self):
        response = self.client.get(reverse('interview:open', args=(1,)))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_anonymous_interviews_question(self):
        response = self.client.get(reverse('interview:question', args=(1,)))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_anonymous_interviews_report(self):
        response = self.client.get(reverse('interview:report', args=(1,)))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)


class TestViewInterviewOpen(TestCase):
    def setUp(self):
        self.user = create_user(
            username='testuser',
            password='password',
        )
        self.testunit = create_test(self.user)
        self.client.login(
            username='testuser',
            password='password',
        )

    def test_open_broken_test_interview(self):
        response = self.client.get(reverse('interview:open', args=(2,)))
        self.assertEqual(response.status_code, 404)

    def test_open_complete_test_interview(self):
        tu = TestUnit.objects.get()
        interview = Interview.objects.create(
            user = self.user,
            testunit = tu,
            is_complete = True,
        )
        response = self.client.get(reverse('interview:open', args=(tu.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertIn('report', response.url)

    def test_open_new_test_interview(self):
        tu = TestUnit.objects.get()
        response = self.client.get(reverse('interview:open', args=(tu.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertIn('question', response.url)

    def test_open_early_runed_test_interview(self):
        tu = TestUnit.objects.get()
        interview = Interview.objects.create(
            user = self.user,
            testunit = tu,
            is_complete = False,
        )
        response = self.client.get(reverse('interview:open', args=(tu.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertIn('question', response.url)


class TestViewReplyQuestion(TestCase):
    def setUp(self):
        self.user = create_user(
            username='testuser',
            password='password',
        )
        self.testunit = create_test(self.user)
        self.client.login(
            username='testuser',
            password='password',
        )

    def test_open_broken_interview_question(self):
        response = self.client.get(reverse('interview:question', args=(2,)))
        self.assertEqual(response.status_code, 404)

    def test_open_new_interview_question(self):
        tu = TestUnit.objects.get()
        interview = Interview.objects.create(
            user = self.user,
            testunit = tu,
            is_complete = False,
        )
        response = self.client.get(reverse('interview:question', args=(tu.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            interview.get_next_question().question.text
        )

    def test_open_report_after_reply_last_question(self):
        tu = TestUnit.objects.get()
        interview = Interview.objects.create(
            user = self.user,
            testunit = tu,
            is_complete = False,
        )
        question = interview.get_next_question().question
        answer = question.answer_set.last()
        response = self.client.post(
            reverse('interview:question', args=(interview.id,)),
            {str(answer.id): 'on'},
        )
        response = self.client.get(reverse('interview:question', args=(tu.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertIn('report', response.url)

class TestViewInterviewReport(TestCase):
    def setUp(self):
        self.user = create_user(
            username='testuser',
            password='password',
        )
        self.testunit = create_test(self.user)
        self.client.login(
            username='testuser',
            password='password',
        )

    def test_report_for_broken_test_interview(self):
        response = self.client.get(reverse('interview:report', args=(2,)))
        self.assertEqual(response.status_code, 404)

    def test_report_for_complete_test_interview(self):
        tu = TestUnit.objects.get()
        interview = Interview.objects.create(
            user = self.user,
            testunit = tu,
            is_complete = False,
        )
        question = interview.get_next_question().question
        answer = question.answer_set.first()
        response = self.client.post(
            reverse('interview:question', args=(interview.id,)),
            {str(answer.id): 'on'},
            follow=True,
        )
        response = self.client.get(reverse('interview:report', args=(interview.id,)))
        self.assertEqual(response.status_code, 200)

    def test_report_for_early_runed_test_interview(self):
        tu = TestUnit.objects.get()
        interview = Interview.objects.create(
            user = self.user,
            testunit = tu,
            is_complete = False,
        )
        response = self.client.get(reverse('interview:report', args=(interview.id,)))
        self.assertEqual(response.status_code, 404)