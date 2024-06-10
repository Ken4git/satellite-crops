import os

### GCP ###

GCP_PROJECT_NAME = os.environ.get("GCP_PROJECT_NAME")
GCP_REGION = os.environ.get("GCP_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

MODEL_TARGET = os.environ.get("MODEL_TARGET")
LOCAL_REGISTRY_PATH = os.path.join(os.path.expanduser('~'), ".lewagon", "satellite-crops", "training_outputs")

### POSTGRES SQL ###

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_INSTANCE = os.environ.get("DB_INSTANCE")

MAPPING = {'Blé tendre d’hiver': 'Blé ',
 'Blé tendre de printemps': 'Blé ',
 'Maïs doux': 'Maïs',
 'Maïs ensilage': 'Maïs',
 'Maïs': 'Maïs',
 "Orge d'hiver": 'Orge',
 'Orge de printemps': 'Orge',
 'Avoine d’hiver': 'Cérélaes(autres)',
 'Avoine de printemps': 'Cérélaes(autres)',
 'Blé dur d’hiver': 'Blé ',
 'Blé dur de printemps': 'Blé ',
 'Blé dur de printemps semé tardivement (après\nle 31/05)': 'Blé ',
 'Autre céréale d’un autre genre': 'Cérélaes(autres)',
 'Autre céréale de genre Fagopyrum': 'Cérélaes(autres)',
 'Autre céréale de genre Phalaris': 'Cérélaes(autres)',
 'Autre céréale de genre Sorghum': 'Cérélaes(autres)',
 'Autre céréale de genre Panicum': 'Cérélaes(autres)',
 'Autre céréale de genre Setaria': 'Cérélaes(autres)',
 'Autre céréale d’hiver de genre Avena': 'Cérélaes(autres)',
 'Autre céréale d’hiver de genre Hordeum': 'Cérélaes(autres)',
 'Autre céréale d’hiver de genre Secale': 'Cérélaes(autres)',
 'Autre céréale d’hiver de genre Triticum': 'Cérélaes(autres)',
 'Autre céréale de\nprintemps de genre Avena': 'Cérélaes(autres)',
 'Autre céréale de printemps de genre Hordeum': 'Cérélaes(autres)',
 'Autre céréale de printemps de genre Secale': 'Cérélaes(autres)',
 'Autre céréale de\nprintemps de genre Triticum': 'Cérélaes(autres)',
 'Autre céréale de printemps de genre Zea': 'Cérélaes(autres)',
 'Épeautre': 'Cérélaes(autres)',
 'Mélange de céréales': 'Cérélaes(autres)',
 'Millet': 'Cérélaes(autres)',
 'Seigle d’hiver': 'Cérélaes(autres)',
 'Seigle de printemps': 'Cérélaes(autres)',
 'Sorgho': 'Cérélaes(autres)',
 'Sarrasin': 'Cérélaes(autres)',
 'Triticale d’hiver': 'Cérélaes(autres)',
 'Triticale de printemps': 'Cérélaes(autres)',
 'Colza d’hiver': 'Colza',
 'Colza de printemps': 'Colza',
 'Tournesol': 'Tournesol',
 'Arachide': 'Oléagineux',
 'Lin non textile d’hiver': 'Oléagineux',
 'Lin non textile de printemps': 'Oléagineux',
 'Mélange d’oléagineux': 'Oléagineux',
 'Navette d’été': 'Oléagineux',
 'Navette d’hiver': 'Oléagineux',
 'Autre oléagineux d’un autre genre': 'Oléagineux',
 'Autre oléagineux d’espèce Helianthus': 'Oléagineux',
 'Œillette': 'Oléagineux',
 'Autre oléagineux d’hiver d’espèce Brassica napus': 'Oléagineux',
 'Autre oléagineux d’hiver d’espèce Brassica rapa': 'Oléagineux',
 'Autre oléagineux de printemps d’espèce Brassica napus': 'Oléagineux',
 'Autre oléagineux de printemps d’espèce Brassica rapa': 'Oléagineux',
 'Soja': 'Oléagineux',
 'Fève': 'Protéagineux',
 'Féverole semée avant le 31/05': 'Protéagineux',
 'Féverole semée tardivement (après le\n31/05)': 'Protéagineux',
 'Lupin doux d’hiver': 'Protéagineux',
 'Lupin doux de printemps semé avant le 31/05': 'Protéagineux',
 'Lupin doux de printemps semé tardivement (après le 31/05)': 'Protéagineux',
 'Mélange de protéagineux (pois et/ou lupin et/ou féverole) prépondérants semés\navant le 31/05 et de céréales': 'Protéagineux',
 'Mélange de protéagineux (pois et/ou lupin et/ou féverole)': 'Protéagineux',
 'Mélange de protéagineux semés tardivement (après le\n31/05)': 'Protéagineux',
 'Autre protéagineux d’un autre genre': 'Protéagineux',
 'Pois d’hiver': 'Protéagineux',
 'Pois de printemps semé avant le 31/05': 'Protéagineux',
 'Pois de printemps semé tardivement (après le 31/05)': 'Protéagineux',
 'Chanvre': 'Chanvre',
 'Lin fibres': 'Oléagineux',
 'Jachère de 5 ans ou moins': 'Prairie / Jachère',
 'Jachère de 6 ans ou plus': 'Prairie / Jachère',
 'Jachère de 6 ans ou plus déclarée comme Surface d’intérêt écologique': 'Prairie / Jachère',
 'Jachère noire': 'Prairie / Jachère',
 'Riz': 'Cérélaes(autres)',
 'Lentille cultivée (non fourragère)': 'Protéagineux',
 'Pois chiche': 'Protéagineux',
 'Betterave fourragère': 'Betterave',
 'Carotte fourragère': 'Légumes',
 'Chou fourrager': 'Légumes',
 'Fourrage composé de céréales et/ou de protéagineux (en proportion < 50%) et/ou de légumineuses\nfourragères (en proportion < 50%)': 'Protéagineux',
 'Dactyle de 5 ans ou moins': 'Prairie / Jachère',
 'Autre fourrage annuel d’un autre genre': 'Prairie / Jachère',
 'Fétuque de 5 ans ou moins': 'Prairie / Jachère',
 'Féverole fourragère\nimplantée pour la récolte 2015': 'Prairie / Jachère',
 'Féverole fourragère implantée pour la récolte 2016': 'Prairie / Jachère',
 'Féverole fourragère implantée pour la récolte 2017': 'Prairie / Jachère',
 'Féverole fourragère implantée pour la récolte 2018': 'Prairie / Jachère',
 'Autre féverole fourragère': 'Prairie / Jachère',
 'Fléole de 5 ans ou moins': 'Prairie / Jachère',
 'Autre plante fourragère sarclée d’un autre genre': 'Prairie / Jachère',
 'Gaillet': 'Prairie / Jachère',
 'Gesse': 'Protéagineux',
 'Autre graminée fourragère pure de 5 ans ou moins': 'Prairie / Jachère',
 'Jarosse implantée pour la récolte 2015': 'Prairie / Jachère',
 'Jarosse implantée pour la récolte 2016': 'Prairie / Jachère',
 'Jarosse implantée pour la récolte 2017': 'Prairie / Jachère',
 'Jarosse implantée pour la récolte 2018': 'Prairie / Jachère',
 'Jarosse déshydratée': 'Prairie / Jachère',
 'Autre jarosse': 'Prairie / Jachère',
 'Lentille fourragère': 'Protéagineux',
 'Autre lupin fourrager d’hiver': 'Prairie / Jachère',
 'Autre lupin fourrager de printemps': 'Prairie / Jachère',
 'Lupin fourrager d’hiver implanté pour la récolte 2015': 'Prairie / Jachère',
 'Lupin fourrager d’hiver implanté pour la récolte 2016': 'Prairie / Jachère',
 'Lupin fourrager d’hiver implanté pour la récolte 2017': 'Prairie / Jachère',
 "Lupin fourrager d'hiver implanté pour la récolte 2018": 'Prairie / Jachère',
 'Lotier implanté pour la récolte 2017': 'Prairie / Jachère',
 'Lotier implanté pour la récolte 2018': 'Prairie / Jachère',
 'Lotier': 'Prairie / Jachère',
 'Lupin fourrager de printemps implanté pour la récolte 2015': 'Prairie / Jachère',
 'Lupin fourrager de printemps implanté pour la récolte 2016': 'Prairie / Jachère',
 'Lupin fourrager de printemps implanté pour la récolte 2017': 'Prairie / Jachère',
 'Lupin fourrager de printemps implanté pour la récolte 2018': 'Prairie / Jachère',
 'Luzerne implantée pour la récolte 2015': 'Prairie / Jachère',
 'Luzerne implantée pour la récolte 2016': 'Prairie / Jachère',
 'Luzerne implantée pour la récolte 2017': 'Prairie / Jachère',
 'Luzerne implantée pour la récolte 2018': 'Prairie / Jachère',
 'Luzerne déshydratée': 'Prairie / Jachère',
 'Autre luzerne': 'Prairie / Jachère',
 'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la\nrécolte 2015 et de céréales': 'Protéagineux',
 'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la\nrécolte 2016 et de céréales': 'Protéagineux',
 'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la\nrécolte 2017 et de céréales': 'Protéagineux',
 'Mélange de légumineuses fourragères prépondérantes implantées pour la\nrécolte 2018 et de céréales et d’oléagineux': 'Protéagineux',
 'Mélilot implanté pour la récolte 2015': 'Prairie / Jachère',
 'Mélilot implanté pour la récolte 2016': 'Prairie / Jachère',
 'Mélilot implanté pour la récolte 2017': 'Prairie / Jachère',
 'Mélilot implanté pour la récolte 2018': 'Prairie / Jachère',
 'Mélilot déshydraté': 'Prairie / Jachère',
 'Autre mélilot': 'Prairie / Jachère',
 'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la récolte 2015 et\nd’herbacées ou de graminées fourragères': 'Protéagineux',
 'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la récolte 2016 et\nd’herbacées ou de graminées fourragères': 'Protéagineux',
 'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la récolte 2017 et\nd’herbacées ou de graminées fourragères': 'Protéagineux',
 'Minette implanté pour la récolte 2017': 'Prairie / Jachère',
 'Minette implanté pour la récolte 2018': 'Prairie / Jachère',
 'Minette': 'Prairie / Jachère',
 'Mélange de légumineuses fourragères implantées\npour la récolte 2015 (entre elles)': 'Protéagineux',
 'Mélange de légumineuses fourragères implantées pour la récolte 2016\n(entre elles)': 'Protéagineux',
 'Mélange de légumineuses fourragères implantées\npour la récolte 2017 (entre elles)': 'Protéagineux',
 'Mélange de légumineuses fourragères implantées pour la récolte 2018 (entre elles)': 'Protéagineux',
 'Mélange de légumineuses fourragères prépondérantes et de\ncéréales et/ou d’oléagineux': 'Protéagineux',
 'Mélange de légumineuses déshydratées (entre elles)': 'Protéagineux',
 'Mélange de\nlégumineuses fourragères (entre elles)': 'Protéagineux',
 'Mélange de légumineuses prépondérantes au semis et de graminées fourragères de 5 ans ou\nmoins': 'Protéagineux',
 'Moha': 'Prairie / Jachère',
 'Navet fourrager': 'Légumes',
 'Pâturin commun de 5 ans ou moins': 'Prairie / Jachère',
 'Autre pois fourrager d’hiver': 'Prairie / Jachère',
 'Autre pois fourrager de printemps': 'Prairie / Jachère',
 'Pois fourrager d’hiver implanté pour la récolte 2015': 'Prairie / Jachère',
 'Pois fourrager d’hiver implanté pour la récolte 2016': 'Prairie / Jachère',
 'Pois fourrager d’hiver implanté pour la récolte 2017': 'Prairie / Jachère',
 'Pois fourrager d’hiver implanté pour la récolte 2018': 'Prairie / Jachère',
 'Pois fourrager de printemps implanté pour la récolte 2015': 'Prairie / Jachère',
 'Pois fourrager de printemps implanté pour la récolte 2016': 'Prairie / Jachère',
 'Pois fourrager de printemps implanté pour la récolte 2017': 'Prairie / Jachère',
 'Pois fourrager de printemps implanté pour la récolte 2018': 'Prairie / Jachère',
 'Radis fourrager': 'Légumes',
 'Sainfoin implanté pour la récolte 2015': 'Prairie / Jachère',
 'Sainfoin implanté pour la récolte 2016': 'Prairie / Jachère',
 'Sainfoin implanté pour la récolte 2017': 'Prairie / Jachère',
 'Sainfoin implanté pour la récolte 2018': 'Prairie / Jachère',
 'Sainfoin déshydraté': 'Prairie / Jachère',
 'Autre sainfoin': 'Prairie / Jachère',
 'Serradelle implantée pour la récolte 2015': 'Prairie / Jachère',
 'Serradelle implantée pour la récolte 2016': 'Prairie / Jachère',
 'Serradelle implantée pour la récolte 2017': 'Prairie / Jachère',
 'Serradelle implantée pour la récolte 2018': 'Prairie / Jachère',
 'Serradelle déshydratée': 'Prairie / Jachère',
 'Autre serradelle': 'Prairie / Jachère',
 'Trèfle implanté pour la récolte 2015': 'Prairie / Jachère',
 'Trèfle implanté pour la récolte 2016': 'Prairie / Jachère',
 'Trèfle implanté pour la récolte 2017': 'Prairie / Jachère',
 'Trèfle implanté pour la récolte 2018': 'Prairie / Jachère',
 'Trèfle déshydraté': 'Prairie / Jachère',
 'Autre trèfle': 'Prairie / Jachère',
 'Vesce implantée pour la récolte 2015': 'Prairie / Jachère',
 'Vesce implantée pour la récolte 2016': 'Prairie / Jachère',
 'Vesce implantée pour la récolte 2017': 'Prairie / Jachère',
 'Vesce implantée pour la récolte 2018': 'Prairie / Jachère',
 'Vesce déshydratée': 'Prairie / Jachère',
 'Autre vesce': 'Prairie / Jachère',
 'X-Felium de 5 ans ou moins': 'Prairie / Jachère',
 'Bois pâturé': 'Prairie / Jachère',
 'Surface pastorale - herbe prédominante et ressources fourragères ligneuses présentes': 'Prairie / Jachère',
 'Surface pastorale - ressources fourragères ligneuses prédominantes': 'Prairie / Jachère',
 'Prairie permanente - herbe prédominante (ressources fourragères\nligneuses absentes ou peu présentes)': 'Prairie / Jachère',
 'Prairie en rotation longue (6 ans ou plus)': 'Prairie / Jachère',
 'Autre prairie temporaire de 5 ans ou moins': 'Prairie / Jachère',
 'Ray-grass de 5 ans ou moins': 'Prairie / Jachère',
 'Agrume': 'Vergers',
 'Ananas': 'Vergers',
 'Avocat': 'Vergers',
 'Banane créole (fruit et légume) - autre': 'Vergers',
 'Banane créole (fruit et légume) - fermage': 'Vergers',
 'Banane créole (fruit et légume) - indivision': 'Vergers',
 'Banane créole (fruit et légume) - propriété ou faire valoir direct': 'Vergers',
 'Banane créole (fruit et légume) - réforme foncière': 'Vergers',
 'Banane export - autre': 'Vergers',
 'Banane export - fermage': 'Vergers',
 'Banane export - indivision': 'Vergers',
 'Banane export - propriété ou faire valoir direct': 'Vergers',
 'Banane export - réforme foncière': 'Vergers',
 'Café / Cacao': 'Vergers',
 'Cerise bigarreau pour transformation': 'Vergers',
 'Petit fruit rouge': 'Vergers',
 'Prune d’Ente pour transformation': 'Vergers',
 'Pêche Pavie pour transformation': 'Vergers',
 'Poire Williams pour transformation': 'Vergers',
 'Verger (DROM)': 'Vergers',
 'Verger': 'Vergers',
 'Restructuration du vignoble': 'Vergers',
 'Vigne : raisins de cuve': 'Vergers',
 'Vigne : raisins de cuve non en production': 'Vergers',
 'Vigne : raisins de table': 'Vergers',
 'Caroube': 'Protéagineux',
 'Châtaigne': 'Protéagineux',
 'Noisette': 'Protéagineux',
 'Noix': 'Protéagineux',
 'Pistache': 'Protéagineux',
 'Oliveraie': 'Vergers',
 'Aneth': 'Légumes',
 'Angélique': 'Légumes',
 'Anis': 'Légumes',
 'Bardane': 'Légumes',
 'Basilic': 'Légumes',
 'Bourrache de 5 ans ou moins': 'Légumes',
 'Betterave non fourragère\n/ Bette': 'Betterave',
 'Carvi': 'Légumes',
 'Chardon Marie': 'Légumes',
 'Ciboulette': 'Légumes',
 'Cameline': 'Légumes',
 'Camomille': 'Légumes',
 'Coriandre': 'Légumes',
 'Cerfeuil': 'Légumes',
 'Cumin': 'Légumes',
 'Curcuma': 'Légumes',
 'Estragon': 'Légumes',
 'Fenouil': 'Légumes',
 'Fenugrec': 'Légumes',
 'Houblon': 'Légumes',
 'Lavande / Lavandin': 'Légumes',
 'Mauve': 'Légumes',
 'Mélisse': 'Légumes',
 'Millepertuis': 'Légumes',
 'Moutarde': 'Légumes',
 'Marjolaine / Origan': 'Légumes',
 'Menthe': 'Légumes',
 'Ortie': 'Légumes',
 'Oseille': 'Légumes',
 'Plante aromatique (autre que vanille)': 'Légumes',
 'Plante médicinale': 'Légumes',
 'Autre plante à parfum, aromatique et médicinale annuelle': 'Légumes',
 'Plante à parfum (autre que géranium et vétiver)': 'Légumes',
 'Autre plante à parfum, aromatique et médicinale pérenne': 'Légumes',
 'Persil': 'Légumes',
 'Psyllium noir de Provence': 'Légumes',
 'Plantain psyllium': 'Légumes',
 'Romarin': 'Légumes',
 'Sauge': 'Légumes',
 'Sarriette': 'Légumes',
 'Tabac': 'Légumes',
 'Thym': 'Légumes',
 'Tomate pour transformation': 'Légumes',
 'Valériane': 'Légumes',
 'Vanille sous bois': 'Légumes',
 'Vanille': 'Légumes',
 'Vanille verte': 'Légumes',
 'Ylang-ylang': 'Légumes',
 'Ail': 'Légumes',
 'Artichaut': 'Légumes',
 'Aubergine': 'Légumes',
 'Bleuet': 'Légumes',
 'Bugle rampante': 'Légumes',
 'Carotte': 'Légumes',
 'Concombre / Cornichon': 'Légumes',
 'Courgette / Citrouille': 'Légumes',
 'Céleri': 'Légumes',
 'Chicorée / Endive / Scarole': 'Légumes',
 'Chou': 'Légumes',
 'Courge musquée / Butternut': 'Légumes',
 'Cresson alénois de 5 ans ou moins': 'Légumes',
 'Cornille': 'Légumes',
 'Cresson': 'Légumes',
 'Culture sous serre hors sol': 'Légumes',
 'Dolique': 'Légumes',
 'Épinard': 'Légumes',
 'Autre légume ou fruit annuel': 'Légumes',
 'Autre légume ou fruit pérenne': 'Légumes',
 'Fraise': 'Légumes',
 'Géranium': 'Légumes',
 'Haricot / Flageolet': 'Légumes',
 'Horticulture ornementale de plein champ': 'Légumes',
 'Horticulture ornementale sous abri': 'Légumes',
 'Laitue / Batavia / Feuille de chêne': 'Légumes',
 'Légume sous abri': 'Légumes',
 'Mâche': 'Légumes',
 'Melon': 'Légumes',
 'Marguerite': 'Légumes',
 'Navet': 'Légumes',
 'Oignon / Échalote': 'Légumes',
 'Panais': 'Légumes',
 'Pâquerette': 'Légumes',
 'Pastèque': 'Légumes',
 'Primevère': 'Légumes',
 'Poireau': 'Légumes',
 'Potiron / Potimarron': 'Légumes',
 'Petits pois': 'Légumes',
 'Pensée': 'Légumes',
 'Pomme de terre de consommation': 'Pomme de terre',
 'Pomme de terre féculière': 'Pomme de terre',
 'Poivron / Piment': 'Légumes',
 'Radis': 'Légumes',
 'Roquette': 'Légumes',
 'Rutabaga': 'Légumes',
 'Salsifis': 'Légumes',
 'Tomate': 'Légumes',
 'Topinambour': 'Légumes',
 'Véronique': 'Légumes',
 'Canne à sucre - autre': 'Cérélaes(autres)',
 'Canne à sucre - fermage': 'Cérélaes(autres)',
 'Canne à sucre - indivision': 'Cérélaes(autres)',
 'Canne à sucre - propriété ou faire valoir direct': 'Cérélaes(autres)',
 'Canne à sucre - réforme foncière': 'Cérélaes(autres)',
 'Autre culture non précisée dans la liste (admissible)': 'Prairie / Jachère',
 'Bande admissible le long\nd’une forêt avec production': 'Prairie / Jachère',
 'Bande admissible le long d’une forêt sans production': 'Prairie / Jachère',
 'Bordure de champ': 'Prairie / Jachère',
 'Brome de 5 ans ou moins': 'Prairie / Jachère',
 'Bande tampon': 'Prairie / Jachère',
 'Châtaigneraie entretenue par des porcins ou des petits\nruminants': 'Prairie / Jachère',
 'Chênaie entretenue par des porcins ou des petits ruminants': 'Prairie / Jachère',
 'Cultures conduites en interrangs : 2 cultures\nreprésentant chacune plus de 25%': 'Prairie / Jachère',
 'Cultures conduites en interrangs : 3 cultures représentant chacune plus de 25%': 'Prairie / Jachère',
 'Culture sous abattis': 'Prairie / Jachère',
 'Miscanthus': 'Prairie / Jachère',
 'Autre mélange de plantes fixant l’azote': 'Prairie / Jachère',
 'Marais salant': 'Prairie / Jachère',
 'Nyger': 'Prairie / Jachère',
 'Phacélie de 5 ans ou moins': 'Prairie / Jachère',
 'Pépinière': 'Prairie / Jachère',
 'Roselière': 'Prairie / Jachère',
 'Surface boisée sur une ancienne terre agricole': 'Prairie / Jachère',
 'Surface non agricole non visible sur l’orthophotographie': 'Prairie / Jachère',
 'Surface agricole temporairement non exploitée': 'Prairie / Jachère',
 'Tubercule tropical': 'Prairie / Jachère',
 'Taillis à courte rotation': 'Prairie / Jachère',
 'Truffière (chênaie de plants mycorhizés)': 'Prairie / Jachère',
 'Vétiver': 'Prairie / Jachère',
 'Culture inconnue': 'Prairie / Jachère'}

LABELS = {0: 'Betterave',
            1: 'Blé ',
            2: 'Chanvre',
            3: 'Colza',
            4: 'Cérélaes(autres)',
            5: 'Légumes',
            6: 'Maïs',
            7: 'Oléagineux',
            8: 'Orge',
            9: 'Pomme de terre',
            10: 'Prairie / Jachère',
            11: 'Protéagineux',
            12: 'Tournesol',
            13: 'Vergers'}
### EO LEARN ###

DPT = os.environ.get("DPT")
ZONE_TYPE = os.environ.get("ZONE_TYPE")
LOCAL_CRS = os.environ.get("LOCAL_CRS")
DATA_PATH = os.path.join(os.path.dirname(os.getcwd()), "satellite-crops", "data", "departments", DPT)
EOPATCH_FOLDER = os.path.join(DATA_PATH, "eopatches")
EOPATCH_SAMPLES_FOLDER = os.path.join(DATA_PATH, "eopatches_sampled")
RESULTS_FOLDER = os.path.join(DATA_PATH, "results")
