"""Livret adultes : Coloriages mystères - Noël cosy (mosaïque)."""
import glob, json, os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import mosaic
from mosaic import PAL, W, H, M, GW_IN, GH_IN
pdfmetrics.registerFont(TTFont('FrIt', 'FrauncesIt.ttf'))

TITLE = 'Coloriages mystères'
SUB = 'Noël cosy'
TAG = '40 coloriages par numéros pour adultes'
BRAND = 'Studio Impulsion'
motifs = sorted(os.path.basename(f)[:-4] for f in glob.glob('mosa/*.svg'))
NAMES = {'01_chocolat': 'Chocolat chaud', '02_maison': "Maison en pain d'épice", '03_sapin': 'Le sapin du salon',
 '04_bonhomme': 'Bonhomme de neige', '05_renne': 'Le petit renne', '06_chat_bonnet': 'Chat de Noël', '07_bougie': 'La bougie',
 '08_couronne': "Couronne de l'Avent", '09_chaussettes': 'Les chaussettes', '10_boule': 'Boule de Noël', '11_pingouin': 'Le pingouin',
 '12_ourson': 'Ourson en pull', '13_village': 'Village sous la neige', '14_chalet': 'Le chalet', '15_traineau': 'Le traîneau',
 '16_pere_noel': 'Père Noël', '17_lutin': 'Le lutin', '18_cadeaux': 'Les cadeaux', '19_biscuits': 'Biscuits de Noël',
 '20_sucres_orge': "Sucres d'orge", '21_moufles': 'Les moufles', '22_bonnet': 'Bonnet tricoté', '23_hibou': 'Le hibou',
 '24_renard': 'Le renard', '25_marche': 'Marché de Noël', '26_lanterne': 'La lanterne', '27_etoile_filante': 'Étoile filante',
 '28_ange': 'Le petit ange', '29_cloches': 'Les cloches', '30_gui': 'Le gui', '31_buche': 'La bûche', '32_lecture': 'Lecture au coin du feu',
 '33_fenetre_chat': 'Chat à la fenêtre', '34_train': 'Le petit train', '35_casse_noisette': 'Casse-noisette', '36_boule_neige': 'Boule à neige',
 '37_patins': 'Les patins', '38_ecureuil': "L'écureuil", '39_guirlandes': 'Maison illuminée', '40_foret': 'Forêt enneigée'}

def centered(cv, txt, font, size, y, gray=0.1):
    cv.setFont(font, size); cv.setFillGray(gray); cv.drawCentredString(W / 2, y, txt)

def title_page(cv):
    centered(cv, BRAND.upper(), 'Arc7', 10, H - 1.4 * inch, 0.35)
    centered(cv, TITLE, 'ArcB', 34, H - 3.6 * inch)
    centered(cv, SUB, 'ArcB', 46, H - 4.4 * inch, 0.25)
    centered(cv, TAG, 'FrIt', 17, H - 5.2 * inch, 0.2)
    cv.showPage()

def copyright_page(cv):
    cv.setFont('Arc5', 9); cv.setFillGray(0.25)
    y = 2.6 * inch
    for line in [f'{TITLE} - {SUB}', f'© 2026 {BRAND}. Tous droits réservés.',
                 'Toute reproduction, même partielle, est interdite sans autorisation écrite de l\'éditeur.',
                 'Les pages peuvent être photocopiées pour un usage strictement personnel et familial.',
                 'Les illustrations ont été conçues avec l\'aide d\'outils numériques et d\'intelligence artificielle.',
                 'Première édition : novembre 2026.']:
        cv.drawString(M, y, line); y -= 0.24 * inch
    cv.showPage()

def howto_page(cv):
    centered(cv, 'Comment ça marche ?', 'ArcB', 24, H - 1.4 * inch)
    cv.setFont('Arc5', 12.5); cv.setFillGray(0.15)
    lines = ['1. Chaque zone porte un numéro.', '2. Chaque numéro correspond à une couleur, indiquée sous le dessin.',
             '3. Coloriez toutes les zones du même numéro, puis passez au suivant.',
             '4. Petit à petit, l\'image de Noël apparaît.', '',
             'Les zones sans numéro restent blanches (neige, glaçage, flocons...).',
             'Crayons de couleur ou feutres à pointe fine conviennent parfaitement.',
             'Chaque dessin est imprimé sur une seule face : glissez une feuille',
             'cartonnée sous la page si vos feutres sont très encreurs.', '',
             'Les solutions se trouvent à la fin du livre, si vous voulez tricher un peu.']
    y = H - 2.3 * inch
    for l in lines:
        cv.drawString(1.0 * inch, y, l); y -= 0.32 * inch
    # cadre "ce livre appartient à"
    cv.setStrokeGray(0.3); cv.setLineWidth(1.2)
    cv.roundRect(1.0 * inch, 1.3 * inch, W - 2.0 * inch, 1.5 * inch, 14)
    centered(cv, 'Ce livre appartient à', 'FrIt', 16, 2.35 * inch, 0.2)
    cv.line(2.0 * inch, 1.7 * inch, W - 2.0 * inch, 1.7 * inch)
    cv.showPage()

