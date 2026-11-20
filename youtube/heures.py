"""Textes courts des 37 Shorts heures miroirs (source : pages oracle-arcana.fr). Génère un JSON par heure."""
import json, os, sys

# h: (ange, accroche scène 2 titre, scène 2 italique, phrase sous l'ange, label scène 4, titre scène 4, italique scène 4, numérologie titre, tarot)
M = {
 '00h00': ('Vehuhiah', "Une heure d'une puissance exceptionnelle.", "L'infini, le recommencement absolu.", "Vos pensées ont une force particulière.", 'EN AMOUR', "La fin d'un chapitre.", "Place à une histoire plus alignée.", "0, le nombre de l'infini", 'Le Mat'),
 '01h01': ('Jeliel', "Une nouvelle énergie entre dans votre vie.", "Des changements positifs approchent.", "Faites confiance à ce nouveau départ.", 'EN AMOUR', "Une rencontre portée par l'indépendance.", "Vous attirez en étant vous-même.", "1, le nombre des commencements", 'Le Bateleur'),
 '02h02': ('Sitael', "Elle parle de vos relations.", "Harmonie, partenariat, diplomatie.", "Cherchez l'équilibre à deux.", 'EN AMOUR', "Une des heures les plus favorables au couple.", "Un rapprochement s'annonce.", "2, le nombre du lien", 'La Papesse'),
 '03h03': ('Elemiah', "L'heure des artistes et des créateurs.", "Exprimez ce que vous ressentez.", "Votre créativité est soutenue.", 'EN AMOUR', "Le moment des déclarations sincères.", "Osez dire les choses autrement.", "3, le nombre de l'expression", "L'Impératrice"),
 '04h04': ('Mahasiah', "Elle parle de fondations et de stabilité.", "L'énergie du bâtisseur.", "Construisez pas à pas, solidement.", 'EN AMOUR', "Une relation qui se consolide.", "Un projet à deux prend racine.", "4, le nombre du bâtisseur", "L'Empereur"),
 '05h05': ('Lelahel', "Des changements importants arrivent.", "Liberté et aventure.", "Accueillez le mouvement sans peur.", 'EN AMOUR', "Le besoin de plus d'air.", "Ou la libération d'un lien qui freinait.", "5, le nombre de la liberté", 'Le Pape'),
 '06h06': ('Achaiah', "L'heure de l'amour et de la famille.", "La réconciliation est possible.", "La douceur revient dans votre foyer.", 'EN AMOUR', "Un lien qui s'approfondit.", "La tendresse est de retour.", "6, le nombre du cœur", "L'Amoureux"),
 '07h07': ('Cahethel', "Une des heures les plus spirituelles.", "Sagesse et intuition.", "Écoutez votre voix intérieure.", 'EN AMOUR', "Bien plus qu'un simple charme.", "Un véritable alignement d'âmes.", "7, le nombre de la sagesse", 'Le Chariot'),
 '08h08': ('Haziel', "L'heure de l'abondance.", "Le 8 couché, symbole de l'infini.", "La prospérité frappe à votre porte.", 'EN AMOUR', "Elle amplifie ce qui existe déjà.", "Ce qui est beau le devient encore plus.", "8, le nombre de l'abondance", 'La Justice'),
 '09h09': ('Aladiah', "La fin d'un cycle important.", "Humanisme et compassion.", "Laissez partir ce qui est terminé.", 'EN AMOUR', "Une page qui se tourne en douceur.", "Pour un amour plus juste.", "9, le nombre de l'accomplissement", "L'Hermite"),
 '10h10': ('Lauviah', "L'heure du potentiel infini.", "Vos pensées se matérialisent vite.", "Pensez à ce que vous voulez vraiment.", 'EN AMOUR', "Une heure faste pour l'amour naissant.", "Une rencontre pleine d'avenir.", "1, le nouveau départ", 'La Roue de Fortune'),
 '11h11': ('Hahaiah', "C'est l'heure miroir la plus puissante.", "Un portail entre vous et l'univers.", "Vos pensées ont une force décuplée.", 'EN AMOUR', "Le signe d'une connexion d'âme.", "Faites un vœu sincère pour votre cœur.", "11, le nombre maître de l'intuition", 'La Force'),
 '12h12': ('Iezalel', "L'harmonie et l'équilibre parfaits.", "Réconciliez vos contraires.", "Une voie harmonieuse s'ouvre à vous.", 'EN AMOUR', "Deux tempéraments qui s'accordent.", "Le couple trouve son équilibre.", "3, la création", 'Le Pendu'),
 '13h13': ('Mebahel', "Une heure de transformation profonde.", "Ne craignez pas ce changement.", "Ce qui se transforme vous libère.", 'EN AMOUR', "Un lien qui devient plus vrai.", "Place à l'authenticité.", "4, la stabilité retrouvée", "L'Arcane sans nom"),
 '14h14': ('Hariel', "Ancrez-vous dans le moment présent.", "Vérifiez vos bases.", "Ce qui est solide durera.", 'EN AMOUR', "Le moment de poser des bases.", "Un engagement clair, un projet commun.", "5, le mouvement", 'Tempérance'),
 '15h15': ('Hekamiah', "Épanouissement et liberté d'être soi.", "Soyez pleinement authentique.", "Vos anges soutiennent votre liberté.", 'EN AMOUR', "Une passion intense s'annonce.", "Laissez parler votre cœur.", "6, l'harmonie", 'Le Diable'),
 '16h16': ('Lauviah II', "L'heure de l'engagement sincère.", "L'amour responsable.", "Votre lien se renforce.", 'EN AMOUR', "L'envie de s'engager plus loin.", "Un couple qui se solidifie.", "7, la sagesse", 'La Maison Dieu'),
 '17h17': ('Caliel', "Protection, espoir et optimisme.", "L'énergie de l'Étoile.", "Dépassez vos propres limites.", 'EN AMOUR', "Elle redonne espoir.", "Une belle personne veille sur vous.", "8, l'abondance", "L'Étoile"),
 '18h18': ('Leuviah', "Une période d'abondance s'annonce.", "Sur tous les plans.", "Accueillez-la avec gratitude.", 'EN AMOUR', "Une belle rencontre approche.", "Ou une relation qui s'épanouit.", "9, l'accomplissement", 'La Lune'),
 '19h19': ('Pahaliah', "Un cycle se termine, un autre commence.", "Lumineux et plein de promesses.", "Faites confiance au processus.", 'EN AMOUR', "Favorable aux nouvelles rencontres.", "Et au couple qui s'épanouit.", "1, le renouveau", 'Le Soleil'),
 '20h20': ('Nelkhael', "Prenez du recul.", "Regardez votre vie avec lucidité.", "Vos décisions seront éclairées.", 'EN AMOUR', "La clarté sur vos sentiments.", "Le moment de voir juste.", "2, le choix", 'Le Jugement'),
 '21h21': ('Yeiayel', "L'univers est pleinement avec vous.", "Avancez avec confiance.", "Le succès se rapproche.", 'EN AMOUR', "L'heure du premier pas.", "Osez envoyer ce message.", "3, la réussite", 'Le Monde'),
 '22h22': ('Melahel', "Une heure très puissante.", "Pensez grand, construisez durable.", "Vos ambitions sont réalisables.", 'EN AMOUR', "Quelqu'un qui vous aime va se manifester.", "Un message, un appel, un geste.", "22, le nombre maître du bâtisseur", None),
 '23h23': ('Haheuiah', "Une transformation spirituelle profonde.", "Un nouveau vous émerge.", "Laissez cette évolution se faire.", 'EN AMOUR', "Quelqu'un a besoin de vous.", "Sans oser vous le dire.", "5, le changement", None),
}
# heures inversées : (ange, titre 2, italique 2, phrase ange, titre message, italique message)
I = {
 '01h10': ('Jeliel', "Un nouveau départ après une période difficile.", "Une lumière nouvelle entre dans votre vie.", "Vos efforts vont porter leurs fruits.", "La persévérance est récompensée.", "Continuez à avancer."),
 '02h20': ('Sitael', "L'heure inversée de la dualité.", "Elle parle de réciprocité.", "Rééquilibrez vos échanges.", "Donnez, mais recevez aussi.", "Vous méritez autant que vous offrez."),
 '03h30': ('Elemiah', "L'heure mystérieuse du milieu de la nuit.", "Celle des créateurs et des visionnaires.", "Une idée cherche à naître en vous.", "Notez ce qui vous vient.", "L'inspiration est là."),
 '04h40': ('Mahasiah', "L'âme travaille en profondeur.", "Loin du bruit du monde.", "Votre évolution continue en silence.", "Rien n'est immobile.", "Même dans l'obscurité, vous grandissez."),
 '05h50': ('Lelahel', "L'heure inversée du changement.", "Regardez la situation autrement.", "Ce qui semblait instable vous libère.", "La vraie liberté naît du changement.", "Même de celui que l'on redoutait."),
 '10h01': ('Achaiah', "Un miroir du temps.", "Il vous ramène à vos origines.", "Regardez d'où vous venez.", "Vos racines sont votre force.", "Elles éclairent la suite du chemin."),
 '12h21': ('Iezalel', "Une heure d'une grande harmonie.", "L'équilibre revient.", "Rééquilibrez les énergies de votre vie.", "Ce qui était bloqué circule à nouveau.", "Laissez la paix s'installer."),
 '13h31': ('Mebahel', "L'énergie transformatrice du 13.", "Amplifiée par le miroir.", "Acceptez le changement avec sérénité.", "Ce qui part laisse de la place.", "Pour ce qui vous ressemble vraiment."),
 '14h41': ('Hariel', "Elle parle de ce que vous construisez.", "Pour votre avenir.", "Les bases durables demandent du temps.", "Soyez patient avec vous-même.", "Chaque pierre compte."),
 '15h51': ('Hekamiah', "Une libération approche.", "Après une période d'épreuves.", "Vos efforts ont été vus et reconnus.", "Le poids s'allège.", "Respirez, le plus dur est derrière vous."),
 '20h02': ('Nelkhael', "Voir au-delà des apparences.", "Votre intuition s'aiguise.", "Regardez la situation sous un autre angle.", "La réponse est plus simple qu'elle n'y paraît.", "Faites confiance à ce que vous sentez."),
 '21h12': ('Yeiayel', "Réconciliez raison et intuition.", "Une décision vous attend.", "Écoutez votre tête et votre cœur.", "Les deux ont raison.", "Le bon choix les réunit."),
 '23h32': ('Haheuiah', "Un message de votre inconscient.", "Depuis la nuit profonde.", "Accordez-vous un moment de silence.", "Écoutez ce qui monte en vous.", "La réponse est déjà là."),
}

