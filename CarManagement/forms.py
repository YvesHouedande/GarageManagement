
from django import forms
from .models import(
        EntreVehicule, Technicien, EntrePanne,
        Vehicule, Panne, Piece, QuantitePiece,
        Client, SortieVehicule
)
from datetime import date 
from django.core.exceptions import ValidationError



class PieceQtyForm(forms.ModelForm):
    class Meta:
        model = QuantitePiece
        fields = ['quantite']
        labels = {
            'quantite': 'Quantite',
        }
        widgets = {
            'quantite': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def clean_quantite(self):
        if self.cleaned_data.get('quantite') <= 0:
            raise ValidationError("La quantite est doit etre positif")
        return self.cleaned_data.get('quantite') 

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['proprietaire', 'carburant', 'libelle', 'immatriculation', 'couleur', 'poids', 'date_arrive']
        labels = {
            'proprietaire': 'Propriétaire',
            'carburant': 'Carburant',
            'libelle': 'Libellé',
            'immatriculation': 'Immatriculation',
            'couleur': 'Couleur',
            'poids': 'Poids',
            'date_arrive': 'Date d\'arrivée',
        }
        widgets = {
            'proprietaire': forms.Select(attrs={'class': 'form-control'}),
            'carburant': forms.Select(attrs={'class': 'form-control'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.Select(attrs={'class': 'form-control'}),
            'immatriculation': forms.TextInput(attrs={'class': 'form-control'}),
            'couleur': forms.TextInput(attrs={'class': 'form-control'}),
            'poids': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_arrive': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
        }

    def clean_date_arrive(self):
        date_arrive = self.cleaned_data.get('date_arrive')
        if date_arrive and date_arrive !=  self.initial.get('date_arrive'):
            if date_arrive > date.today():
                raise ValidationError("La date d'arrivée ne peut pas être supérieure à la date d'aujourd'hui.")
            return date_arrive
        if not date_arrive and not self.initial.get('date_arrive'):
            return date.today()      
        return self.initial.get('date_arrive')
    
    def clean_poids(self):
        if self.cleaned_data.get('poids') <= 0:
            raise ValidationError("Le poids ne peut pas negatif")
        return self.cleaned_data.get('poids')
    
    def clean_couleur(self):
        if isinstance(self.cleaned_data.get('couleur'), int):
            raise ValidationError("la couleur est une chaine de caractères")
        return self.cleaned_data.get('couleur')



class EntreVehiculeForm(forms.ModelForm):
    class Meta:
        model = EntreVehicule
        fields = ['moment', 'raison', 'techniciens', 'pannes', 'vehicule', ]
        labels = {
            'moment': 'Jour',
            'raison': 'Raison',
            'techniciens': 'Techniciens',
            'pannes': 'Pannes',
            'vehicule': 'Vehicule',
        }
        widgets = {
            'moment': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', "type":"date"}),
            'raison': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'techniciens': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'pannes': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'vehicule': forms.Select(attrs={'class': 'form-control select2'}),
        }

    def clean_moment(self):
        moment = self.cleaned_data.get('moment')
        if moment and moment != self.initial.get('moment'):
            if moment > date.today():
                raise ValidationError("Le jour ne peut pas être supérieur à la date d'aujourd'hui.")
            return moment
        if not moment and not self.initial.get('moment'):
            return date.today()
        return self.initial.get('moment')

class TechnicienForm(forms.ModelForm):
    class Meta:
        model = Technicien
        fields = ['specialite', 'nom', 'prenom', 'mail', 'tel', 'salaire', 'date_arrive', 'avatar'] 
        labels = {
            'specialite': 'Spécialité',
            'nom': 'Nom',
            'prenom': 'Prénom',
            'mail': 'Adresse email',
            'tel': 'Téléphone',
            'salaire': 'Salaire',
            'date_arrive': 'Date d\'arrivée',
            'avatar':"Image de profil",
        }
        widgets = {
            'specialite': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'salaire': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_arrive': forms.DateInput(attrs={
            'class': 'form-control',
                    'placeholder': 'jj/mm/aaaa',
                    'type':'date'
             }),
            'avatar':forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def clean_date_arrive(self):
        date_arrive = self.cleaned_data.get('date_arrive')
        if date_arrive and date_arrive !=  self.initial.get('date_arrive'):
            if date_arrive > date.today():
                raise ValidationError("La date d'arrivée ne peut pas être supérieure à la date d'aujourd'hui.")
            return date_arrive
        if not date_arrive and not self.initial.get('date_arrive'):
            return date.today()      
        return self.initial.get('date_arrive')
    
    def clean_salaire(self):
        if self.cleaned_data.get('salaire') <= 0:
            raise ValidationError("Le salaire doit être supérieur à zeo")
        return self.cleaned_data.get('salaire')



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'mail', 'tel', 'avatar', 'dateAdhesion']
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'mail': 'Adresse email',
            'tel': 'Téléphone',
            'avatar': 'Image de profil',
            'dateAdhesion': 'Date d\'adhésion',
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'tel': forms.NumberInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'dateAdhesion': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
        }

    def clean_dateAdhesion(self):
        dateAdhesion = self.cleaned_data.get('dateAdhesion')
        if dateAdhesion and dateAdhesion !=  self.initial.get('dateAdhesion'):
            if dateAdhesion > date.today():
                raise ValidationError("La date d'arrivée ne peut pas être supérieure à la date d'aujourd'hui.")
            return dateAdhesion
        if not dateAdhesion and not self.initial.get('dateAdhesion'):
            return date.today()      
        return self.initial.get('dateAdhesion')

                           
