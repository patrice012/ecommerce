from django.test import TestCase, Client
from django.db import IntegrityError
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout , authenticate


# Create your tests here.
User = get_user_model()

class TestUserType(TestCase):
    def setUp(self):
        self.user = User(email='dev@gmail.com', password="user0123")
        self.user1 = User(email='test@gmail.com', password="test0123")
        self.user1.is_admin = True
        self.user1.is_superuser = True



    def test_superuser_user(self):
        self.assertTrue(self.user1.is_admin == True)
        self.assertTrue(self.user1.is_superuser == True)
        self.assertFalse(self.user.is_admin != False)



class TestUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email = "test@ok.com", password="test")

    
    def test_user_login_url(self):
        response = self.client.get('/account/login', {'email':'dev@gmail.com', 'password':'user0123'}, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_user_register_url(self):
        register_url = self.client.get(reverse('authapp:register'))
        self.user = self.client.post(reverse('authapp:register'), {'email':'dev@gmail.com', 'password':'user0123'}, follow=True)
        # print(dir(self.user))
        # print(self.user.redirect_chain)
        # print(self.user.templates) -->
        self.assertEqual(self.user.resolver_match._func_path, 'authapp.views.auth_register')
        self.assertTrue(register_url.request.get('PATH_INFO') == '/account/register/')
        self.assertEquals(register_url.status_code, 200)


    # def test_user_login_state(self):
    #     userr  = login(self.user)
    #     print(userr)



class TestUserCreation(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email = "test1@ok.com", password="test1")
        self.user2 = User.objects.create_user(email = "test2@ok.com", password="test2")
        self.user3 = User.objects.create_user(email = "test3@ok.com", password="test3")

    def test_users_numbers(self):
        self.users = User.objects.all().count()
        self.assertAlmostEquals(self.users, 3)

    def test_user_email(self):
        self.assertEqual(self.user1.email, 'test1@ok.com')

    
    # this two test are the same 1
    # def test_unique_email_contraint(self):
    #     self.assertRaises(IntegrityError, userr)

    # 2
    def test_unique_email_contraint_two(self):
        with self.assertRaises(IntegrityError):
            user4 = User.objects.create_user(email = 'test1@ok.com', password = "test1")


# def userr():
#     user4 = User.objects.create_user(email = 'test1@ok.com', password = "test1")
    