
from django import forms

from .models import Competition, Cotisation


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



class AdherentForm(forms.Form):
    COMPETITIONS = []
    COTISATIONS = []



    date_naissance = forms.DateField(label='Date de Naissance', widget=forms.DateInput(attrs={'type':'date', 'class':'datepicker'}))
    adresse = forms.CharField(max_length=400, widget=forms.TextInput(attrs={'size': '50'}))
    ville = forms.CharField(max_length=50)
    telephone = forms.IntegerField(label='Téléphone', required=True, widget=forms.NumberInput(attrs={'class': 'contact-form'}))
    code_postal = forms.IntegerField()
    pays = forms.CharField(max_length=100)
    forfait = forms.ChoiceField(widget=forms.RadioSelect, choices=COTISATIONS)
    competitions = forms.MultipleChoiceField(
        label='Compétitions',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=COMPETITIONS,
    )










