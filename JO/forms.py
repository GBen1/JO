from django import forms
from utilisateur.models import Offres
from django.contrib.auth.models import User
import time
from datetime import datetime
import _strptime
from datetime import date

class ModifyOffre(forms.Form):
    libelle = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={'style':'width:90%'}))
    description = forms.CharField(max_length=1000,required=True, widget =forms.Textarea(attrs={'style':'width:90%'}))
    prix = forms.FloatField(min_value=0.5,required=True,widget=forms.TextInput(attrs={'style':'width:90%'}))
    image = forms.ImageField(required=True,widget=forms.FileInput(attrs={'style':'width:90%','value':'fichier'}))
 
class CreateOffre(forms.Form):
    libelle = forms.CharField(max_length=1000)
    description = forms.CharField(max_length=1000,required=True, widget =forms.Textarea())
    prix = forms.FloatField(min_value=0.5,required=True)
    image = forms.ImageField(required=True)


class RegistrationForm(forms.Form):
  Nom = forms.CharField(max_length=100,required=True)
  Prénom = forms.CharField(max_length=100,required=True)
  Mot_de_passe = forms.CharField(min_length=8,widget=forms.PasswordInput())
  Confirmer_Mot_de_passe = forms.CharField(min_length=8,widget=forms.PasswordInput())
  E_mail = forms.EmailField(required=True)


  
  def clean(self):

    Mot_de_passe = self.cleaned_data.get("Mot_de_passe")
    Confirmer_Mot_de_passe = self.cleaned_data.get("Confirmer_Mot_de_passe")
    E_mail = self.cleaned_data.get("E_mail")
    Nom = self.cleaned_data.get("Nom")
    Prénom = self.cleaned_data.get("Prénom")



    sc_list = list('[@_!#$%^&*()<>?/\|}{~:]')
    maj=[c for c in Mot_de_passe if c.isupper()]
    min=[c for c in Mot_de_passe if c.islower()]
    numb=[c for c in Mot_de_passe if c.isdigit()]
    spec=[c for c in Mot_de_passe if c in sc_list]
     
    if (len(maj) == 0 or len(min) == 0) or len(numb) == 0 or len(spec) == 0:
     raise forms.ValidationError([
           forms.ValidationError('Le mot de passe doit contenir des majuscules et des minuscules'),
            forms.ValidationError('Le mot de passe doit contenir au moins un chiffre'),
            forms.ValidationError("Le mot de passe doit contenir au moins un caractère spécial '[@_!#$%^&*()<>?/\|}{~:]'"),
                        ])
    elif Mot_de_passe != Confirmer_Mot_de_passe:
     raise forms.ValidationError("Les mots de passe ne sont pas identiques - Veuillez réessayer")  
    elif User.objects.filter(username=self.cleaned_data["E_mail"].lower()).exists():
     raise forms.ValidationError("Cette adresse mail existe déjà") 
    return self.cleaned_data
    
class VerifyTicketForm(forms.Form):
    Billet = forms.CharField(max_length=3000)