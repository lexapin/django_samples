from django.test import TestCase
from django.urls import reverse

from .models import TestGroup, TestUnit
from django.contrib.auth.models import User

# Create your tests here.
# Тестирование представлений
#   - группа тестов
#     - отображение наборов тестов
#       - наборы тестов в системе отсутствуют
#       - наборы тестов есть в системе
#     - отображение тестов набора
#       - если идентификатор набора отсутствует в базе данных редирект на 404
#       - отображение что набор тестов пуст, если вопросв нет
#       - отображение тестов набора если они есть


def create_differ_object_list(obj_list, link):
    return [str((obj, reverse(link, args=(obj.id,)))) for obj in obj_list]


class GroupTestTest(TestCase):
    def test_view_testgrouplist_without_data(self):
        response = self.client.get(reverse('test:groups'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_testgrouplist_with_data(self):
        TestGroup.objects.create(
            name='testgroup_name',
            description='testgroup_description',
            )
        response = self.client.get(reverse('test:groups'))
        self.assertQuerysetEqual(
                response.context['object_list'],
                create_differ_object_list(TestGroup.objects.all(), 'test:group')
            )
        TestGroup.objects.all().delete()


class TestUnitTest(TestCase):
    def test_view_broken_testgroup(self):
        response = self.client.get(reverse('test:group', args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_view_empty_testunit_list(self):
        tg = TestGroup.objects.create(
            name='testgroup_name',
            description='testgroup_description',
            )
        response = self.client.get(reverse('test:group', args=(tg.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], [])
        TestGroup.objects.all().delete()

    def test_view_testunit_list(self):
        user = User.objects.create(
            username='testuser',
            password='password',
            )
        tg = TestGroup.objects.create(
            name='testgroup_name',
            description='testgroup_description',
            )
        tg.testunit_set.create(
            name = 'testunit_name',
            description = 'testunit_description',
            owner = user,
            )
        response = self.client.get(reverse('test:group', args=(tg.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'], 
            create_differ_object_list(tg.testunit_set.all(), 'interview:open')
            )
        TestGroup.objects.all().delete()