def swatch_page(cv):
    centered(cv, 'Testez vos couleurs', 'ArcB', 24, H - 1.4 * inch)
    centered(cv, 'Coloriez chaque case avec le crayon ou le feutre que vous utiliserez.', 'Arc5', 11, H - 1.8 * inch, 0.3)
    bw, bh = 2.0 * inch, 1.3 * inch
    x0 = (W - 3 * bw - 2 * 0.3 * inch) / 2
    for i in range(12):
        n = i + 1; c, r = i % 3, i // 3
        x = x0 + c * (bw + 0.3 * inch); y = H - 2.4 * inch - (r + 1) * (bh + 0.45 * inch)
        cv.setStrokeGray(0.3); cv.setLineWidth(1); cv.roundRect(x, y, bw, bh, 10)
        cv.setFont('Arc7', 12); cv.setFillGray(0.15)
        cv.drawCentredString(x + bw / 2, y - 0.25 * inch, f'{n}  {PAL[n][0]}')
    cv.showPage()

def coloring_page(cv, b, num):
    mk = json.load(open(f'cache/{b}.json'))
    gw, gh = GW_IN * inch, GH_IN * inch
    gx, gy = M, H - 1.0 * inch - gh
    cv.drawImage(f'cache/{b}_edge.png', gx, gy, gw, gh)
    cv.setLineWidth(1.2); cv.setStrokeGray(0.25); cv.rect(gx, gy, gw, gh)
    cv.setFont('Arc7', 11); cv.setFillGray(0.15); cv.drawString(M, H - 0.68 * inch, f'N° {num}')
    cv.setFont('Arc5', 9); cv.setFillGray(0.45)
    cv.drawRightString(W - M, H - 0.68 * inch, "Coloriez chaque zone selon son numéro")
    sc = inch / 300
    for x, y, r, col in mk:
        if col == 0: continue
        fs = max(4.4, min(8.0, r * sc * 1.25))
        cv.setFont('Arc5', fs); cv.setFillGray(0.3)
        cv.drawCentredString(gx + x * sc, gy + gh - y * sc - fs * 0.36, str(col))
    used = sorted({m[3] for m in mk if m[3]})
    ly = gy - 0.36 * inch
    cv.setFont('Arc7', 10.5); cv.setFillGray(0.15); cv.drawString(M, ly, 'Couleurs :')
    x = M + 0.9 * inch
    for n in used:
        lab = f'{n} = {PAL[n][0]}'; w = pdfmetrics.stringWidth(lab, 'Arc5', 10.5)
        if x + w > W - M: ly -= 0.25 * inch; x = M + 0.9 * inch
        cv.setFont('Arc5', 10.5); cv.drawString(x, ly, lab); x += w + 0.24 * inch
    cv.setFont('Arc5', 9); cv.setFillGray(0.45); cv.drawString(M, ly - 0.28 * inch, 'Zone sans numéro = laisser blanc.')
    cv.showPage()

def solutions(cv):
    per = 9
    for p in range(0, len(motifs), per):
        if p == 0: centered(cv, 'Les solutions', 'ArcB', 22, H - 0.95 * inch)
        tw = 2.1 * inch; th = tw * 320 / 300
        for i, b in enumerate(motifs[p:p + per]):
            c, r = i % 3, i // 3
            x = (W - 3 * tw - 0.6 * inch) / 2 + c * (tw + 0.3 * inch); y = H - 1.25 * inch - (r + 1) * (th + 0.4 * inch)
            g = Image.open(f'cache/{b}_sol.png').convert('L')
            tmp = f'cache/{b}_solg.png'; g.save(tmp)
            cv.drawImage(tmp, x, y, tw, th)
            cv.setFont('Arc7', 9); cv.setFillGray(0.2)
            cv.drawString(x, y - 0.17 * inch, f'N° {motifs.index(b) + 1}  {NAMES.get(b, "")}')
        cv.showPage()

def build(out):
    cv = canvas.Canvas(out, pagesize=(W, H))
    cv.setTitle(f'{TITLE} - {SUB}'); cv.setAuthor(BRAND)
    title_page(cv); copyright_page(cv); howto_page(cv); swatch_page(cv)
    for i, b in enumerate(motifs, 1):
        coloring_page(cv, b, i)
        cv.showPage()  # verso blanc
    solutions(cv)
    centered(cv, "Merci d'avoir colorié avec nous !", 'ArcB', 24, H / 2 + 0.6 * inch)
    centered(cv, 'Si ce livre vous a plu, un avis sur Amazon nous aide beaucoup.', 'Arc5', 12, H / 2, 0.3)
    cv.showPage()
    cv.save()

if __name__ == '__main__':
    build('Noel_cosy_adultes_interieur.pdf')
