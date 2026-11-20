# Reprise : livres Studio Impulsion (coloriages)

Mémo pour la session Claude qui reprend la gestion depuis l'ordinateur de Denis.

## En ligne sur Amazon (publiés le 15/10/2026, en vente le 17/10)
- Coloriages mystères : Noël cosy (adultes), 90 p., 9,99 €, ASIN B0HN4P82LY : https://www.amazon.fr/dp/B0HN4P82LY
- Coloriages magiques de Noël (enfants dès 6 ans), 90 p., 9,99 €, ASIN B0HN4PP78Z : https://www.amazon.fr/dp/B0HN4PP78Z

## Soumis à KDP le 18/10/2026 (en cours d'examen, jusqu'à 72 h)
- Mandalas de Noël (ados et adultes), 86 p., 9,99 €, ISBN 9798163293605, ID KDP MP45YVSJAP2, ASIN B0HNGRHJBY : https://www.amazon.fr/dp/B0HNGRHJBY (« en cours de publication » le 18/10 à 11 h).
- Fiche : livres/Fiche_KDP_Mandalas_Noel.txt. Catégories retenues : Art et création > Saisonnier ; Art et création > Journaux d'activités ; Coloriage pour adultes > Mandalas et motifs géométriques. Redevance 3,51 €.
- Astuce KDP : si la page de création s'ouvre avec des paramètres openid dans l'URL (après reconnexion), les menus de catégories ne fonctionnent pas. Enregistrer en brouillon puis recharger l'URL propre.

## Pinterest
- Compte pro associé « Studio Impulsion » (pinterest.com/studioimpulsion), tableau public « Coloriages de Noël ».
- Série 1 importée le 17/10 par CSV (16 épingles, 1/jour à 19 h, du 18/10 au 02/11).
- Images hébergées : branche `pinterest-assets` du dépôt ImpulsionDN/cap-vitae (URL raw.githubusercontent.com/ImpulsionDN/cap-vitae/pinterest-assets/...).
- Série 2 importée le 18/10 (48 épingles, 1/jour à 19 h, du 03/11 au 20/12) : 24 nouvelles images (branche pinterest-assets, dossier coloriages-noel-2) + 24 rappels de décembre sur des images existantes. CSV : pinterest/Import_Pinterest_Coloriages_Noel_serie2.csv, générateur sources/promo_pins2.py.
- 19/10 : les imports du 17-18/10 n'avaient créé que la 1re ou les 2 premières épingles (Pinterest refuse les lignes dont le lien est déjà utilisé, et deux titres identiques dans un même fichier). Correction : chaque épingle a un lien unique (amazon.fr/dp/ASIN?pin=s1-03, s2-xx, m-xx) et un titre unique. Complément importé le 19/10 (pinterest/Import_Pinterest_complement_19oct.csv, puis Import_Pinterest_complement2_19oct.csv pour les rappels : Pinterest refuse aussi une image déjà utilisée dans le même fichier, contourné avec ?v=2 sur l'URL de l'image). Vérifié le 19/10 : 96 épingles programmées, aucun créneau manquant du 19/10 au 20/12 (19 h chaque jour, 12 h un jour sur deux pour les Mandalas). Doublons à supprimer à la main : Père Noël 19/10, marché de Noël 03/11, pingouin 04/11.
- Astuce import : la page Pinterest bloque fetch ; construire le CSV dans la page et le déposer par un événement drop sur la zone « Glissez votre fichier ».
- Mandalas importés le 18/10 : 30 épingles, un jour sur deux à 12 h, du 22/10 au 19/12, lien https://www.amazon.fr/dp/B0HNGRHJBY. Images : branche pinterest-assets, dossier mandalas-noel. CSV : pinterest/Import_Pinterest_Mandalas_Noel.csv, générateur sources/promo_pins_mandala.py.
- 19/11 : escape games et calendriers de l'Avent (Adrien Valcourt) : 65 épingles importées sur Studio Impulsion, tableau « Calendrier de l'Avent escape game ». Liste perdue et Horloger : 1/jour à 9 h et 15 h (heure de Paris) du 20/11 au 06/12 ; Kerdaniel et Dame au Lys : en alternance à 21 h du 20/11 au 20/12. Images = couvertures Amazon (m.media-amazon.com/images/I/<id>._SL1000_.jpg?v=N). CSV : pinterest/make_csv_escape_games.py. Heures du CSV en UTC.
- Attention comptes : le panneau navigateur était connecté à Oracle Arcana (même famille de comptes). Un premier import des 65 épingles est parti par erreur sur Oracle Arcana le 19/11 (0 épingle visible 10 min après) : à vérifier et faire supprimer par Denis si elles apparaissent. Studio Impulsion se retrouve via pinterest.com/password/reset en cherchant « studioimpulsion » (e-mail Gmail commençant par dn).
- 19/11 soir : le 1er import n'a créé que 4 épingles sur 65 (Pinterest considère ...jpg?v=2 comme la même image Amazon). Les 4 créées par erreur sur Oracle Arcana ont été supprimées avec l'accord de Denis, ainsi que le tableau vide. Correctif importé sur Studio Impulsion : les 61 autres lignes avec des tailles d'image différentes (_SL999_, _SL998_...). Les deux comptes sont maintenant reliés dans le panneau (menu en haut à droite pour basculer).
- État au 19/11 : 0 vente sur 30 jours (tableau de bord KDP), aucun budget publicité. Il restait 46 épingles coloriages programmées.

