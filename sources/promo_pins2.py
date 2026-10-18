"""Série 2 d'épingles Pinterest (1000x1500) pour les 2 livres de coloriage de Noël."""
from PIL import Image, ImageDraw
from promo_common import *
from promo_static import bg, framed, split, kids_pair, mockup
from promo_pins import (W, H, NAVY, RED, YEL, COV_A, COV_K, save, corner_book, footer,
                        pin_split, pin_grid, pin_book)


def pin_howto(key, name):
    color, cov = (NAVY, COV_A) if key == 'a' else (RED, COV_K)
    im = bg(W, H, color, hash(name) % 100); d = ImageDraw.Draw(im)
    if key == 'a':
        title, sub = 'Comment ça marche ?', 'le coloriage mystère en 3 étapes'
        steps = ['Chaque zone porte\nun numéro', 'Chaque numéro\n= une couleur', 'Le dessin de Noël\napparaît !']
        sol, num, _, _ = mosaic_assets('29_cloches')
        crop = lambda i: i.crop((i.width // 6, i.height // 6, i.width * 5 // 6, i.height * 5 // 6))
        imgs = [crop(num), crop(split(num, sol)), crop(sol)]
    else:
        title, sub = 'Comment ça marche ?', 'facile dès 6 ans'
        steps = ['Je lis le numéro\nde la case', 'Je prends\nla bonne couleur', "L'image cachée\napparaît !"]
        a, c = kids_pair('11_pingouin')
        imgs = [a, split(a, c), c]
    text_center(d, W, 50, title, font(FONT_B, 70), 'white')
    text_center(d, W, 150, sub, font(FONT_I, 42), YEL)
    y = 240
    for i, (s, img) in enumerate(zip(steps, imgs), 1):
        f = framed(img, 330); im.paste(f, (60, y))
        d.ellipse((440, y + 40, 520, y + 120), fill=YEL)
        text_center(d, 960, y + 52, str(i), font(FONT_B, 50), (20, 20, 40))
        d.multiline_text((550, y + 60), s, font=font(FONT_7, 44), fill='white', spacing=8)
        y += f.height + 30
    corner_book(im, cov, 300)
    return save(im, name)


if __name__ == '__main__':
    A1 = ['25_marche', '31_buche', '35_casse_noisette', '38_ecureuil', '40_foret', '26_lanterne', '29_cloches', '37_patins', '27_etoile_filante']
    A2 = ['23_hibou', '24_renard', '18_cadeaux', '08_couronne', '07_bougie', '30_gui', '31_buche', '25_marche', '38_ecureuil']
    K1 = ['11_pingouin', '34_train', '23_hibou', '24_renard', '18_cadeaux', '17_lutin', '25_marche', '29_cloches', '38_ecureuil']
    K2 = ['31_buche', '26_lanterne', '37_patins', '40_foret', '28_ange', '35_casse_noisette', '30_gui', '21_moufles', '22_bonnet']
    K3 = ['07_bougie', '08_couronne', '09_chaussettes', '10_boule', '13_village', '14_chalet', '19_biscuits', '20_sucres_orge', '27_etoile_filante']
    made = [
        pin_split('a', '25_marche', 'Le marché de Noël\nà colorier', 'coloriage mystère pour adultes', 'A09_marche'),
        pin_split('k', '11_pingouin', 'Le pingouin\nde Noël', 'case après case, il apparaît !', 'K09_pingouin'),
        pin_split('a', '31_buche', 'La bûche de Noël\nse révèle', 'zone après zone, sous vos crayons', 'A10_buche'),
        pin_split('k', '34_train', 'Le train\nde Noël', 'coloriage par numéros dès 6 ans', 'K10_train'),
        pin_howto('a', 'A11_comment'),
        pin_howto('k', 'K11_comment'),
        pin_split('a', '35_casse_noisette', 'Casse-noisette\nà colorier', 'un numéro, une couleur', 'A12_casse_noisette'),
        pin_split('k', '23_hibou', 'La chouette\nde Noël', 'une image cachée dans chaque page', 'K12_chouette'),
        pin_grid('a', A1, 'Coloriage zen\npour l\'hiver', '40 dessins de Noël à révéler', 'A13_zen_hiver'),
        pin_grid('k', K1, 'Calendrier de l\'Avent\nà colorier', 'un coloriage magique par jour', 'K13_avent'),
        pin_book('a', 'Cadeau pour une amie\nqui aime colorier', 'le livre anti-stress de Noël', ['40 coloriages mystères', 'Solutions incluses', 'Grand format 21,6 x 27,9 cm'], 'A14_cadeau_amie'),
        pin_book('k', 'Cadeau pour enfant\nde 6 à 10 ans', 'le cahier magique de Noël', ['40 images à découvrir', 'Grandes cases faciles', 'Solutions à la fin'], 'K14_cadeau_enfant'),
        pin_split('a', '38_ecureuil', "L'écureuil\nsous la neige", 'coloriage par numéros adulte', 'A15_ecureuil'),
        pin_split('k', '24_renard', 'Le renard\ndans la neige', 'coloriage magique de Noël', 'K15_renard'),
        pin_split('a', '40_foret', 'La forêt\nenneigée', 'un moment de calme à colorier', 'A16_foret'),
        pin_split('k', '18_cadeaux', 'Les cadeaux\nsous le sapin', 'case après case, la surprise !', 'K16_cadeaux'),
        pin_grid('a', A2, 'Calendrier de l\'Avent\npour adultes', 'un coloriage mystère par jour', 'A17_avent'),
        pin_grid('k', K2, 'Occuper les enfants\nà Noël', 'sans écran, au calme', 'K17_vacances'),
        pin_split('a', '26_lanterne', 'La lanterne\nde Noël', 'se révèle numéro après numéro', 'A18_lanterne'),
        pin_split('k', '17_lutin', 'Le lutin\nde Noël', 'à découvrir en coloriant', 'K18_lutin'),
        pin_book('a', 'Le cadeau parfait\npour mamie', 'coloriages mystères de Noël cosy', ['Un dessin par page', 'Verso blanc, pas de transfert', 'Solutions incluses'], 'A19_mamie'),
        pin_grid('k', K3, 'Coloriage de Noël\npour 7 ans', '40 images magiques à révéler', 'K19_7_ans'),
        pin_split('a', '29_cloches', 'Les cloches\nde Noël', 'coloriage anti-stress adulte', 'A20_cloches'),
        pin_book('k', 'Le cahier des\nvacances de Noël', 'à glisser dans la hotte', ['40 coloriages magiques', 'Dès 6 ans', 'Chiffres faciles de 1 à 12'], 'K20_cahier'),
    ]
    print(made)
