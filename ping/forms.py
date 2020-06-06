from django import forms
from django.forms import DateInput, ModelForm
from .models import Competition, Cotisation, Joueur, Adresse, Inscription


class NouvellePhotoForm(forms.Form):
    nom = forms.CharField(label="Nom de l'image", max_length=100)
    photo = forms.ImageField()


class ConnexionForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'contact-form'}), required=True, label='Email')
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'contact-form'}))


class UserForm(forms.Form):
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'contact-form'}))
    first_name = forms.CharField(label="Prénom", max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'contact-form'}))
    last_name = forms.CharField(label="Nom", max_length=40, required=True, widget=forms.TextInput(attrs={'class': 'contact-form'}))
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'contact-form'}), required=True, label="Mot de Passe")
    confirm_password = forms.CharField(label='Confirmation Mot de Passe', widget=forms.PasswordInput(attrs={'class': 'contact-form'}), required=True)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirm_password = cleaned_data.get("confirm_password")
        if not mot_de_passe == confirm_password:
            raise forms.ValidationError("Les deux mots de passe saisis sont différents")

        return cleaned_data


class InscriptionForm(ModelForm):

    COMPETITIONS = [
        ('indivs & 41', 'indivs 41€'),
        ('fscf & 25', 'fscf 25€'),
    ]


    COTISATIONS = [
        ('fille -11ans & 50', 'fille -11ans 50€'),
        ('enfant -11ans & 140', 'fille -11ans 140€'),
        ('enfant +11ans & 155', 'fille -11ans 155€'),
        ('adulte competition & 155', 'fille -11ans 155€'),
        ('adulte loisir & 145', 'fille -11ans 145€'),
    ]

    cotisation = forms.ChoiceField(widget=forms.RadioSelect, choices=COTISATIONS)
    competition = forms.MultipleChoiceField(
        label='Compétitions',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=COMPETITIONS,
    )

    def __init__(self, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        self.fields['cotisation'].empty_label = None

    class Meta:

        model = Inscription
        exclude = ['saison', 'paiement', 'joueur', 'date']

    def clean_cotisation(self):
        cotisation = self.cleaned_data.get('cotisation')

        if cotisation.find('&'):
            cotisation = cotisation[0:cotisation.find('&') - 1]
            return Cotisation.objects.get(id=Cotisation.objects.filter(nom=cotisation)[0].id)
        else:
            raise forms.ValidationError("Séléctionnez une cotisation")

    def clean_competition(self, *args, **kwargs):
        competitions = self.cleaned_data.get('competition')
        if len(competitions) > 0:
            competition_selectionne = []
            for competition in competitions:
                compet = competition[0:competition.find('&') - 1]
                competition_selectionne.append(compet)
            return competition_selectionne
        else:
            return competitions


class AdresseForm(ModelForm):
    class Meta:
        model = Adresse
        fields = '__all__'


class JoueurForm(ModelForm):
    class Meta:
        model = Joueur
        exclude = ['licence', 'adresse', 'user']
        widgets = {
            'date_naissance': DateInput(format=('%d-%m-%Y'), attrs={'type':'date', 'class':'datepicker'}),
        }








