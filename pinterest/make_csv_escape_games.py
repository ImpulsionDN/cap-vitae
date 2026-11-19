"""CSV Pinterest pour les escape games d'Adrien Valcourt (20/11 -> 20/12/2026).
Images : couvertures Amazon (une URL unique par épingle grâce à ?v=N). Liens uniques (?pin=...)."""
import csv, datetime

IMG = {'liste': '71pJ98Uz1YL', 'horloger': '71LEHx63JwL', 'kerdaniel': '713ClZNjL5L', 'dame': '71B91t3U9ML'}
ASIN = {'liste': 'B0HQFX7D6R', 'horloger': 'B0HPKXPL4Q', 'kerdaniel': 'B0HQCDQ31Q', 'dame': 'B0HPLFXQZ7'}
BOARD = "Escape games et calendriers de l'Avent"
KW = {
 'liste': "calendrier de l'avent enfant, escape game enfant, calendrier de l'avent livre, énigmes enfant 8 ans, activité noël enfant",
 'horloger': "calendrier de l'avent adulte, escape game livre adulte, calendrier de l'avent original, énigmes adulte, idée cadeau noël",
 'kerdaniel': "escape game livre adulte, jeu d'énigmes adulte, cadeau noël original, enquête à résoudre, casse-tête adulte",
 'dame': "escape game livre adulte, enquête policière jeu, jeu d'énigmes adulte, cadeau noël original, livre énigmes",
}
TAG = {'liste': " #calendrierdelavent #escapegame #noel", 'horloger': " #calendrierdelavent #escapegame #noel",
       'kerdaniel': " #escapegame #enigmes #ideecadeau", 'dame': " #escapegame #enigmes #ideecadeau"}

