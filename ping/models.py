from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username =[]
    email = models.EmailField(_("email address"), unique=True) # L'adresse email est rendue unique
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS
    objects = UserManager()


class Image(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    photo = models.FileField()


class Adresse(models.Model):
    voie = models.CharField(max_length=250)
    code_postal = models.IntegerField()
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)


class Cotisation(models.Model):

    nom = models.CharField(max_length=250)
    prix = models.IntegerField()
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.nom


class Competition(models.Model):
    nom = models.CharField(max_length=250)
    prix = models.IntegerField()
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.nom


class Saison(models.Model):
    date_debut_saison = models.DateField()
    date_fin_saison = models.DateField()
    nom = models.CharField(max_length=40)


class Inscription(models.Model):
    saison = models.ForeignKey('Saison', on_delete=models.CASCADE)
    competition = models.ManyToManyField(Competition, blank=True)
    cotisation = models.ForeignKey('Cotisation', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    paiement = models.BooleanField(default=False)
    joueur = models.ForeignKey('Joueur', on_delete=models.CASCADE)


class Joueur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    licence = models.IntegerField(null=True, blank=True)
    adresse = models.ForeignKey('Adresse', on_delete=models.CASCADE)
    date_naissance = models.DateField()
    telephone = models.IntegerField()

    def compet(self):
        compets = []
        for choix_competition in self.competition.all():
            compets.append(choix_competition.nom)
        return '/'.join(compets)

    def __str__(self):
        return self.user.last_name


