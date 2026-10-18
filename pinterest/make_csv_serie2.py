"""Génère le CSV d'import Pinterest de la série 2 (3 novembre -> 20 décembre 2026)."""
import csv, datetime

BASE = 'https://raw.githubusercontent.com/ImpulsionDN/cap-vitae/pinterest-assets/'
LINK = {'a': 'https://www.amazon.fr/dp/B0HN4P82LY', 'k': 'https://www.amazon.fr/dp/B0HN4PP78Z'}
KW = {'a': 'coloriage mystère adulte, coloriage par numéros adulte, coloriage noël adulte, coloriage anti stress, idée cadeau noël femme',
      'k': 'coloriage magique enfant, coloriage par numéros enfant, coloriage noël enfant, activité noël enfant, idée cadeau enfant 6 ans'}
BOARD = 'Coloriages de Noël'
TAG = {'a': ' #coloriageadulte #noel', 'k': ' #coloriageenfant #noel'}

# (livre, image, titre, description)
NEW = [
    ('a', '01_A09_marche.jpg', 'Coloriage mystère adulte : le marché de Noël à colorier par numéros',
     "Les chalets, les guirlandes et les lumières du marché de Noël apparaissent zone après zone. 40 coloriages mystères de Noël cosy pour adultes, solutions incluses, un dessin par page."),
    ('k', '02_K09_pingouin.jpg', 'Coloriage magique de Noël : le pingouin caché, dès 6 ans',
     "Ton enfant lit le numéro de chaque case, prend la bonne couleur, et le pingouin de Noël apparaît ! 40 coloriages par numéros avec grandes cases, solutions à la fin du livre."),
    ('a', '03_A10_buche.jpg', 'Coloriage par numéros adulte : la bûche de Noël',
     "Un coloriage gourmand qui se révèle sous vos crayons. Environ 500 zones par dessin pour un vrai moment de détente pendant les fêtes. 40 coloriages mystères de Noël, grand format."),
    ('k', '04_K10_train.jpg', 'Coloriage magique enfant : le train de Noël à découvrir',
     "Case après case, le train du Père Noël sort de la page. 40 coloriages magiques de Noël pour les 6 à 10 ans : chiffres de 1 à 12, grandes cases, une activité calme sans écran."),
    ('a', '05_A11_comment.jpg', 'Comment faire un coloriage mystère ? Le principe en 3 étapes',
     "Chaque zone porte un numéro, chaque numéro correspond à une couleur, et le dessin de Noël apparaît peu à peu. Le coloriage par numéros pour adultes, simple et relaxant. 40 dessins cosy, solutions incluses."),
    ('k', '06_K11_comment.jpg', 'Coloriage magique : comment ça marche ? Facile dès 6 ans',
     "1. Je lis le numéro de la case. 2. Je prends la bonne couleur. 3. L'image cachée apparaît ! Un cahier de 40 coloriages magiques de Noël qui fait travailler les chiffres et la concentration."),
    ('a', '07_A12_casse_noisette.jpg', 'Coloriage mystère de Noël : Casse-noisette pour adultes',
     "Le soldat Casse-noisette se dévoile numéro après numéro. 40 coloriages mystères de Noël cosy, anti-stress, pour crayons de couleur ou feutres fins. Verso blanc, solutions incluses."),
    ('k', '08_K12_chouette.jpg', 'Coloriage par numéros enfant : la chouette de Noël',
     "Une jolie chouette se cache dans la grille. 40 coloriages magiques de Noël dès 6 ans, avec grandes cases et solutions à la fin. Parfait pour les mercredis et les vacances."),
    ('a', '09_A13_zen_hiver.jpg', "Coloriage zen pour l'hiver : 40 dessins de Noël à révéler",
     "Marché de Noël, bûche, forêt enneigée, écureuil, cloches... 40 coloriages mystères pour adultes à faire au calme, au coin du feu. Un dessin par page, grand format 21,6 x 27,9 cm."),
    ('k', '10_K13_avent.jpg', "Calendrier de l'Avent à colorier pour enfant : un coloriage par jour",
     "Une idée pour patienter jusqu'à Noël : un coloriage magique par jour, du 1er au 24 décembre. Le cahier en contient 40, avec grandes cases et solutions. Dès 6 ans."),
    ('a', '11_A14_cadeau_amie.jpg', "Idée cadeau de Noël pour une amie qui aime colorier",
     "Un petit cadeau qui fait plaisir à une amie, une collègue ou une sœur : 40 coloriages mystères de Noël cosy, anti-stress, solutions incluses. À glisser sous le sapin ou dans un calendrier de l'Avent."),
    ('k', '12_K14_cadeau_enfant.jpg', 'Idée cadeau de Noël pour enfant de 6 à 10 ans : coloriages magiques',
     "Un cadeau simple et utile pour les vacances : 40 coloriages magiques de Noël, grandes cases faciles, solutions à la fin. Idéal pour un neveu, une nièce, un petit-fils ou une petite-fille."),
    ('a', '13_A15_ecureuil.jpg', "Coloriage par numéros adulte : l'écureuil sous la neige",
     "Un petit écureuil apparaît dans la neige, zone après zone. 40 coloriages mystères de Noël pour adultes, 1 à 2 heures de détente par dessin. Solutions incluses."),
    ('k', '14_K15_renard.jpg', 'Coloriage magique de Noël : le renard dans la neige',
     "Le renard se cache dans les cases numérotées. Ton enfant colorie et le découvre petit à petit ! 40 coloriages par numéros de Noël dès 6 ans, solutions incluses."),
    ('a', '15_A16_foret.jpg', 'Coloriage mystère anti-stress : la forêt enneigée',
     "Sapins, neige et silence : un paysage d'hiver à révéler en coloriant chaque zone selon son numéro. 40 coloriages mystères de Noël pour adultes, un dessin par page."),
    ('k', '16_K16_cadeaux.jpg', 'Coloriage magique enfant : les cadeaux sous le sapin',
     "Quelle surprise se cache sous le sapin ? Case après case, les cadeaux apparaissent ! 40 coloriages magiques de Noël pour les 6 à 10 ans, grandes cases et solutions."),
    ('a', '17_A17_avent.jpg', "Calendrier de l'Avent pour adultes : un coloriage mystère par jour",
     "Offrez-vous une pause chaque jour de décembre : un coloriage mystère de Noël par jour jusqu'au 24. Le livre en contient 40, anti-stress, solutions incluses."),
    ('k', '18_K17_vacances.jpg', 'Occuper les enfants pendant les vacances de Noël, sans écran',
     "40 coloriages magiques de Noël pour des moments calmes à la maison ou chez papi et mamie. Grandes cases, chiffres faciles, solutions à la fin. Dès 6 ans."),
    ('a', '19_A18_lanterne.jpg', 'Coloriage par numéros de Noël : la lanterne pour adultes',
     "Une lanterne chaleureuse se révèle numéro après numéro. 40 coloriages mystères de Noël cosy, grand format, verso blanc pour éviter les transferts de feutre."),
    ('k', '20_K18_lutin.jpg', 'Coloriage magique de Noël : le lutin à découvrir',
     "Le lutin du Père Noël se cache dans la grille ! 40 coloriages par numéros de Noël avec grandes cases, pour les enfants de 6, 7, 8 ans. Solutions incluses."),
    ('a', '21_A19_mamie.jpg', 'Idée cadeau de Noël pour mamie : livre de coloriages mystères',
     "Pour une mamie qui aime colorier : 40 dessins de Noël cosy à révéler par numéros, un dessin par page, grand format, solutions incluses. Un cadeau doux et relaxant."),
    ('k', '22_K19_7_ans.jpg', 'Coloriage de Noël pour enfant de 7 ans : 40 images magiques',
     "Bougie, couronne, chaussettes, village enneigé, biscuits... 40 images de Noël à découvrir case par case. Le cahier de coloriage magique idéal pour les 6 à 10 ans."),
    ('a', '23_A20_cloches.jpg', 'Coloriage mystère adulte anti-stress : les cloches de Noël',
     "Les cloches de Noël apparaissent sous vos crayons. Environ 500 zones par dessin, 40 coloriages par numéros pour adultes, solutions incluses. Disponible sur Amazon."),
    ('k', '24_K20_cahier.jpg', 'Cahier de coloriage de Noël pour enfant : à glisser dans la hotte',
     "Le cahier des vacances de Noël : 40 coloriages magiques dès 6 ans, chiffres de 1 à 12, grandes cases, solutions à la fin. Un petit cadeau qui occupe longtemps."),
]