T = {
'liste': [
 ("Calendrier de l'Avent escape game pour enfant de 8 à 12 ans", "Le Père Noël a perdu sa liste ! Chaque jour de décembre, ton enfant résout une énigme avec Pistache le lutin pour sauver Noël. 24 énigmes, coups de pouce et solutions inclus."),
 ("Calendrier de l'Avent original pour enfant : un livre d'énigmes", "Un calendrier de l'Avent sans chocolat et sans écran : 24 énigmes à résoudre du 1er au 24 décembre. Labyrinthes, codes secrets, morse, sudoku 4x4. Dès 8 ans."),
 ("Idée de calendrier de l'Avent pour un enfant de 8 ans", "Une énigme par soir jusqu'à Noël pour retrouver la liste perdue du Père Noël. Une histoire tendre et drôle, un carnet d'enquête et un diplôme de super détective à la fin."),
 ("Calendrier de l'Avent pour enfant de 10 ans : escape game de Noël", "Ton enfant devient l'assistant détective d'un lutin malin. 24 énigmes qui montent doucement en difficulté, pour patienter jusqu'à Noël en s'amusant."),
 ("Activité de Noël sans écran pour les enfants : 24 énigmes", "Chaque soir de décembre, une nouvelle énigme rapproche les petits enquêteurs de la liste du Père Noël. Un crayon suffit. Solutions à la fin du livre."),
 ("Escape game de Noël pour enfants à faire à la maison", "Le 1er décembre, la liste des enfants sages disparaît du pôle Nord. Ton enfant mène l'enquête jour après jour, jusqu'au dénouement du 24 décembre."),
 ("Calendrier de l'Avent livre pour enfant : jeux et énigmes", "Mots mêlés, devinettes, calculs, coloriage magique, codes secrets : 24 jeux différents pour un calendrier de l'Avent pas comme les autres. De 8 à 12 ans."),
 ("Cadeau pour patienter jusqu'à Noël : un calendrier d'énigmes", "À offrir avant le 1er décembre : un calendrier de l'Avent en forme d'escape game pour les enfants de 8 à 12 ans. Grand format, 68 pages, solutions incluses."),
 ("Calendrier de l'Avent pour garçon ou fille de 9 ans", "Une enquête de Noël à suivre chaque soir avec Pistache le lutin. 24 énigmes adaptées aux enfants, des coups de pouce et un diplôme à remplir à la fin."),
 ("Calendrier de l'Avent intelligent : 24 énigmes pour les enfants", "Un calendrier qui fait réfléchir : logique, lecture, calcul et observation, une énigme par jour jusqu'à Noël. À faire seul ou avec un adulte."),
 ("Jeu de Noël pour enfant : retrouver la liste du Père Noël", "Sans sa liste, le Père Noël ne peut pas livrer les cadeaux ! 24 énigmes pour aider Pistache à retrouver la liste et démasquer le coupable."),
 ("Calendrier de l'Avent fait maison ? Celui-ci est prêt à jouer", "Pas besoin de préparer 24 surprises : ce livre propose une énigme par jour, une histoire à suivre et toutes les solutions. Dès 8 ans."),
 ("Escape game enfant 8 ans : une enquête au pôle Nord", "Un petit lutin, une liste disparue et 24 énigmes à résoudre jusqu'au réveillon. L'activité calme des soirs de décembre."),
 ("Calendrier de l'Avent qui n'est pas en chocolat", "Pour changer des chocolats : un calendrier de l'Avent en livre, avec une énigme de Noël par jour. Grand format, coups de pouce et solutions inclus."),
 ("Il n'est pas trop tard pour un calendrier de l'Avent", "Commencé le 1er ou en cours de route, ce calendrier d'énigmes se rattrape facilement : deux énigmes un soir, et l'enquête continue jusqu'au 24 décembre."),
 ("Calendrier de l'Avent de dernière minute pour enfant", "Disponible tout de suite sur Amazon : 24 énigmes de Noël pour les 8 à 12 ans, une histoire à suivre et un diplôme de super détective."),
 ("Livre d'énigmes de Noël pour les enfants de 8 à 12 ans", "Labyrinthe, morse, sudoku, devinettes : 24 énigmes pour sauver Noël avec Pistache le lutin. Une idée cadeau qui occupe tout le mois de décembre."),
],
'horloger': [
 ("Calendrier de l'Avent escape game pour adultes", "24 jours, 24 énigmes, une seule vérité. L'horloger d'un village alsacien a disparu avec la clé d'or. Chaque jour de décembre, une énigme vous rapproche du coupable."),
 ("Calendrier de l'Avent original pour adulte : un livre d'énigmes", "Pour changer des chocolats : un calendrier de l'Avent en forme d'escape game. Codes secrets, sudoku, grilles de logique, chiffre de César, morse. Dès 14 ans."),
 ("Idée cadeau de Noël : calendrier de l'Avent pour adulte", "Une enquête à suivre du 1er au 24 décembre dans un village d'Alsace, avec ses suspects et ses fausses pistes. 24 énigmes, indices et solutions inclus."),
 ("Calendrier de l'Avent pour couple : escape game à deux", "Chaque soir de décembre, une énigme à résoudre ensemble pour retrouver la clé d'or de l'Horloge des Étoiles. Un crayon suffit, aucun matériel."),
 ("Calendrier de l'Avent pour amateurs d'énigmes et de casse-têtes", "Nonogramme, labyrinthe, grilles de logique, mots mêlés : 24 énigmes toutes différentes, en 4 niveaux de difficulté, d'Apprenti à Grand maître."),
 ("Escape game de Noël en livre pour adultes", "Vous êtes l'apprenti de l'horloger disparu. Chaque jour, un indice, une énigme, un suspect de moins. Dénouement le 24 décembre."),
 ("Calendrier de l'Avent en famille : une enquête de Noël", "À jouer seul, en couple ou en famille dès 14 ans : 24 énigmes de Noël et une véritable histoire à suivre. Grand format, 70 pages."),
 ("Cadeau de Noël original pour un adulte qui aime les énigmes", "Un calendrier de l'Avent qui fait travailler les méninges : 24 énigmes, un carnet d'enquête, deux indices par jour et des solutions détaillées."),
 ("Calendrier de l'Avent pour ado de 14 ans et plus", "Une enquête de Noël en Alsace, avec des énigmes qui montent en difficulté jour après jour. Pour les ados comme pour les parents."),
 ("Calendrier de l'Avent sans chocolat pour adulte", "Vingt-quatre énigmes pour attendre Noël autrement. Codes, logique, observation : retrouvez la clé d'or avant minuit le 24 décembre."),
 ("Calendrier de l'Avent pour mamie ou papy qui aime les jeux", "Mots mêlés, sudoku, codes secrets et une histoire à suivre : un calendrier de l'Avent en livre, à faire seul ou avec les petits-enfants."),
 ("Jeu d'enquête de Noël : retrouvez la clé d'or de l'horloger", "Le 1er décembre, l'horloger Anselme disparaît. Sans sa clé, l'Horloge des Étoiles restera muette le soir de Noël. À vous de mener l'enquête."),
 ("Calendrier de l'Avent intelligent pour adulte : 24 énigmes", "Une difficulté progressive en 4 niveaux : les dernières énigmes résistent même aux joueurs aguerris. Indices progressifs et solutions détaillées."),
 ("Calendrier de l'Avent livre pour adulte, à offrir fin novembre", "Le cadeau à glisser avant le 1er décembre : un escape game de Noël en 24 jours, grand format 21,6 x 27,9 cm."),
 ("Pas trop tard pour un calendrier de l'Avent escape game", "Vous avez manqué le 1er décembre ? Rattrapez deux énigmes par soir et l'enquête continue jusqu'au 24. Indices et solutions inclus."),
 ("Calendrier de l'Avent de dernière minute pour adulte", "24 énigmes de Noël et une enquête en Alsace. Idéal pour un cadeau de dernière minute, disponible sur Amazon."),
 ("Livre d'énigmes de Noël pour adultes : l'Horloger de Noël", "Codes secrets, morse, chiffre de César, nonogramme : 24 énigmes pour retrouver la clé d'or avant minuit. Dès 14 ans."),
],
'kerdaniel': [
 ("Escape game en livre pour adultes : le manoir breton", "Votre oncle vous lègue son manoir, à condition de trouver son testament avant minuit. 19 énigmes, une pièce après l'autre. Indices et solutions inclus."),
 ("Idée cadeau de Noël pour un adulte qui aime les énigmes", "Braille, rayons laser et miroirs, KenKen, Kakuro, code binaire : 19 énigmes toutes différentes pour une enquête cosy en Bretagne."),
 ("Jeu d'énigmes pour adulte à faire chez soi", "Un soir de tempête dans le Finistère, un manoir, dix-neuf pièces et un testament caché. Un crayon suffit pour jouer."),
 ("Escape game à jouer en couple : le Testament du Manoir", "Une enquête à mener à deux, pièce par pièce, avant que la maison ne soit vendue à minuit. 4 niveaux de difficulté, de l'Invité au Maître des lieux."),
 ("Cadeau original pour les fans d'escape game", "Pour ceux qui adorent les escape rooms : un escape game en livre, 19 énigmes inédites et une grille finale pour révéler la cachette du testament."),
 ("Livre de casse-têtes pour adulte : une vraie enquête", "Des personnages, des fausses pistes et un coupable à démasquer. Chaque énigme a été vérifiée pour n'avoir qu'une seule solution."),
 ("Escape game en famille dès 14 ans : le manoir Kerdaniel", "À jouer seul, en couple ou en famille pendant les vacances de Noël. Grand format, 58 pages, deux indices progressifs par énigme."),
 ("Activité pour les soirées d'hiver : un escape game en livre", "Un manoir breton, une tempête et un inventeur un peu fou. 19 énigmes pour passer une soirée d'enquête au coin du feu."),
 ("Cadeau de Noël pour un papa qui aime les énigmes", "Kakuro, cavalier d'échecs, grille tournante, carré latin : un escape game en livre qui résiste même aux joueurs aguerris."),
 ("Escape game livre adulte : trouvez le testament avant minuit", "Chaque pièce cache une énigme, chaque énigme mène à la suivante. Et quelqu'un dans la maison fait tout pour vous devancer."),
 ("Jeu de logique pour adulte : 19 énigmes inédites", "Une enquête cosy en Bretagne, à résoudre crayon en main. Carnet d'enquête, indices progressifs et solutions détaillées."),
 ("Idée cadeau pour un ado de 15 ans qui aime réfléchir", "Un escape game en livre, sans écran : 19 énigmes de logique et d'observation pour retrouver un testament caché."),
 ("Escape game en livre à offrir à Noël", "Un cadeau qui se joue : l'héritage d'un oncle inventeur, un manoir breton et 19 énigmes avant minuit. Disponible sur Amazon."),
 ("Escape game pour les vacances de Noël en famille", "Pendant les vacances, une enquête à mener ensemble dans un manoir du Finistère. Dès 14 ans, solutions incluses."),
 ("Livre d'énigmes pour adulte : le Testament du Manoir Kerdaniel", "Braille, laser, binaire, échecs : un escape game breton plein de surprises. Grand format 21,6 x 27,9 cm."),
 ("Cadeau de dernière minute : un escape game en livre", "Disponible tout de suite sur Amazon : 19 énigmes et une enquête cosy pour les amateurs de casse-têtes."),
],
'dame': [
 ("Escape game en livre pour adultes : le tableau volé", "Paris, 6 heures du matin : la Dame au Lys a disparu du musée. Vous avez jusqu'à l'aube pour la retrouver. 21 énigmes, indices et solutions inclus."),
 ("Enquête policière à résoudre soi-même : un escape game", "Un chef-d'œuvre volé, des suspects qui mentent et un départ par le port du Havre à 4 heures. 21 énigmes pour démasquer le coupable."),
 ("Idée cadeau de Noël pour un fan d'enquêtes et d'énigmes", "Chiffre de Vigenère, carré de Playfair, Mastermind, futoshiki : 21 énigmes toutes différentes dans une vraie enquête d'art."),
 ("Escape game à deux : retrouvez la Dame au Lys", "À jouer en couple ou entre amis : chaque heure apporte un nouvel indice et une nouvelle énigme. 4 niveaux, de Stagiaire à Légende."),
 ("Livre jeu d'enquête pour adulte : vol au musée", "Vous êtes l'expert appelé par la police. Clavier codé, téléphone à touches, nonogramme : résolvez chaque énigme pour suivre la piste du tableau."),
 ("Cadeau original pour un amateur d'art et de mystères", "Un escape game en livre autour d'un vol de tableau à Paris. Une vraie enquête avec ses mensonges et ses fausses pistes."),
 ("Jeu d'énigmes pour adulte sans écran", "Un crayon, un carnet d'enquête et 21 énigmes pour retrouver un chef-d'œuvre volé avant l'aube. Grand format, 64 pages."),
 ("Escape game livre : 21 énigmes pour une nuit d'enquête", "De Paris au port du Havre, une course contre la montre pour retrouver la Dame au Lys. Deux indices progressifs par énigme."),
 ("Cadeau de Noël pour un ado qui aime les codes secrets", "Vigenère, Playfair, morse et Mastermind : un escape game en livre dès 14 ans, avec une enquête à suivre jusqu'au dénouement."),
 ("Escape game pour adulte : vol au musée Saint-Aubin", "Il ne reste qu'un cadre doré, vide. À vous de retrouver le tableau et le voleur avant 4 heures du matin. Solutions détaillées incluses."),
 ("Livre d'énigmes et de logique pour adulte", "Gratte-ciel, futoshiki, labyrinthe : 21 énigmes inédites, chacune vérifiée pour n'avoir qu'une seule solution."),
 ("Soirée enquête entre amis : un escape game en livre", "Une énigme par heure, une vraie intrigue et une grille finale pour révéler la cachette du tableau. Pour jouer à plusieurs dès 14 ans."),
 ("Escape game en livre à offrir à Noël : la Dame au Lys", "Un cadeau qui se joue : une enquête d'art parisienne et 21 énigmes. Disponible sur Amazon."),
 ("Cadeau de dernière minute pour un fan d'escape game", "Disponible tout de suite sur Amazon : un tableau volé, 21 énigmes et une nuit pour le retrouver. Indices et solutions inclus."),
 ("Enquête à résoudre pendant les vacances de Noël", "Pendant les vacances, une nuit d'enquête entre Paris et Le Havre pour retrouver un chef-d'œuvre volé. Dès 14 ans."),
],
}

