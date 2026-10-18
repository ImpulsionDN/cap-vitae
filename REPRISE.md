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
- Astuce import : la page Pinterest bloque fetch ; construire le CSV dans la page et le déposer par un événement drop sur la zone « Glissez votre fichier ».
- Mandalas importés le 18/10 : 30 épingles, un jour sur deux à 12 h, du 22/10 au 19/12, lien https://www.amazon.fr/dp/B0HNGRHJBY. Images : branche pinterest-assets, dossier mandalas-noel. CSV : pinterest/Import_Pinterest_Mandalas_Noel.csv, générateur sources/promo_pins_mandala.py.

## Préférences de Denis
Direct et franc, une action à la fois, instructions prêtes à copier, pas de tirets cadratins, pas de « satisfait ou remboursé ». Il veut que Claude gère tout lui-même.

## Metricool
Compte gratuit, une seule marque (Oracle Arcana), quota mensuel atteint depuis le 13/10 (repart le 01/11). Ne pas l'utiliser pour Studio Impulsion.

## Sources
sources/ : générateurs Python (mosaïques, pixels, mandalas, couvertures, épingles). Les caches d'images ne sont pas inclus.
