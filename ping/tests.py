from django.test import TestCase
from django.urls import reverse
from .models import *
from django.test import Client
from django.contrib.auth import get_user_model


class HomePageTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user('test@email.com', 'mot_de_passe')

    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_display_moncompte_if_user_is_not_connect(self):
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, 'Mon Compte')

    def test_display_moncompte_if_user_is_connect(self):
        self.client.login(email='test@email.com', password='mot_de_passe')
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Mon Compte')


class LoginPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.create_user('test@email.com', 'passwordtest')

    def test_Login(self):
        self.client.login(email='test@email.com', password='passwordtest')
        response = self.client.get(reverse('reuillytt:connexion'))
        self.assertEqual(response.status_code, 200)


class MentionsPageTestCase(TestCase):
    def test_mentions_page(self):
        response = self.client.get(reverse('reuillytt:mentions'))
        self.assertEqual(response.status_code, 200)


class HistoriquePageTestCase(TestCase):
    def test_historique_page(self):
        response = self.client.get(reverse('reuillytt:historique'))
        self.assertEqual(response.status_code, 200)


class LiensPageTestCase(TestCase):
    def test_liens_page(self):
        response = self.client.get(reverse('reuillytt:liens'))
        self.assertEqual(response.status_code, 200)


class CguPageTestCase(TestCase):
    def test_mentions_page(self):
        response = self.client.get(reverse('reuillytt:cgu'))
        self.assertEqual(response.status_code, 200)


class MyAccountPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email='test@test.com', password='mot_de_passe')

    def test_page_return_200_if_connect(self):
        self.client.login(email='test@test.com', password='mot_de_passe')
        response = self.client.get(reverse('reuillytt:moncompte'))
        self.assertEqual(response.status_code, 200)

    def test_page_return_302_if_not_connect(self):
        response = self.client.get(reverse('reuillytt:moncompte'))
        self.assertEqual(response.status_code, 302)


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class CreationComptePageTestCase(TestCase):

    def test_creation_is_ok(self):
        user_count = User.objects.count()
        data = {
            'email': 'foobar@example.com',
            'mot_de_passe': 'somepassword',
            'confirm_password': 'somepassword',
            'first_name': 'first',
            'last_name': 'last'
        }
        response = self.client.post(reverse('reuillytt:creation'), data)
        self.assertEqual(User.objects.count(), user_count+1)


class InscriptionPageTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email='test@test.com', password='mot_de_passe')
        self.competition = Competition.objects.create(nom="fscf", prix=25, description="compet")
        self.cotisation = Cotisation.objects.create(nom="adulte loisir", prix=145, description="adulte loisir")
        self.client = Client()

    def test_inscription_is_ok(self):
        self.client.login(email='test@test.com', password='mot_de_passe')
        inscription_count = Inscription.objects.count()
        data = {
            'date_naissance': '2001-01-10',
            'adresse': '40 rue de la voute',
            'ville': 'paris',
            'telephone': '01234672772',
            'code_postal': '75012',
            'pays': 'france',
            'forfait': 'adulte loisir',
            'competitions': 'fscf',
        }
        response = self.client.post(reverse('reuillytt:inscription'), data)
        self.assertEqual(Inscription.objects.count(), inscription_count+1)





