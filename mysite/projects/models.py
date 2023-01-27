from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from django.core.validators import RegexValidator
# Create your models here.
class Klientas(models.Model):
    vardas = models.CharField("Vardas", max_length=200, help_text="Kliento vardas")
    pavarde = models.CharField("Pavarde", max_length=200, help_text="Kliento pavarde")
    imone = models.CharField("Imone", max_length=200, help_text="Kliento imone", null=True, blank = True)
    email = models.EmailField(max_length=254, blank = True, unique= True)
    telregex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Telefono numeris")
    telnr = models.CharField(verbose_name="Telefono numeris", validators=[telregex], max_length=16, blank=True, help_text="Telefono numeris")
    def __str__(self):
        return f"{self.vardas} {self.pavarde}"
    class Meta:
        verbose_name = "Klientas"
        verbose_name_plural = "Klientai"


class Darbuotojas(models.Model):
    vardas = models.CharField("Vardas", max_length=200, help_text="Darbuotojo vardas")
    pavarde = models.CharField("Pavarde", max_length=200, help_text="Darbuotojo pavarde")
    pareigos = models.CharField("Pareigos", max_length=200, help_text="Darbuotojo pareigos")
    def __str__(self):
        return f"{self.vardas} {self.pavarde}"
    class Meta:
        verbose_name = "Darbuotojas"
        verbose_name_plural = "Darbuotojai"

class Darbas(models.Model):
    pavadinimas = models.CharField("Pavadinimas", max_length=200, help_text="Darbo pavadinimas")
    pastabos = models.CharField("Pastabos", max_length=200, help_text="Pastabos", null=True, blank = True)
    projektas = models.ForeignKey("Projektas", on_delete=models.CASCADE, related_name="darbai")
    kaina = models.DecimalField("Kaina", decimal_places=2, max_digits=100, null=True, blank=True)
    def __str__(self):
        return f"{self.pavadinimas}"
    class Meta:
        verbose_name = "Darbas"
        verbose_name_plural = "Darbai"

class Saskaita(models.Model):
    data = models.DateField("Data")
    projektas = models.ForeignKey("Projektas", on_delete=models.CASCADE, null=True, related_name="saskaitos")
    darbai = models.ManyToManyField("Darbas", blank=True)

    def suma(self):
        sum = 0
        for darbas in self.darbai.all():
            sum += darbas.kaina
        return sum
    suma.short_description = "Suma"
    def __str__(self):
        return f"{self.data}"
    class Meta:
        verbose_name = "Saskaita"
        verbose_name_plural = "Saskaitos"

class Projektas(models.Model):
    pavadinimas = models.CharField("Projekto pavadinimas", max_length=200, help_text="Projekto pavadinimas")
    datapr = models.DateField("Pradzios data")
    datapb = models.DateField("Pabaigos data")
    klientas = models.ForeignKey("Klientas", on_delete=models.SET_NULL, null=True)
    vadovas = models.ForeignKey(User, verbose_name="Vadovas", on_delete=models.SET_NULL, null=True, blank=True)
    darbuotojai = models.ManyToManyField("Darbuotojas", blank=True)
    aprasymas = HTMLField(null=True, blank=True)
    foto = models.ImageField('Nuotrauka', upload_to='foto', null=True, blank=True)
    def display_darbuotojai(self):
        return ', '.join(darbuotojas.vardas+" "+darbuotojas.pavarde for darbuotojas in self.darbuotojai.all())
    def display_darbai(self):
        return ', '.join(darbas.pavadinimas for darbas in self.darbai.all())

    display_darbuotojai.short_description = "Darbuotojai"
    def __str__(self):
        return f"{self.pavadinimas}"
    class Meta:
        verbose_name = "Projektas"
        verbose_name_plural = "Projektai"
