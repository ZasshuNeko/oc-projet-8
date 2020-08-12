from django.core.management.base import BaseCommand, CommandError
from app.models import Produits, Vendeurs, Nutriments, categories

import requests
import json
import unicodedata

class Command(BaseCommand):
    help = "Importe un jeu de donnée venant d'OpenFoodFact"

    def handle(self, *args, **options):
        x = 0
        while x < 1:
            x += 1
            url = "https://fr.openfoodfacts.org/cgi/search.pl?"
            playload = {
                'action': 'process',
                'sort_by': 'unique_scan_n',
                'page_size': '130',
                'page': x,
                'json': 'true'
            }
            reponse = requests.get(url, params=playload)
            f = reponse.json()

            for item in f['products']:
                liste_verification = []
                # Vérification si nom francais est vide
                name_fr = item.get("product_name")
                test_produit = Produits.objects.filter(
                    generic_name_fr__exact=name_fr)
                if not test_produit.exists():
                    if name_fr:
                        # insertion du produit
                        liste_nutriment = item.get("nutriments")
                        ingredient_text = item.get("ingredients_text_fr")
                        ingredient_second = item.get("ingredients_text")
                        img_ingredients = item.get("image_ingredients_url")

                        liste_verification = [ingredient_text,ingredient_second,img_ingredients]
                        for fill in enumerate(liste_verification):
                            if not fill[1]:
                                liste_verification[fill[0]] = 'Non fournis par Open Food Fact'

                        if ingredient_second:
                            nw_produit = Produits(
                                ingredient=liste_verification[1],
                                url_image_ingredients=liste_verification[2],
                                brands_tags=item.get("brands_tags"),
                                grade=liste_nutriment.get("nutrition-score-fr_100g"),
                                image_front_url=item.get("image_front_url"),
                                image_nutrition_url=item.get("image_nutrition_url"),
                                nova_groups=item.get("quantity"),
                                generic_name_fr=item.get("product_name"),
                                url_site=item.get("url"),
                                ingredients_text_fr=liste_verification[0],
                                _id=item.get("_id"))
                            # récupération des catégories
                            categories_item = item.get("categories")
                            if categories_item:
                                if categories_item.find(':') == -1:
                                    nw_produit.save()
                                    liste_categories = categories_item.split(
                                        ',')
                                    # On vérifie si les catégories existe
                                    for categorie in liste_categories:
                                        categorie = categorie.strip()
                                        try:
                                            object_cat = categories.objects.get(
                                                nom__exact=categorie)
                                            object_cat.save()
                                            #id_cat = object_cat.id
                                            try:
                                                object_cat.produit.add(
                                                    nw_produit)
                                            except BaseException:
                                                print("doublon")
                                        except categories.DoesNotExist:
                                            no_accent = "".join((c for c in unicodedata.normalize(
                                                'NFD', categorie) if unicodedata.category(c) != 'Mn'))
                                            nw_categorie = categories.objects.create(
                                                nom=categorie, nom_iaccents=no_accent)
                                            nw_categorie.save()
                                            #id_cat = nw_categorie.id
                                            try:
                                                nw_categorie.produit.add(
                                                    nw_produit)
                                            except BaseException:
                                                print('Doublon 2')
                                    liste_store = item.get("stores_tags")
                                    if liste_store:
                                        for stores in item.get(
                                                "stores_tags"):
                                            Vendeurs.objects.create(
                                                produits=nw_produit, nom=stores)

                                    for cle, valeur in liste_nutriment.items():
                                        unit = ""
                                        val_100 = 0
                                        label = ""
                                        if cle.find("_label") == -1:
                                            if cle.find("_unit") != -1:
                                                unit = liste_nutriment.get(
                                                    cle)
                                                label = cle.split('_')
                                                label = label[0]
                                            elif cle.find("_100g") != -1:
                                                val_100 = liste_nutriment.get(
                                                    cle)
                                                label = cle.split('_')
                                                label = label[0]

                                            if len(unit) != 0 or len(
                                                    str(val_100)) != 0:
                                                Nutriments.objects.create(
                                                    produits=nw_produit, nom=label, unite=unit, valeur=val_100)
                                                unit = ""
                                                val_100 = 0


        self.stdout.write(self.style.SUCCESS('commande succes'))