def slots():
    out = []
    start = datetime.date(2026, 11, 20)
    # Calendriers de l'Avent : 1 par jour du 20/11 au 06/12 (17 jours)
    for i in range(17):
        d = start + datetime.timedelta(days=i)
        out.append(('liste', d, '08:00:00'))     # 9 h Paris
        out.append(('horloger', d, '14:00:00'))  # 15 h Paris
    # Escape games : un jour sur deux chacun, à 21 h Paris, du 20/11 au 20/12
    for i in range(31):
        d = start + datetime.timedelta(days=i)
        out.append(('kerdaniel' if i % 2 == 0 else 'dame', d, '20:00:00'))
    return out

rows = []; used = {k: 0 for k in T}
for book, d, h in sorted(slots(), key=lambda x: (x[1], x[2])):
    n = used[book]; used[book] += 1
    title, desc = T[book][n]
    rows.append({'Title': title, 'Media URL': f"https://m.media-amazon.com/images/I/{IMG[book]}._SL1000_.jpg?v={n+1}",
                 'Pinterest board': BOARD, 'Thumbnail': '', 'Description': desc + TAG[book],
                 'Link': f"https://www.amazon.fr/dp/{ASIN[book]}?pin={book}-{n+1:02d}",
                 'Publish date': f"{d}T{h}", 'Keywords': KW[book]})
assert all(used[k] <= len(T[k]) for k in T), used
for k in ('Title', 'Media URL', 'Link'):
    assert len({r[k] for r in rows}) == len(rows), k
assert all(len(r['Title']) <= 100 and len(r['Description']) <= 500 for r in rows)
with open('Import_Pinterest_Escape_Games.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), used)
