from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import TemplateView
from .forms import ConnexionForm, UserForm, NouvellePhotoForm, InscriptionForm, AdresseForm, JoueurForm
from .models import *
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings


@permission_required('ping.add_photo', login_url='/')
def photo(request):
    ajout = False
    form = NouvellePhotoForm(request.POST or None, request.FILES)
    if form.is_valid():
        photo = Image()
        photo.nom = form.cleaned_data["nom"]
        photo.photo = form.cleaned_data["photo"]

        photo.save()
        ajout = True

    form = NouvellePhotoForm()
    return render(request, 'ping/photo.html', locals())


@permission_required('ping.remove_photo', login_url='/')
def supprimerphoto(request):
    images = Image.objects.all()

    if request.method == 'POST':
        photo = request.POST.get('id_photo', False)
        photo_a_supprimer = Image.objects.get(id=photo)
        photo_a_supprimer.delete()

    return render(request, 'ping/supprimerphoto.html', locals())


def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return redirect('reuillytt:moncompte')
            else:  # sinon une erreur sera affichée
                error = True
        else:
            error = True

    else:
        form = ConnexionForm()

    return render(request, 'ping/login.html', locals())


def index(request):
    photos = Image.objects.all()
    return render(request, 'ping/index.html', locals())


def creation(request):
    compte_existant = False
    user_form = UserForm(request.POST or None)

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            email = user_form.cleaned_data["email"]
            password = user_form.cleaned_data["mot_de_passe"]
            nom = user_form.cleaned_data["last_name"]
            prenom = user_form.cleaned_data["first_name"]
            if User.objects.filter(email=email):
                compte_existant = True


            else:
                val = {
                    'prenom': prenom,
                }
                html_message = render_to_string('ping/email.html', val)
                plain_message = strip_tags(html_message)
                send_mail("Bienvenue à l'Espérance de Reuilly", plain_message, settings.EMAIL_HOST_USER, [email],
                          fail_silently=False, html_message=html_message)
                user = User.objects.create_user(email, password)
                user.first_name = prenom
                user.last_name = nom
                user.save()
                login(request, user)
                return redirect('reuillytt:moncompte')

    return render(request, 'ping/creation.html', locals())


