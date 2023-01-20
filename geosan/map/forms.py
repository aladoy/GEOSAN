from django import forms
from django.db import models
import pandas as pd

"""communes_data = './geojson/Caracterisation_PCA_wgs_84_2.csv'
communes_data = pd.read_csv(communes_data)
communes_names = communes_data['Nom_CMN']
communes_names = sorted(communes_names)

CHOICES = ()

for index, name in enumerate(communes_names):
    CHOICES.append(str(index), name)

class CommuneForm(forms.ModelForm):
    communes = forms.CharField(widget=forms.Select(choices=CHOICES))"""