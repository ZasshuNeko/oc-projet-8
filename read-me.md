OpenClassRooms - Projet 8

*##Version française*

I. Description
==============

Cette application permet de mettre en place une plateforme de recherche de substitut alimentaire. Avec possibilité de création de compte, de gestion de compte et de gestion des favoris.

II. Installation de python 3
============================

**Windows 10**
> Rendez-vous sur (https://python.org/downloads/)
> Téléchargez la dernière version de python 3.X.X
> Installez-la sur votre système

III. Installation de Git et copie du programme
==============================================

> Rendez-vous sur (https://git-scm.com/downloads)
> Téléchargez la dernière version de git
> Installez cette dernière puis lancer l'application "Git Bash"

Copiez le répertoire du programme avec la commande : `git clone https://github.com/ZasshuNeko/OC-Projet_5.git`


IV. Exécuter le programme
=========================

L’application tourne avec le frameworks django. 
Editer le fichier « settings » que vous trouverez dans le dossier « OCprojetHuit ».

Les variables à éditer sont :
SECRET_KEY : Votre clé de production
ALLOWED_HOST : Les hosts autorisés à se connecter à votre application
DATABASES : La base de données dont va faire appel l’application

Pour tester l’application en local, autoriser l’ip 127.0.0.1, créer une base de données avec postgresql et renseigner les dans DATABASES.

Une fois les données renseignées, lancez l’application en invite de commande en vous mettant à la racine du projet et entrez les commandes suivantes :

> `Python manage.py migrate`

(Cette commande va faire tourner le script 001_initial présent dans polls/migrations. Cette première migration va faire un import de 140 produits, ce nombre limité de produits est dû à la limite gratuite de heroku de 10 000 lignes, vous pouvez à tous moment modifier le fichier de migration pour faire en sorte d’intégrer plus de produits)

> `python manage.py runserver`

Votre application se lance sur l’adresse 127.0.0.1 :8000

V. L’application
================

L’application est composée de différentes fonctionnalités :

Recherche : Deux barres de recherche sont à votre disposition, l’une sur l’index et l’autre intégrée au menu de l’application

Compte : A tout moment les utilisateurs peuvent ouvrir un compte sur votre site. Ils auront alors accès à la fonctionnalité des favoris et de l’affichage sur l’index. Le compte peut être édité à tout moment par l’utilisateur.

Favoris : Tout utilisateur ayant un compte peut sauvegarder un produit de substitution, il apparaitra alors dans la partie « Aliments ». A partir de cette page, l’utilisateur peut demander que l’aliment apparaisse sur son index lors de sa prochaine connexion.

L’application est scindée en trois :

Polls : gérant la recherche et les favoris, c’est aussi dans ce dossier que vous retrouverez le fichier de migration, Template et static.

Compte : gérant la partie compte, création et édition

Auth_app : gérant la partie authentification


VI. Les tests
=============

Les tests pour l’application sont répartis dans les trois grandes parties (polls, compte, auth_app), chacune possède un fichier « tests.py » regroupant tous les tests de cette partie.
Les tests utilisent Sélénium pour la pratique émulation d’une navigation.

La couverture de ces tests est de 87% et ils peuvent être exécutés avec ces lignes :

`coverage run –source=‘.’ manage.py test`
`coverage html`

Vous trouverez les résultats à la racine du projet dans le dossier htmlco


*##English version*

I. Description
==============

This program aims to educate a healthier substitute for a food chosen by the user
It is based on a data set obtained by the Open Food Facts API.

II. Installation of python 3
============================

** Windows 10 **
> Go to (https://python.org/downloads/)
> Download the latest version of python 3.X.X
> Install it on your system

III. Installation of Gît and copy of the program
================================================

> Go to (https://git-scm.com/downloads)
> Download the latest version of git
> Install the latter then launch the "Git Bash" application

Copy the program directory with the command: `git clone https: // github.com / ZasshuNeko / OC-Projet_5.git`


IV. Execute the program
=========================

The application runs with the django frameworks.
Edit the "settings" file that you will find in the "OCprojetHuit" folder.

The variables to be edited are:
SECRET_KEY: Your production key
ALLOWED_HOST: Hosts authorized to connect to your application
DATABASES: The database that the application will use

To test the application locally, authorized ip 127.0.0.1, create a database with postgresql and enter them in DATABASES.

Once the data has been filled in, launch the application at the command prompt by going to the root of the project and entering the following commands:

> `Python manage.py migrate`

(This command will run the 001_initial script present in polls / migrations. This first migration will import 140 products, this limited number of products is due to the free heroku limit of 10,000 lines, you can modify at any time the migration file to ensure that more products are integrated)

> `python manage.py runserver`

Your application starts at the address 127.0.0.1: 8000

V. The program
================

The application is made up of different features:

Search: Two search bars are available to you, one on the index and the other integrated into the application menu

Account: At any time users can open an account on your site. They will then have access to the favorites and index view functionality. The account can be edited at any time by the user.

Favorites: Any user with an account can save a substitute product, it will then appear in the “Food” section. From this page, the user can request that the food appear on their index the next time they log in.

The application is split into three:

Polls: managing search and favorites, it is also in this folder that you will find the migration file, Template and static.

Account: managing the account, creation and edition part

Auth_app: managing the authentication part

VI. The tests
==============

The tests for the application are divided into the three main parts (polls, count, auth_app), each has a "tests.py" file containing all the tests in this part.
The tests use Selenium for practical navigation emulation.

The coverage of these tests is 87% and they can be run with these lines:

`coverage run –source =‘. ’manage.py test`
`coverage html`

You will find the results at the root of the project in the htmlco folder

