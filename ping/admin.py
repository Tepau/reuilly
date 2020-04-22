from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

saisons = Saison.objects.all()
for saison in saisons:
    if date.today() >= saison.date_debut_saison:
        if date.today() < saison.date_fin_saison:
            saison_actuelle = saison


class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'paiement', 'annee', 'montant')

    def nom(self, instance):
        return instance.joueur

    def prenom(self, instance):
        return instance.joueur.user.first_name

    def paiement(self, instance):
        if instance.paiement:
            return 'OK'
        else:
            return 'Non effectué'

    def annee(self, instance):
        return instance.saison.nom

    def montant(self, instance):
        prix_competition = []
        prix_cotisation = instance.cotisation.prix
        if len(instance.competition.all()) == 0:
            prix_competition = 0
        if len(instance.competition.all()) == 1:
            prix_competition = instance.competition.all()[0].prix
        elif len(instance.competition.all()) > 1:

            for competition in instance.competition.all():
                prix_competition.append(competition.prix)
            prix_competition = sum(prix_competition)
        montant_total = prix_competition + prix_cotisation

        return str(montant_total) + "€"


class JoueurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'adress', 'ville', 'paiement')

    def nom(self, instance):
        return instance.user.last_name
    nom.short_description = 'Nom'

    def prenom(self, instance):
        return instance.user.first_name
    prenom.short_description = 'Prénom'

    def adress(self, instance):
        return instance.adresse.voie
    adress.short_description = 'Adresse'

    def ville(self, instance):
        return instance.adresse.ville
    ville.short_description = 'Ville'

    def paiement(self, instance):
        mon_inscription = instance.inscription_set.all()[0]
        if mon_inscription.paiement:
            return 'OK'
        else:
            return 'Non effectué'


class SaisonAdmin(admin.ModelAdmin):
    list_display = ('annee', 'date_debut', 'date_fin')

    def annee(self, instance):
        return instance.nom
    annee.short_description = 'Saison'

    def date_debut(self, instance):
        return instance.date_debut_saison
    date_debut.short_description = 'Début de saison'

    def date_fin(self, instance):
        return instance.date_fin_saison
    date_fin.short_description = 'Fin de saison'


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(Joueur, JoueurAdmin)
admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(Saison, SaisonAdmin)
admin.site.register(Competition)
admin.site.register(Cotisation)