HOOKS = ["Vous la voyez souvent ?", "Ce n'est pas un hasard.", "L'univers vous parle.", "Elle revient sans cesse ?"]

def scenes(h, kind):
    hh = h.replace('h', ':')
    lab = 'HEURE MIROIR' if kind == 'miroir' else 'HEURE INVERSÉE'
    n = int(h[:2]) * 60 + int(h[3:])
    s = [{"dur": 4.5, "groups": [
        {"at": 0.2, "lines": [{"style": "label", "text": lab, "y": 560}]},
        {"at": 0.5, "lines": [{"style": "big", "text": hh, "y": 640, "size": 280}]},
        {"at": 1.8, "lines": [{"style": "italic", "text": HOOKS[n % 4], "y": 1010, "size": 84}]}]}]
    if kind == 'miroir':
        ange, t2, i2, pa, l4, t4, i4, num, tarot = M[h]
    else:
        ange, t2, i2, pa, t4, i4 = I[h]; l4 = 'LE MESSAGE'; num = tarot = None
    s.append({"dur": 5.0, "groups": [
        {"at": 0.2, "lines": [{"style": "title", "text": t2, "y": 580, "size": 92}]},
        {"at": 2.0, "lines": [{"style": "italic", "text": i2, "y": 950, "size": 84}]}]})
    s.append({"dur": 5.0, "groups": [
        {"at": 0.2, "lines": [{"style": "label", "text": "ANGE ASSOCIÉ", "y": 600}]},
        {"at": 0.4, "lines": [{"style": "big", "text": ange, "y": 670, "size": 170 if len(ange) <= 8 else 140}]},
        {"at": 2.0, "lines": [{"style": "title", "text": pa, "y": 960, "size": 84}]}]})
    s.append({"dur": 5.0, "groups": [
        {"at": 0.2, "lines": [{"style": "label", "text": l4, "y": 600}]},
        {"at": 0.4, "lines": [{"style": "title", "text": t4, "y": 680, "size": 96}]},
        {"at": 2.2, "lines": [{"style": "italic", "text": i4, "y": 960, "size": 80}]}]})
    if num:
        g = [{"at": 0.2, "lines": [{"style": "label", "text": "NUMÉROLOGIE", "y": 560 if tarot else 700}, {"style": "title", "text": num, "y": 630 if tarot else 770, "size": 84}]}]
        if tarot:
            g.append({"at": 2.0, "lines": [{"style": "label", "text": "ÉCHO DU TAROT", "y": 960}, {"style": "title", "text": tarot, "y": 1030, "size": 110}]})
        s.append({"dur": 5.0, "groups": g})
    s.append({"dur": 5.5, "logo": True, "groups": [
        {"at": 0.6, "lines": [{"style": "italic", "text": "Accueillez ce message.", "y": 720, "size": 80}]},
        {"at": 1.6, "lines": [{"style": "small", "text": "Signification complète sur", "y": 900, "size": 46}, {"style": "title", "text": "oracle-arcana.fr", "y": 960, "size": 96}]},
        {"at": 2.8, "lines": [{"style": "label", "text": "ABONNEZ-VOUS POUR VOTRE PROCHAIN SIGNE", "y": 1150}]}]})
    return s

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for h in M:
        if h == '11h11': continue
        json.dump({"name": f"Short_heure_miroir_{h}", "seed": int(h[:2]) * 60 + int(h[3:]), "scenes": scenes(h, 'miroir')}, open(f'{out}/{h}.json', 'w'), ensure_ascii=False)
    for h in I:
        json.dump({"name": f"Short_heure_inversee_{h}", "seed": int(h[:2]) * 60 + int(h[3:]), "scenes": scenes(h, 'inversee')}, open(f'{out}/{h}.json', 'w'), ensure_ascii=False)
    print(len(os.listdir(out)))
