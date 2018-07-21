from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.
# - Тестирование формы login
#   - Вход от имени пользователя, который отсутствует в базе данных
#   - Вход от имени пользователя, с неправильным паролем
#   - Вход от имени пользователя, с правильным паролем
#   - Вход от имени пользователя, без пароля
#   - Вход без имени пользователя, без пароля

# - Тестирование формы logout
#   - пользователь аутентифицирован
#   - пользователь аноним

# - Тестирование регистрации пользователя
#   - с недопустимым имененем
#   - с недопустимым паролем
#     - недостаточное число символов
#     - пароли не совпадают
#     - в пароле нет чисел
#   - с допустимым паролем


class SignInTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'password',
        }
        User.objects.create_user(**self.user_data)

    def test_signin_correct_user_and_pass(self):
        response = self.client.post(
            reverse('accounts:signin'),
            self.user_data,
            follow=True
        )
        self.assertTrue(response.context['user'].is_active)

    def test_signin_correct_user_not_pass(self):
        response = self.client.post(
            reverse('accounts:signin'),
            {
                'username': 'testuser',
                'password': 'nopassword',
            },
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)

    def test_signin_uncorrect_user_and_pass(self):
        response = self.client.post(
            reverse('accounts:signin'),
            {
                'username': 'notestuser',
                'password': 'nopassword',
            },
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)

    def test_signin_correct_user_no_pass(self):
        response = self.client.post(
            reverse('accounts:signin'),
            {
                'username': 'testuser',
            },
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)

    def test_signin_no_user_and_pass(self):
        response = self.client.post(
            reverse('accounts:signin'),
            {},
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)


class SignOutTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'password',
        }
        User.objects.create_user(**self.user_data)

    def test_signout_active_user(self):
        response = self.client.post(
            reverse('accounts:signin'),
            self.user_data,
            follow=True
        )
        self.assertTrue(response.context['user'].is_active)
        response = self.client.get(
            reverse('accounts:signout'),
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)

    def test_signout_anonymous(self):
        response = self.client.get(
            reverse('accounts:signout'),
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)


class SignUpTest(TestCase):
    def test_signup_uncorrect_name(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': '"khfh%',
                'password1': '123',
                'password2': '123',
            },
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)

    def test_signup_no_name(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': '',
            },
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)

    def test_signup_short_pass(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'testuser',
                'password1': '123',
                'password2': '123',
            },
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)

    def test_signup_passes_not_equal(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'testuser',
                'password1': '123',
                'password2': '124',
            },
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)

    def test_signup_correct_name_no_digits_in_pass(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'testuser',
                'password1': 'password',
                'password2': 'password',
            },
            follow=True
        )
        self.assertFalse(response.context['user'].is_active)

    def test_signup_correct_name_and_pass(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'testuser',
                'password1': 'pass1234',
                'password2': 'pass1234',
            },
            follow=True
        )
        self.assertTrue(response.context['user'].is_active)