# -*-coding:Utf-8 -*

""" Ce fichier permet de gérer ce qui est lié à la recherche de produit
This file is used to manage what is related to the product search"""

from django.template.loader import *
from .models import Produits, Favoris, categories
from .forms import MultiSelect

import unicodedata


class ClassSearch:
    """ Cette classe fait appel à deux modules, l'un faisant une recherche global
    L'autre faisant une recherche via une liste déroulante sur un id précis
    This class uses two modules, one doing a global search
    The other doing a search via a drop-down list on a specific id"""

    def global_search(search_user, user_current, request, answer_search):
        ''' Utiliser pour les barres de recherche
        Use for search bars '''

        if not answer_search.exists():
            liste_render = search_categorie(search_user, user_current, request)
            liste_results = liste_render[0]
            id_select = liste_render[2]
            if len(liste_results) == 0:
                search_null = True
                dico_answer = {"search": search_user}
                liste_affiche = []
                results_view = multi_answer(
                    liste_render[1], dico_answer, id_select)
                dico_other_produit = results_view[0]
                dico_answer = results_view[1]
            else:
                search_null = False
                dico_answer = liste_results[1]
                liste_affiche = liste_results[0]
                results_view = multi_answer(
                    liste_render[1], dico_answer, id_select)
                dico_other_produit = results_view[0]
                dico_answer = results_view[1]
        else:
            for answer in answer_search:
                produit_caracteristique = selection_produit(answer)
                if len(produit_caracteristique) == 9:
                    break

            liste_render = selection_reponse(
                produit_caracteristique, search_user, user_current)
            search_null = liste_render[2]
            dico_answer = liste_render[1]
            liste_affiche = liste_render[0]
            results_view = multi_answer(
                answer_search, dico_answer, produit_caracteristique[8])
            dico_other_produit = results_view[0]
            dico_answer = results_view[1]

        form_multi = MultiSelect()
        liste_tuple = []
        for select in results_view[0]:
            id_produit = str(select.get('id'))
            nom_produit = select.get('nom') + '[' + select.get('qte') + ']'
            tuple_produit = (id_produit, nom_produit)
            liste_tuple.append(tuple_produit)

        form_multi.fields['select_produit'].choices = liste_tuple
        form_multi.fields['select_produit'].initial = [1]

        dico_answer['error'] = search_null

        return [dico_answer, liste_affiche, dico_other_produit, form_multi]

    def select_search(id_produit, user_current):
        ''' Utiliser lors de l'appel de la liste déroulante et sélectionner un produit particulier
        Use when calling drop-down list and select a particular product'''
        id_prop = Produits.objects.filter(
            id__exact=id_produit).values()
        id_search = Produits.objects.filter(
            id__exact=id_produit)
        for produit in id_search:
            produit_caracteristique = selection_produit(produit)
        search_user = id_prop[0].get('generic_name_fr')
        liste_render = selection_reponse(
            produit_caracteristique, search_user, user_current)
        search_null = liste_render[2]
        dico_answer = liste_render[1]
        liste_affiche = liste_render[0]
        answer_search = Produits.objects.filter(
            generic_name_fr__icontains=search_user)
        results_view = multi_answer(
            answer_search,
            dico_answer,
            produit_caracteristique[8])
        dico_other_produit = results_view[0]
        dico_answer = results_view[1]

        form_multi = MultiSelect()
        liste_tuple = []
        for select in results_view[0]:
            id_produit = str(select.get('id'))
            nom_produit = select.get('nom') + '[' + select.get('qte') + ']'
            tuple_produit = (id_produit, nom_produit)
            liste_tuple.append(tuple_produit)

        form_multi.fields['select_produit'].choices = liste_tuple
        form_multi.fields['select_produit'].initial = [1]

        dico_answer['error'] = search_null

        return [dico_answer, liste_affiche, dico_other_produit, form_multi]


def multi_answer(answer_search, dico_answer, id_select):
    ''' Ce module gère en cas de réponses multiple
    This module manages in case of multiple responses'''
    if len(answer_search) > 1:
        dico_other_produit = other_produit(answer_search, id_select)
        dico_answer['multi'] = True
    else:
        dico_answer['multi'] = False
        dico_other_produit = []

    return [dico_other_produit, dico_answer]


def other_produit(produits, id_select):
    ''' Sélection des produits multiples
    Selection of multiple products'''
    liste_produit = []
    for produit in produits:
        if produit.id != id_select:
            nom = produit.generic_name_fr
            id_produit = produit.id
            qte_produit = produit.nova_groups
            dico = {'nom': nom,
                    'id': id_produit,
                    'qte': qte_produit}
            liste_produit.append(dico)
    return liste_produit


