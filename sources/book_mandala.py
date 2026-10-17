"""Livret : Mandalas de Noël (40 mandalas à colorier pour ados et adultes)."""
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
for n, f in [('Arc5', 'Archivo-500.ttf'), ('Arc7', 'Archivo-700.ttf'), ('ArcB', 'ArchivoBlack.ttf'), ('FrIt', 'FrauncesIt.ttf')]:
    pdfmetrics.registerFont(TTFont(n, f))
W, H = 8.5 * inch, 11 * inch
M = 0.55 * inch
TITLE, SUB, TAG, BRAND = 'Mandalas', 'de Noël', '40 mandalas à colorier pour ados et adultes', 'Studio Impulsion'
SEEDS = list(range(40))

def centered(cv, t, f, s, y, g=0.1):
    cv.setFont(f, s); cv.setFillGray(g); cv.drawCentredString(W / 2, y, t)

def build(out):
    cv = canvas.Canvas(out, pagesize=(W, H)); cv.setTitle(f'{TITLE} {SUB}'); cv.setAuthor(BRAND)
    # 1. titre
    centered(cv, BRAND.upper(), 'Arc7', 10, H - 1.4 * inch, 0.35)
    centered(cv, TITLE, 'ArcB', 44, H - 3.6 * inch); centered(cv, SUB, 'ArcB', 44, H - 4.35 * inch, 0.25)
    centered(cv, TAG, 'FrIt', 18, H - 5.15 * inch, 0.2)
    cv.drawImage('mcache/m00.png', W / 2 - 1.6 * inch, 1.6 * inch, 3.2 * inch, 3.2 * inch)
    cv.showPage()
    # 2. copyright
    cv.setFont('Arc5', 9); cv.setFillGray(0.25); y = 2.6 * inch
    for l in [f'{TITLE} {SUB}', f'© 2026 {BRAND}. Tous droits réservés.',
              'Toute reproduction, même partielle, est interdite sans autorisation écrite de l\'éditeur.',
              'Les pages peuvent être photocopiées pour un usage strictement personnel et familial.',
              'Les illustrations ont été conçues avec l\'aide d\'outils numériques.', 'Première édition : novembre 2026.']:
        cv.drawString(M, y, l); y -= 0.24 * inch
    cv.showPage()
    # 3. mode d'emploi + appartient à
    centered(cv, 'Un moment pour soi', 'ArcB', 26, H - 1.4 * inch)
    cv.setFont('Arc5', 12.5); cv.setFillGray(0.15); y = H - 2.3 * inch
    for l in ['Installez-vous au calme, avec un thé ou un chocolat chaud.',
              'Commencez par le centre du mandala et avancez vers l\'extérieur,',
              'anneau après anneau : c\'est ce qui rend le coloriage si apaisant.', '',
              'Sapins, houx, cadeaux, cloches, étoiles : chaque mandala cache',
              'des motifs de Noël. À vous de choisir les couleurs.', '',
              'Chaque dessin est imprimé sur une seule face. Glissez une feuille',
              'cartonnée sous la page si vous utilisez des feutres.',
              'Crayons de couleur, feutres fins ou stylos gel conviennent très bien.']:
        cv.drawString(1.0 * inch, y, l); y -= 0.32 * inch
    cv.setStrokeGray(0.3); cv.setLineWidth(1.2); cv.roundRect(1.0 * inch, 1.3 * inch, W - 2.0 * inch, 1.5 * inch, 14)
    centered(cv, 'Ce livre appartient à', 'FrIt', 16, 2.35 * inch, 0.2); cv.line(2.0 * inch, 1.7 * inch, W - 2.0 * inch, 1.7 * inch)
    cv.showPage()
    # 4. test des couleurs
    centered(cv, 'Testez vos couleurs', 'ArcB', 24, H - 1.4 * inch)
    centered(cv, 'Essayez vos crayons ou feutres ici avant de commencer.', 'Arc5', 11, H - 1.8 * inch, 0.3)
    r = 0.62 * inch
    for i in range(20):
        c, rr = i % 4, i // 4
        cx = W / 2 + (c - 1.5) * 1.7 * inch; cy = H - 3.0 * inch - rr * 1.6 * inch
        cv.setStrokeGray(0.3); cv.setLineWidth(1); cv.circle(cx, cy, r)
    cv.showPage()
    # 5. mandalas
    D = 7.4 * inch
    for i, s in enumerate(SEEDS, 1):
        cv.setFont('Arc7', 11); cv.setFillGray(0.3); cv.drawString(M, H - 0.7 * inch, f'N° {i}')
        cv.drawImage(f'mcache/m{s:02d}.png', (W - D) / 2, (H - D) / 2 - 0.1 * inch, D, D)
        cv.showPage()
        cv.showPage()  # verso blanc
    centered(cv, "Merci d'avoir colorié avec nous !", 'ArcB', 24, H / 2 + 0.6 * inch)
    centered(cv, 'Si ce livre vous a plu, un avis sur Amazon nous aide beaucoup.', 'Arc5', 12, H / 2, 0.3)
    cv.showPage()
    cv.showPage()  # page finale blanche (nombre pair)
    cv.save()

if __name__ == '__main__':
    build('Mandalas_Noel_interieur.pdf')
