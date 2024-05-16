from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

class EntreVehicule(models.Model):
    moment = models.DateField(null=True, blank=True)
    raison = models.TextField()
    techniciens = models.ManyToManyField('Technicien', blank=True)
    pannes = models.ManyToManyField('Panne', blank=True, through="EntrePanne") 
    vehicule = models.ForeignKey("Vehicule", on_delete=models.CASCADE, null=True, blank=True)
    state = models.BooleanField(default=True) 

    class Meta:
        verbose_name = "Entrée Vehicule"

    def __str__(self):
        return f"--Id:{self.id} --Moment:{self.moment} --Raison:{self.raison}"
    
    def etat(self):
        return 'actif' if self.state else "non actif"

class EntrePanne(models.Model):
    panne = models.ForeignKey('Panne', on_delete=models.CASCADE)
    entre = models.ForeignKey(EntreVehicule, on_delete=models.CASCADE)
    resolu = models.BooleanField(default=False)

    def resolue(self):
        return "resolue" if self.resolu else "non resolue"


class Panne(models.Model):
    libelle = models.CharField(max_length=255, null=True, blank=True, unique=True)
    desc = models.TextField()
    cout = models.PositiveIntegerField(null=True, verbose_name="Coût")
    piece = models.ManyToManyField("Piece",  through="QuantitePiece")

    def __str__(self):
        return f"{self.libelle}"


class QuantitePiece(models.Model):
    quantite = models.PositiveIntegerField(default=1)
    piece = models.ForeignKey("Piece", null=True, blank=True, on_delete=models.CASCADE)
    panne = models.ForeignKey(Panne, default=1,  on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.piece.libelle}"
 
class Technicien(models.Model):
    SPECIALITE = (
        ('MECANIQUE', "MECANIQUE"),
        ('TOLERIE', "TOLERIE"),
        ('ELECTRONIQUE', "ELECTRONIQUE"),
        ("CLIMATISATION", "CLIMATISATION"),
        ("HABITACLE", "HABITACLE")
    )
    specialite = models.CharField(choices=SPECIALITE, max_length=13, null=True, verbose_name="Spécialité")
    nom = models.CharField(max_length=50, null=True, verbose_name="Nom")
    prenom = models.CharField(max_length=50, null=True, verbose_name="Prénom")
    mail = models.EmailField()
    tel = models.PositiveIntegerField(null=True, verbose_name="Téléphone")
    salaire = models.PositiveIntegerField(null=True, verbose_name="salaire")
    date_arrive = models.DateField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, verbose_name="Image Profile")

    def get_absolute_url(self):
        # Renvoyer l'URL de détail de l'objet
        return reverse('technicien-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.nom}:{self.specialite}"

class Client(models.Model):
    nom = models.CharField(max_length=10, null=True, verbose_name="Nom")
    prenom = models.CharField(max_length=10, null=True, verbose_name="Prénom")
    mail = models.EmailField()
    tel = models.PositiveIntegerField(null=True, verbose_name="Téléphone")
    avatar = models.ImageField(null=True, blank=True, verbose_name="Image Profile")
    dateAdhesion = models.DateField()

    def __str__(self):
        return f"--Id: {self.pk} --Nom: {self.nom} {self.prenom} --DateAdhesion: {self.dateAdhesion}"

    def get_absolute_url(self):
        return reverse('detail-client', kwargs={'pk': self.pk})


class Vehicule(models.Model):
    CARBURANT = (
        ('Essence', "Essence"),
        ('Diesel', "Diesel"),
    )
    proprietaire = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    carburant = models.CharField(choices=CARBURANT, max_length=7, null=True, verbose_name="Carburant")
    libelle = models.CharField(max_length=50, null=True, verbose_name="Libellé")
    immatriculation = models.CharField(max_length=15, null=True, verbose_name="Immatriculation", unique=True)
    couleur = models.CharField(max_length=10, null=True, verbose_name="Couleur")
    poids = models.PositiveIntegerField(null=True, verbose_name="Poids")
    date_arrive = models.DateField(null=True)

    def __str__(self):
        return f"--Immat:{self.immatriculation} --Libelle:{self.libelle} --proprio:{self.proprietaire.nom} {self.proprietaire.prenom}"

    def get_absolute_url(self):
        # Renvoyer l'URL de détail de l'objet
        return reverse('vehicule-detail', kwargs={'pk': self.pk})


class SortieVehicule(models.Model):
    entre = models.OneToOneField("EntreVehicule", on_delete=models.CASCADE)
    moment = models.DateField(null=True, blank=True)
    cout = models.PositiveIntegerField(blank=True, verbose_name="Coût")

    class Meta:
        verbose_name = "Sortie Vehicule"

    # def get_absolute_url(self):
    #     # Renvoyer l'URL de détail de l'objet
    #     return reverse('sortie-detail', kwargs={'pk': self.pk})


class Piece(models.Model):
    libelle = models.CharField(max_length=50)
    ref = models.CharField(max_length=255, null=True)
    image = models.ImageField(null=True, blank=True, verbose_name="Image Piece")
    desc = models.TextField()
    prix = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.libelle}" 









