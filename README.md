# defi_IA

Défi IA 2023 : 1001 Nights !
Ce repository contient le travail de notre équipe (constituée d'Agathe Gentric, de Juliette Marionneau et d'Enora Cariou) sur le défi IA 2023. Les livrables pour l'évluation du module IA frameworks sont Analysis.ipynb, train.py, app.py et le Dockerfile. Le dossier travail_continu contient les différents fichiers développés tout au long du semestre mais pas utiles pour l'évaluation. 

Les livrables :
- Analysis.ipynb : notebook contenant notre analysis de la base de données et des modèles
- train.py : fichier python permettant l'entrainement du modèle
- app.py : application gradio
- Dockerfile (+ requirements.txt qui marche avec le Dockerfile)


Dossier travail_continu :
- Dossier soumissions : contient les fichiers submission.csv déposés sur kaggle ;
- Dossier pricing_requests : contient les fichiers csv consituant la base de données ;
- creation_modele.ipynb : même chose qu'Analysis.ipynb ;
- creation_base_donnees.ipynb : différentes requêtes faites pour construire notre base de données ;
- analyse_hotels_features.ipynb : analyse des features

### Démarche et résultats:
On a distingué de façon de penser notre modèle : celle pour le score kaggle et celle pour obtenir une application aussi performante que possible. Ces démarches et les résultats obtenus sont expliqués en détail dans le notebook Analysis. Nous avons testé différentes manières d'encoder et différents modèles. Finalement nous avons choisi de travailler avec un modèle XGBoost et un encodage en target encoding. </br>

Score kaggle : 35ème sur 76 équipes avec un score de 21.65450.

### EVALUATION :

Commandes à exécuter pour faire tourner l'application avec une image docker : 
- après avoir télécharger le repository git, ouvrir un terminal dans le dossier
#### exécuter :  
- $ sudo docker build -t image_app_hotel [répertoire où se situe le Dockerfile]   
- $ docker run -it --name cont_app_hotel image_app_hotel 
- $ python app.py

Deux adresses URL vont s'afficher (ça peut prendre quelques secondes avant de s'afficher). Copier l'URL public (deuxième lien) et coller le dans un navigateur. Vous pourrez alors tester l'application en choisissant la ville, la date, le stock et la marque. Le prix peut mettre environ 30secondes avant de s'afficher.

Si un problème se produit avec le docker, pour quand même tester l'application sans passer par docker : ouvrir un terminal dans le répertoire et exécuter
$ python app.py








