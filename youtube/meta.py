"""Titres, descriptions et dates de programmation des 36 Shorts (un par jour à 18 h, Paris)."""
import json, datetime as D
from heures import M, I

ORDER = ['22h22', '12h12', '21h12', '10h10', '00h00', '15h51', '14h14', '20h20', '17h17', '01h10', '23h23', '12h21',
         '18h18', '05h50', '21h21', '02h20', '19h19', '13h31', '16h16', '03h30', '15h15', '20h02', '13h13', '04h40',
         '01h01', '14h41', '02h02', '10h01', '03h03', '23h32', '04h04', '05h05', '06h06', '07h07', '08h08', '09h09']
TITLES = ["{h} : que veut vous dire l'univers ?", "Vous voyez souvent {h} ? Voici sa signification", "{h} : le message caché de cette heure",
          "Pourquoi vous voyez {h} ?", "{h} : ce que votre ange essaie de vous dire"]

def meta():
    out = []; start = D.date(2026, 11, 21)
    for i, h in enumerate(ORDER):
        kind = 'miroir' if h in M else 'inversee'
        if kind == 'miroir':
            ange, t2, i2, pa, l4, t4, i4, num, tarot = M[h]
            body = f"{t2} {i2} Ange associé : {ange}. {pa}\n\nEn amour : {t4} {i4}\nNumérologie : {num}." + (f" Écho du tarot : {tarot}." if tarot else '')
            tag = 'heuremiroir'
        else:
            ange, t2, i2, pa, t4, i4 = I[h]
            body = f"{t2} {i2} Ange associé : {ange}. {pa}\n\nLe message : {t4} {i4}"
            tag = 'heureinversee'
        page = f"https://oracle-arcana.fr/heure-{'miroir' if kind == 'miroir' else 'inversee'}-{h}.html"
        title = TITLES[i % len(TITLES)].format(h=h) + f" #{tag} #{h} #spiritualité"
        desc = (f"{body}\n\nLa signification complète de {h} : {page}\nHoroscope quotidien gratuit et toutes les heures miroirs : https://oracle-arcana.fr\n\n"
                f"Dites-nous en commentaire quelle heure vous voyez le plus souvent.\n\n#{tag} #{h} #spiritualité #ange #numérologie #oraclearcana")
        f = f"Short_heure_{'miroir' if kind == 'miroir' else 'inversee'}_{h}.mp4"
        out.append({"h": h, "file": f, "title": title, "desc": desc, "date": (start + D.timedelta(days=i)).isoformat(), "time": "18:00"})
    return out

if __name__ == '__main__':
    m = meta(); assert len(set(x['h'] for x in m)) == 36 and set(x['h'] for x in m) == (set(M) - {'11h11'}) | set(I)
    assert all(len(x['title']) <= 100 for x in m), [x['title'] for x in m if len(x['title']) > 100]
    json.dump(m, open('meta.json', 'w'), ensure_ascii=False, indent=1); print(m[0]['title']); print(m[0]['desc']); print(m[-1]['date'])
