"""CSV d'import Pinterest pour Mandalas de Noël (30 épingles, un jour sur deux à 12 h, 22/10 -> 19/12/2026)."""
import csv, datetime

BASE = 'https://raw.githubusercontent.com/ImpulsionDN/cap-vitae/pinterest-assets/mandalas-noel/'
LINK = 'https://www.amazon.fr/dp/B0HNGRHJBY'
KW = 'mandala noël adulte, mandala à colorier, coloriage anti stress adulte, coloriage ado, idée cadeau noël ado'
TAG = ' #mandala #coloriage #noel'
P = [
    ('M01_mandala_noel', 'Mandala de Noël à colorier pour ados et adultes',
     "Un mandala de Noël au trait, puis tout en couleurs : 40 mandalas originaux où se cachent sapins, houx, cadeaux et étoiles. Grand format, un mandala par page."),
    ('M02_comment', 'Comment colorier un mandala ? La méthode zen en 3 étapes',
     "Commencez par le centre, avancez anneau après anneau, puis admirez le résultat. Le livre Mandalas de Noël propose 40 modèles pour se détendre pendant les fêtes."),
    ('M03_grille', 'Mandalas de Noël anti-stress : 40 modèles tous différents',
     "Des mandalas festifs, simples ou très détaillés, pour colorier au calme en décembre. Feutres fins, crayons de couleur ou stylos gel. Pour ados et adultes."),
    ('M04_livre', 'Livre de mandalas de Noël à colorier, grand format',
     "40 mandalas de Noël originaux, un dessin par page avec verso blanc, une page pour tester vos couleurs. Format 21,6 x 27,9 cm. Un joli cadeau sous le sapin."),
    ('M05_zen', 'Coloriage zen pour les fêtes : un mandala, un moment de calme',
     "Quand l'agitation des fêtes monte, un mandala à colorier aide à se poser. 40 mandalas de Noël pour ados et adultes, motifs de Noël cachés dans chaque anneau."),
    ('M06_details', 'Mandala de Noël détaillé : sapins, houx et étoiles cachés',
     "Regardez de près : chaque anneau cache un motif de Noël. 40 mandalas à colorier avec des niveaux de détail variés, du plus simple au plus fin."),
    ('M07_trait', 'Mandala de Noël adulte prêt à colorier',
     "Un mandala de Noël au trait, prêt pour vos crayons. Le livre en contient 40, tous différents, avec un seul dessin par page pour éviter les transferts de feutre."),
    ('M08_art_therapie', 'Art-thérapie de Noël : mandala à colorier pour se détendre',
     "Le coloriage de mandalas aide à se concentrer et à relâcher la pression. 40 mandalas de Noël pour s'offrir une pause créative pendant l'hiver."),
    ('M09_cadeau_ado', 'Idée cadeau de Noël pour ado : livre de mandalas à colorier',
     "Un cadeau qui plaît aux ados qui aiment dessiner : 40 mandalas de Noël originaux, à colorier aux feutres fins ou aux stylos gel. Grand format."),
    ('M10_cadeau', 'Le cadeau zen de Noël pour celles et ceux qui aiment colorier',
     "40 mandalas de Noël, un par page, verso blanc, page test pour les couleurs. Un cadeau doux pour une amie, une sœur, une maman ou une mamie."),
    ('M11_niveaux', 'Mandalas de Noël faciles ou détaillés : des niveaux pour tous',
     "Pour débuter ou se perfectionner : 40 mandalas de Noël avec des niveaux de détail variés. Pour ados et adultes, grand format."),
    ('M12_anti_stress', 'Coloriage anti-stress adulte : mandala de Noël aux feutres fins',
     "Des zones fines et régulières, parfaites pour les feutres fins, les crayons de couleur ou les stylos gel. 40 mandalas de Noël pour déconnecter."),
    ('M13_feutres', 'Mandala de Noël à colorier anneau après anneau',
     "Rouge, vert, or : composez votre palette de Noël et avancez anneau après anneau. 40 mandalas originaux à colorier, pour ados et adultes."),
    ('M14_avent', "Calendrier de l'Avent zen : un mandala de Noël par jour",
     "Un mandala par jour du 1er au 24 décembre pour patienter jusqu'à Noël dans le calme. Le livre en contient 40, tous différents."),
    ('M15_trait2', 'Mandala à colorier pour Noël, grand format',
     "Un grand mandala de Noël au trait, avec étoiles et feuilles de houx. 40 modèles à colorier dans le livre Mandalas de Noël, pour ados et adultes."),
    ('M16_cocooning', 'Une pause cocooning à Noël : colorier un mandala',
     "Un plaid, une boisson chaude et un mandala de Noël à colorier. 40 mandalas pour s'offrir des moments de calme pendant les fêtes."),
    ('M17_cadeau_femme', 'Idée cadeau de Noël femme ou ado : mandalas à colorier',
     "40 mandalas de Noël à colorier, anti-stress, grand format. Un petit cadeau apprécié à glisser sous le sapin ou dans une hotte."),
    ('M18_cosy', 'Mandala de Noël cosy à colorier pendant les vacances',
     "Les vacances de Noël sont faites pour ralentir. 40 mandalas de Noël originaux à colorier en famille ou seul, pour ados et adultes."),
    ('M19_adultes', 'Mandalas de Noël pour adultes : zen, détaillés, festifs',
     "Des mandalas pleins de petits motifs de Noël à révéler en couleurs. 40 modèles pour adultes et ados, un dessin par page."),
    ('M20_derniere_minute', 'Dernier cadeau de Noël ? Le livre de mandalas à colorier',
     "Il manque encore un cadeau ? 40 mandalas de Noël à colorier pour ados et adultes, grand format. Disponible sur Amazon."),
    # rappels avec nouveaux textes
    ('M04_livre', "Mandalas de Noël : le livre de coloriage pour l'hiver",
     "40 mandalas de Noël originaux à colorier, motifs de sapins, cadeaux et cloches. Grand format, verso blanc, page test pour vos couleurs."),
    ('M01_mandala_noel', 'Mandala de Noël avant / après : du trait aux couleurs',
     "À gauche le trait, à droite les couleurs : voici ce que donne un mandala de Noël colorié. 40 modèles à découvrir dans le livre."),
    ('M09_cadeau_ado', "Cadeau de Noël pour adolescente qui aime dessiner",
     "40 mandalas de Noël à colorier aux feutres ou aux stylos gel. Une activité calme et créative pour les ados pendant les vacances."),
    ('M14_avent', "Un mandala de Noël par jour jusqu'au 24 décembre",
     "Le compte à rebours a commencé : un mandala de Noël à colorier chaque jour pour se poser avant les fêtes. 40 modèles dans le livre."),
    ('M10_cadeau', 'Cadeau de Noël pour mamie ou maman qui aime colorier',
     "40 mandalas de Noël, un par page, grand format. Un cadeau zen et original pour les fêtes."),
    ('M08_art_therapie', 'Mandala anti-stress : se détendre avant Noël',
     "Les préparatifs de Noël fatiguent ? Un mandala à colorier pour souffler un moment. 40 mandalas de Noël pour ados et adultes."),
    ('M17_cadeau_femme', 'Petit cadeau de Noël pour une collègue : mandalas à colorier',
     "Idéal pour un échange de cadeaux au bureau : 40 mandalas de Noël anti-stress, grand format."),
    ('M03_grille', 'Mandalas de Noël à colorier : 40 modèles festifs',
     "Étoiles, houx, sapins, cloches : 40 mandalas de Noël originaux, simples ou détaillés, pour ados et adultes."),
    ('M20_derniere_minute', 'Dernière minute : cadeau de Noël mandalas à colorier',
     "Encore un cadeau à trouver avant Noël ? 40 mandalas de Noël à colorier pour ados et adultes. Disponible sur Amazon."),
    ('M18_cosy', 'Vacances de Noël : mandalas à colorier en famille',
     "Les vacances commencent ! 40 mandalas de Noël à colorier au calme, pour ados et adultes."),
]
start = datetime.date(2026, 10, 22)
with open('Import_Pinterest_Mandalas_Noel.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Title', 'Media URL', 'Pinterest board', 'Thumbnail', 'Description', 'Link', 'Publish date', 'Keywords'])
    for i, (img, t, d) in enumerate(P):
        day = start + datetime.timedelta(days=2 * i)
        hh = '10' if day < datetime.date(2026, 10, 25) else '11'   # 12 h heure de Paris
        assert len(t) <= 100 and len(d + TAG) <= 500, t
        w.writerow([t, f'{BASE}{img}.jpg', 'Coloriages de Noël', '', d + TAG, LINK, f'{day}T{hh}:00:00', KW])
print(len(P), 'épingles, du', start, 'au', start + datetime.timedelta(days=2 * (len(P) - 1)))