def selection_reponse(caract_prod, search_user, user_current):
    ''' Ramène les propriété du produit à comparé, et la liste des produits
    trouvé dut à cette comparaison
    Brings back the properties of the product to be compared, and the list of products
    found due to this comparison'''

    nutri_score = caract_prod[0]
    image_produit = caract_prod[1]
    ingredient = caract_prod[2]
    url_open = caract_prod[3]
    nom_produit = caract_prod[5]
    image_nutrition = caract_prod[6]
    qte_produit = caract_prod[7]
    id_tbl_produit = caract_prod[8]

    if len(nutri_score) != 0:
        score = nutri_score
        nutrilien = lien_nutriscore(score)
        val_cat_produit = categories.objects.filter(
            produit__exact=id_tbl_produit)
        list_filter_cat = []
        for id_cat in val_cat_produit:
            list_filter_cat.append(id_cat.id)
        compare_search = Produits.objects.filter(grade__lt=score).filter(
            categories__in=list_filter_cat).order_by('grade')
        if not compare_search.exists():
            compare_search = Produits.objects.filter(grade__lte=score).filter(
                categories__in=list_filter_cat).order_by('grade')

    dico_answer = {
        "score": score,
        "search": search_user,
        "image": image_produit,
        "ingredient": ingredient,
        'url': url_open,
        'nom': nom_produit,
        'nutrilien': nutrilien,
        'img_nutri': image_nutrition,
        'qte': qte_produit}

    if not compare_search.exists():
        search_null = True
        liste_reponse = []
    else:
        search_null = False
        liste_reponse = generer_dic_produit(compare_search, user_current)

    return [liste_reponse, dico_answer, search_null]


def selection_produit(answer):
    ''' Ramène les propriétés d'un produit sélectionné
    Brings back the properties of a selected product'''
    id_cat_test = categories.objects.filter(produit__exact=answer.id)
    if answer.grade:
        nutri_score = answer.grade
        image_produit = answer.image_front_url
        ingredient = answer.ingredients_text_fr
        url_open = answer.url_site
        id_produit = answer._id
        nom_produit = answer.generic_name_fr
        image_nutrition = answer.image_nutrition_url
        qte_produit = answer.nova_groups
        if id_cat_test.exists():
            id_tbl_produit = answer.id

    return [
        nutri_score,
        image_produit,
        ingredient,
        url_open,
        id_produit,
        nom_produit,
        image_nutrition,
        qte_produit,
        id_tbl_produit]


def search_categorie(answer_utilisateur, user_current, request):
    ''' Si le produit n'est pas trouvé dans la base produit,
    on lui demande de chercher dans la base catégories.
    If the product is not found in the product database,
    it is asked to search in the categories database '''
    answer_no_accent = "".join((c for c in unicodedata.normalize(
        'NFD', answer_utilisateur) if unicodedata.category(c) != 'Mn'))
    search_categorie = categories.objects.filter(
        nom_iaccents__icontains=answer_no_accent)

    if search_categorie.exists():
        search_produit = Produits.objects.filter().filter(
            categories__id=search_categorie[0].id)
        for answer in search_produit:
            produit_caracteristique = selection_produit(answer)
            if len(produit_caracteristique) == 9:
                break

        id_produit = produit_caracteristique[8]
        liste_render = selection_reponse(
            produit_caracteristique,
            answer_utilisateur,
            user_current)
        all_produit = Produits.objects.filter().filter(categories__in=search_categorie)

    else:
        liste_render = []
        all_produit = []
        id_produit = []

    return [liste_render, all_produit, id_produit]


def generer_dic_produit(compare_search, user_current):
    ''' Créer une réponse avec les produits demandés par l'utilisateur
    Create a response with the products requested by the user '''
    produit = {}
    reponse = []
    for compare in compare_search:
        produit = {}
        if compare.brands_tags:
            produit['nom'] = compare.generic_name_fr
            produit['image'] = compare.image_front_url
            produit['url'] = compare.url_site
            produit['id'] = compare.id
            produit['grade'] = compare.grade

            compare_score = compare.grade
            if compare_score is None:
                nutrilien = "oc_projetHuit/assets/img/nutriscore-NC.png"
            else:
                nutrilien = lien_nutriscore(compare_score)
            produit['url_img_nutri'] = nutrilien
            liste_reponse = generer_liste_reponse(
                produit, reponse, user_current, compare)
    return liste_reponse


def generer_liste_reponse(produit, liste_reponse, user_current, compare):
    ''' vérifie si un produit trouvé n'est pas déjà enregistré dans les favoris
    checks if a product found is not already saved in favorites '''
    save = True
    try:
        user_favoris = Favoris.objects.filter(user__exact=user_current.id)
        for favoris in user_favoris:
            if favoris.produits.id == compare.id:
                save = False
                break
            else:
                save = True
        produit['favoris'] = save
        liste_reponse.append(produit)
    except BaseException:
        produit['favoris'] = save
        liste_reponse.append(produit)
    nw_liste_reponse = sorted(liste_reponse, key=lambda k: k['grade'])
    return nw_liste_reponse


def lien_nutriscore(nutri_point):
    ''' Ramène le lien vers l'image de nutriscore
    Brings back the link to the nutriscore image '''
    compare_score = nutri_point

    if int(compare_score) >= -15 and int(compare_score) <= 0:
        lien = "oc_projetHuit/assets/img/nutriscore-A.png"
    elif int(compare_score) > 0 and int(compare_score) <= 3:
        lien = "oc_projetHuit/assets/img/nutriscore-B.png"
    elif int(compare_score) >= 4 and int(compare_score) <= 11:
        lien = "oc_projetHuit/assets/img/nutriscore-C.png"
    elif int(compare_score) >= 12 and int(compare_score) <= 16:
        lien = "oc_projetHuit/assets/img/nutriscore-D.png"
    elif int(compare_score) >= 17 and int(compare_score) <= 40:
        lien = "oc_projetHuit/assets/img/nutriscore-E.png"

    return lien