@login_required(login_url='reuillytt:connexion')
def inscription(request):
    inscrit = False
    form = InscriptionForm(request.POST or None)
    formAdresse = AdresseForm(request.POST or None)
    formJoueur = JoueurForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid() and formAdresse.is_valid() and formJoueur.is_valid():
            user = User.objects.get(id=request.user.id)
            date_naissance = formJoueur.cleaned_data['date_naissance']
            telephone = formJoueur.cleaned_data['telephone']
            voie = formAdresse.cleaned_data['voie']
            code_postal = formAdresse.cleaned_data['code_postal']
            ville = formAdresse.cleaned_data['ville']
            pays = formAdresse.cleaned_data['pays']
            forfait = form.cleaned_data['cotisation']
            competition = form.cleaned_data['competition']

            saisons = Saison.objects.all()
            for saison in saisons:
                if date.today() >= saison.date_debut_saison:
                    if date.today() < saison.date_fin_saison:
                        saison_actuelle = saison

            if len(Joueur.objects.filter(user=user)) == 1:
                joueur = Joueur.objects.get(user=user)
                if len(Inscription.objects.filter(joueur=joueur, saison=saison_actuelle)) == 1:
                    inscrit = True

                else:
                    adresse = Adresse.objects.get_or_create(voie=voie, ville=ville, code_postal=code_postal,
                                                            pays=pays)
                    cotisation = Cotisation.objects.filter(nom=forfait)[0]
                    joueur = Joueur.objects.get(user=user)
                    joueur.adresse = adresse
                    joueur.save()
                    inscription = Inscription.objects.create(saison=saison_actuelle, cotisation=cotisation,
                                                             joueur=joueur)
                    montant = [cotisation.prix]
                    competition = []

                    if len(competition) > 0:

                        for compet in competition:
                            ma_competition = compet[0:compet.find('&') - 1]
                            competitions_selectionnee = Competition.objects.filter(nom=ma_competition)[0]
                            inscription.competition.add(competitions_selectionnee)
                            montant.append(competitions_selectionnee.prix)
                            competition.append(competitions_selectionnee.nom)

                        val = {
                            'prenom': joueur.user.first_name,
                            'saison': saison_actuelle.nom,
                        }

                        html_message = render_to_string('ping/email_cotisation.html', val)
                        plain_message = strip_tags(html_message)
                        send_mail("Inscription saison " + saison_actuelle.nom, plain_message, settings.EMAIL_HOST_USER,
                                  [joueur.user.email], fail_silently=False, html_message=html_message)

                    return redirect('reuillytt:moncompte')

            else:

                adresse = Adresse.objects.get_or_create(voie=voie, ville=ville, code_postal=code_postal, pays=pays)
                cotisation = Cotisation.objects.filter(nom=forfait)[0]

                joueur = Joueur.objects.create(user=user, date_naissance=date_naissance, adresse=adresse[0],
                                               telephone=telephone)

                inscription = Inscription.objects.create(saison=saison_actuelle, cotisation=cotisation, joueur=joueur)

                montant = [cotisation.prix]

                competition = []

                if len(competition) > 0:

                    for compet in competition:
                        ma_competition = compet[0:compet.find('&') - 1]
                        competitions_selectionnee = Competition.objects.filter(nom=ma_competition)[0]
                        inscription.competition.add(competitions_selectionnee)
                        montant.append(competitions_selectionnee.prix)
                        competition.append(competitions_selectionnee.nom)

                val = {
                    'prenom': joueur.user.first_name,
                    'saison': saison_actuelle.nom,

                }

                html_message = render_to_string('ping/email_cotisation.html', val)
                plain_message = strip_tags(html_message)
                send_mail("Inscription saison " + saison_actuelle.nom, plain_message, settings.EMAIL_HOST_USER,
                          [joueur.user.email], fail_silently=False, html_message=html_message)

                return redirect('reuillytt:moncompte')

    return render(request, 'ping/inscription.html', locals())


# Access information account
@login_required(login_url='reuillytt:connexion')  # redirect when user is not logged in
def account(request):
    saisons = Saison.objects.all()
    for saison in saisons:
        if date.today() >= saison.date_debut_saison:
            if date.today() < saison.date_fin_saison:
                saison_actuelle = saison

    user = User.objects.get(id=request.user.id)

    if len(Joueur.objects.filter(user=user)) == 1:
        licencie = True
        joueur = user.joueur
        if len(Inscription.objects.filter(joueur=joueur, saison=saison_actuelle)) == 1:
            inscrit = True
            inscription = Inscription.objects.get(joueur=joueur, saison=saison_actuelle)
            prix_cotisation = inscription.cotisation.prix
            nom_cotisation = inscription.cotisation.nom
            prix_competition = []
            if len(inscription.competition.all()) == 0:
                prix_competition = 0
                competition = False
            if len(inscription.competition.all()) == 1:
                prix_competition = inscription.competition.all()[0].prix
                competition = True
                mes_competitions = inscription.competition.all()
            elif len(inscription.competition.all()) > 1:
                competition = True
                mes_competitions = inscription.competition.all()

                for competition in inscription.competition.all():
                    prix_competition.append(competition.prix)
                prix_competition = sum(prix_competition)

            prix_total = prix_cotisation + prix_competition
            if inscription.paiement:
                paiement = True
            else:
                paiement = False

    return render(request, 'ping/moncompte.html', locals())


class horaires(TemplateView):
    template_name = "ping/horaires.html"


class liens(TemplateView):
    template_name = "ping/liens.html"


class Historique(TemplateView):
    template_name = "ping/historique.html"


class Mentions(TemplateView):
    template_name = "ping/mentions.html"


class Cgu(TemplateView):
    template_name = "ping/cgu.html"