## Page auteur Amazon
- 20/11 : nom de plume « Studio Impulsion » créé dans la Plateforme Auteurs (author.amazon.fr, même compte qu'Adrien Valcourt ; bascule par l'icône en haut à droite). Biographie FR publiée, logo SI (promo/Photo_profil_A.png) en photo. Livres rattachés : Noël cosy, Coloriages magiques, Vendre sans forcer ; Mandalas demandé le 20/11 (validation Amazon en attente).
- 20/11 : nom de plume « Élise Arcane » créé (3e et dernier autorisé par compte Amazon : impossible d'ajouter Claire Orage sur ce compte). Biographie FR publiée. En attente de vérification Amazon : ajout des livres refusé et photo grisée tant que ce n'est pas validé. Logo prêt : promo/Photo_profil_Elise_Arcane.png.

## YouTube
- 20/11 : la chaîne « L'œil de Nostradamus » (21 abonnés, 20 vidéos) est renommée « Oracle Arcana », identifiant @OracleArcana, ID UCv92LdHsIAtXUtPtx5UjhOQ, avec l'accord de Denis. Logo et bannière : promo/YouTube_logo_Oracle_Arcana.png, promo/YouTube_banniere_Oracle_Arcana.png. Description et lien vers oracle-arcana.fr. Prévu : Shorts heures miroirs, horoscope, nombres angéliques. Denis a 18 chaînes sur le même compte Google (choix par studio.youtube.com).
- 20/11 : 1er Short publié en public avec l'accord de Denis : 11h11, https://youtube.com/shorts/taypgofADD4 (générateur youtube/render.py + youtube/11h11.json ; texte + musique d'ambiance générée, pas de voix : aucune synthèse vocale accessible depuis le conteneur). Import : fichier injecté depuis raw.githubusercontent dans input[name=Filedata] de YouTube Studio ; « Pas conçue pour les enfants » ; bouton « Publier quand même » si la vérification n'est pas finie. - 20/11 : 36 autres Shorts (toutes les heures miroirs et inversées du site) programmés, un par jour à 18 h du 21/11 au 26/12, vérifiés dans Studio (onglet Shorts, 37 vidéos dont 11h11 publique). Textes : youtube/heures.py ; titres, descriptions, dates : youtube/meta.py ; vidéos et meta.json sur la branche youtube-assets. Musique différente par vidéo (tonalité et accords selon l'heure), demande de Denis. Méthode d'import : JS (fichier depuis raw.githubusercontent, titre/description en innerText + événement input, « pas pour enfants », 3 × Suivant, ouvrir Programmer), puis triple-clic sur le champ date du calendrier (200,193), Ctrl+A, taper « 25 nov. 2026 », Entrée ; focus heure, Ctrl+A, « 18:00 », Entrée ; vérifier date et heure avant de cliquer Programmer (sinon la vidéo part au 21/11 à 00:00).
- Instagram et TikTok : Denis a dit oui pour y publier les mêmes vidéos via Metricool (marque Oracle Arcana reliée à Instagram @oracle_arcana et TikTok @oracle.arcana.fr), quota gratuit à vérifier.
- Attention : les paramètres d'importation par défaut de la chaîne pré-remplissent encore un titre et une description Nostradamus.

## Préférences de Denis
Direct et franc, une action à la fois, instructions prêtes à copier, pas de tirets cadratins, pas de « satisfait ou remboursé », pas de pictogrammes (emoji) dans les titres et descriptions. Il veut que Claude gère tout lui-même.

## Metricool
Compte gratuit, une seule marque (Oracle Arcana), quota mensuel atteint depuis le 13/10 (repart le 01/11). Ne pas l'utiliser pour Studio Impulsion.

## Sources
sources/ : générateurs Python (mosaïques, pixels, mandalas, couvertures, épingles). Les caches d'images ne sont pas inclus.