class EntrePanneForm(forms.ModelForm):
    class Meta:
        model = EntrePanne
        fields = ['resolu']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resolu'].label = "Panne résolue"

class PanneForm(forms.ModelForm):
    class Meta:
        model = Panne
        fields = ['libelle', 'desc', 'cout', 'piece']
        labels = {
            'libelle': 'Libellé',
            'desc': 'Description',
            'cout': 'Coût',
            'piece': 'Pièces',
        }
        widgets = {
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cout': forms.NumberInput(attrs={'class': 'form-control'}),
            'piece': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_cout(self):
        cout = self.cleaned_data.get('cout')
        if cout <= 0 :
            raise ValidationError("Le cout doit être supérieur à zero")
        return cout

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ['libelle', 'desc', 'prix', 'image', 'ref']
        labels = {
            'libelle': 'Libellé',
            'desc': 'Description',
            'prix': 'Prix',
            'image':'Image Piece',
            'ref':'reference',
        }
        widgets = {
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'ref': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix <= 0 :
            raise ValidationError("Le prix doit être supérieur à zero")
        return prix


class SortieVehiculeForm(forms.ModelForm):
    class Meta:
        model = SortieVehicule
        fields = ['entre', 'moment', 'cout',]
        labels = {
            'entre': 'Entrée Véhicule associée',
            'moment': 'Date/Heure de sortie',
            'cout': 'Coût',
        }
        widgets = {
            'entre': forms.Select(attrs={'class': 'form-control'}),
            'moment': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', "type":"date"}),
            'cout': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_cout(self):
        cout = self.cleaned_data.get("cout")
        if cout and cout <= 0:
            ValidationError("Le coût doit être supérieur à zéro.")
        elif not cout:
            ValidationError("Le coût ne doit pas être nul")
        return self.cleaned_data.get("cout")
    
    def clean_moment(self):
        moment = self.cleaned_data.get('moment')
        if moment and moment < self.cleaned_data.get('entre').moment:
            raise ValidationError("La date de sortie doit etre supperieur à celle d'entre ")
        if moment and moment !=  self.initial.get('moment'):
            # if moment > date.today():
            #     raise ValidationError("Le moment ne peut pas être supérieure à la date d'aujourd'hui.")
            return moment
        if not moment and not self.initial.get('moment'):
            return date.today()     
        # return self.initial.get('moment')
        