S1 = 'coloriages-noel/'
S2 = 'coloriages-noel-2/'
# Rappels de décembre : images déjà publiées, nouveaux textes orientés cadeau et dernière minute
REMIND = [
    ('a', S1 + '15_A08_idee_cadeau.jpg', 'Cadeau de Noël pas cher et original : coloriages mystères adultes',
     "Vous cherchez un petit cadeau qui sort de l'ordinaire ? 40 coloriages mystères de Noël cosy, anti-stress, solutions incluses. Pensez à commander tôt pour le recevoir avant Noël."),
    ('k', S1 + '16_K08_idee_cadeau.jpg', 'Cadeau de Noël pour enfant : cahier de coloriages magiques',
     "Pour remplir la hotte : 40 coloriages magiques de Noël dès 6 ans, grandes cases faciles, solutions incluses. Pensez à commander tôt pour le recevoir avant Noël."),
    ('a', S1 + '01_A01_chalet_avant_apres.jpg', 'Avant / après : le chalet de Noël en coloriage mystère',
     "Une page de numéros, quelques crayons, et un chalet sous la neige apparaît. 40 coloriages par numéros de Noël pour adultes, à faire en décembre pour se détendre."),
    ('k', S1 + '02_K01_pere_noel_avant_apres.jpg', 'Avant / après : le Père Noël caché dans le coloriage magique',
     "Le Père Noël apparaît case après case ! Une activité de décembre pour les enfants dès 6 ans : 40 coloriages magiques de Noël, solutions incluses."),
    ('a', S2 + '05_A11_comment.jpg', 'Coloriage mystère : le loisir créatif relaxant de décembre',
     "Pas besoin de savoir dessiner : il suffit de suivre les numéros. 40 coloriages mystères de Noël pour adultes, anti-stress, solutions incluses. Idée cadeau pour une femme ou une maman."),
    ('k', S2 + '06_K11_comment.jpg', 'Activité de Noël facile pour enfant : le coloriage par numéros',
     "Lire un chiffre, trouver la couleur, découvrir l'image : une activité qui plaît dès 6 ans. 40 coloriages magiques de Noël pour les après-midis de décembre."),
    ('a', S1 + '03_A02_cadeau_maman.jpg', 'Cadeau de Noël pour maman : livre de coloriage anti-stress',
     "Une pause rien que pour elle pendant les fêtes : 40 coloriages mystères de Noël cosy, un dessin par page, grand format, solutions incluses."),
    ('k', S1 + '04_K02_sans_ecran.jpg', 'Vacances de Noël sans écran : coloriages magiques pour enfants',
     "Les vacances approchent ! 40 coloriages magiques de Noël pour occuper les enfants au calme. Grandes cases, chiffres faciles, solutions à la fin. Dès 6 ans."),
    ('a', S1 + '07_A04_livre.jpg', 'Livre de coloriage pour adultes Noël cosy : 40 dessins',
     "Chocolat chaud, chalet, renne, marché de Noël, chat au coin du feu : 40 coloriages mystères pour adultes à colorier par numéros. Verso blanc, solutions incluses."),
    ('k', S1 + '08_K04_livre.jpg', 'Livre de coloriage magique de Noël pour enfants dès 6 ans',
     "40 images de Noël à découvrir case par case, grandes cases et chiffres faciles. Le cahier idéal pour les vacances de Noël, solutions incluses."),
    ('a', S2 + '09_A13_zen_hiver.jpg', "Coloriage pour adultes : se détendre pendant les fêtes de fin d'année",
     "Quand l'agitation des fêtes monte, une page de coloriage mystère fait du bien. 40 dessins de Noël cosy à révéler, solutions incluses."),
    ('k', S2 + '10_K13_avent.jpg', "Idée calendrier de l'Avent : un coloriage magique par jour",
     "Il reste quelques jours avant Noël : un coloriage magique par jour pour patienter ! 40 images de Noël dès 6 ans, grandes cases, solutions à la fin."),
    ('a', S1 + '05_A03_chat_avant_apres.jpg', 'Coloriage mystère : le chat de Noël à la fenêtre',
     "Un chat qui regarde la neige tomber, à révéler numéro après numéro. 40 coloriages par numéros de Noël pour adultes, un cadeau doux pour les amoureux des chats."),
    ('k', S1 + '06_K03_renne_avant_apres.jpg', 'Coloriage magique de Noël : le renne du Père Noël',
     "Le petit renne apparaît case après case ! 40 coloriages par numéros de Noël pour les enfants dès 6 ans, solutions incluses."),
    ('a', S1 + '09_A05_500_zones.jpg', 'Coloriage par numéros difficile pour adultes : 500 zones',
     "Pour celles et ceux qui aiment les longues séances : environ 500 zones par dessin, 1 à 2 heures de coloriage. 40 coloriages mystères de Noël, solutions incluses."),
    ('k', S1 + '10_K05_grandes_cases.jpg', 'Coloriage par numéros facile : grandes cases pour enfants',
     "Des grandes cases et des chiffres de 1 à 12, parfaits pour les petites mains. 40 coloriages magiques de Noël dès 6 ans."),
    ('a', S2 + '21_A19_mamie.jpg', 'Dernière minute : cadeau de Noël pour mamie qui aime colorier',
     "Encore un cadeau à trouver ? 40 coloriages mystères de Noël cosy, grand format, solutions incluses. Disponible sur Amazon."),
    ('k', S2 + '12_K14_cadeau_enfant.jpg', 'Dernière minute : cadeau de Noël pour enfant de 6 à 10 ans',
     "Il manque un cadeau ? 40 coloriages magiques de Noël, grandes cases faciles, solutions à la fin. Disponible sur Amazon."),
    ('a', S1 + '11_A06_anti_stress.jpg', 'Coloriages de Noël anti-stress pour adultes',
     "Chalet, renne, marché de Noël, boule à neige : 40 coloriages mystères pour souffler pendant les préparatifs. Un dessin par page, solutions incluses."),
    ('k', S1 + '12_K06_enfant_6_ans.jpg', 'Coloriage de Noël pour enfant de 6 ans : renne, lutin, traîneau',
     "Renne, lutin, traîneau, cadeaux, renard... 40 coloriages magiques de Noël à découvrir case par case. Le cadeau qui occupe pendant les vacances."),
    ('a', S1 + '13_A07_avant_apres.jpg', 'Coloriage mystère avant / après : le chocolat chaud de Noël',
     "Le chocolat chaud se révèle sous vos crayons. 40 coloriages par numéros de Noël cosy pour adultes, solutions incluses."),
    ('k', S1 + '14_K07_avant_apres.jpg', 'Coloriage magique avant / après : le bonhomme de neige',
     "Le bonhomme de neige apparaît case après case ! 40 coloriages par numéros de Noël pour les enfants dès 6 ans, solutions incluses."),
    ('a', S2 + '17_A17_avent.jpg', 'Petit cadeau de Noël pour une collègue ou une amie',
     "Un cadeau simple et apprécié : 40 coloriages mystères de Noël anti-stress, solutions incluses. Parfait pour un échange de cadeaux au bureau."),
    ('k', S2 + '24_K20_cahier.jpg', "Cahier de coloriage pour les vacances de Noël, dès 6 ans",
     "Les vacances commencent ! 40 coloriages magiques de Noël pour les enfants de 6 à 10 ans, grandes cases, solutions à la fin."),
]

rows = [(k, S2 + img, t, d) for k, img, t, d in NEW] + REMIND
start = datetime.date(2026, 11, 3)
with open('Import_Pinterest_Coloriages_Noel_serie2.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Title', 'Media URL', 'Pinterest board', 'Thumbnail', 'Description', 'Link', 'Publish date', 'Keywords'])
    for i, (k, path, t, d) in enumerate(rows):
        day = start + datetime.timedelta(days=i)
        assert len(t) <= 100 and len(d + TAG[k]) <= 500, t
        w.writerow([t, BASE + path, BOARD, '', d + TAG[k], LINK[k], f'{day}T18:00:00', KW[k]])
print(len(rows), 'épingles, du', start, 'au', start + datetime.timedelta(days=len(rows) - 1))
