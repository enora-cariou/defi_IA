# defi_IA

Défi IA 2023 : 1001 Nights !
Ce repository contient le travail de notre équipe (constituée d'Agathe Gentric, de Juliette Marionneau et d'Enora Cariou) sur le défi IA 2023. Les livrable pour l'évluation du module IA frameworks sont Analysis.ipynb, train.py et app.py. Le dossier travail_continu contient les différents fichiers développés tout au long du semestre mais à utiles pour l'évaluation. 

Les livrables :
- Analysis.ipynb : notebook contenant notre analysis de la base de données et des modèles
- train.py : fichier python permettant l'entrainement du modèle
- app.py : application gradio


Dossier travail_continu :
- Dossier soumissions : contient les fichiers submission.csv déposés sur kaggle ;
- Dossier pricing_requests : contient les fichiers csv consituant la base de données ;
- creation_modele.ipynb : même chose qu'Analysis.ipynb ;
- creation_base_donnees.ipynb : différentes requêtes faites pour construire notre base de données ;
- analyse_hotels_features.ipynb : analyse des features


EVALUATION :

Commandes à exécuter pour faire tourner l'application avec une image docker : 
- après avoir télécharger le repository git, ouvrir un terminal dans le dossier
- exécuter : 
$ sudo docker build -t image_app_hotel [répertoire où se situe le Dockerfile]
$(ex : sudo docker build -t image_app_hotel ~/defi_IA-main/)
$ docker run -it --name cont_app_hotel imahe_app_hotel

L'application va alors tourner et deux adresses URL vont s'afficher. Copier l'adresse HTTPS et coller la dans un navigateur. Vous pourrez alors tester l'application.

Si un problème se produit avec le docker, pour quand même tester l'application sans passer par docker : ouvrir un terminal dans le répertoire et exécuter
$ python app.py








