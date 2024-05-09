import pygame as pg
import sys, random

fare_pozisyonu = [(640,300),(640,300)]
class UzayAraci(pg.sprite.Sprite):
    def __init__(self,yol,yol_hasarli,yol_sag,yol_sol,x_poz,y_poz):
        super().__init__()
        self.orijinal = pg.image.load(yol)
        self.image = pg.image.load(yol)
        self.sag = pg.image.load(yol_sag)
        self.sol = pg.image.load(yol_sol)
        self.rect = self.image.get_rect(center = (x_poz,y_poz))
        self.can = pg.image.load("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\can.png")
        self.can_sayisi = 5
        self.hasarli = pg.image.load(yol_hasarli)

    def update(self):
        # rect bizim istediğimiz bir nesnenin konumunu veren şey.
        self.rect.center = pg.mouse.get_pos()
        self.ekran_limiti()
        self.can_goster()
        self.az_can()
        self.manevra()

    def ekran_limiti(self):
        if self.rect.right >= 1400:
            self.rect.right = 1400
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 750:
            self.rect.bottom = 750

    def can_goster(self):
        for index,kalan_can in enumerate(range(self.can_sayisi)):
            ekran.blit(self.can, (1400-50*(index+1),15))

    def hasar(self,hasar_miktari):
        self.can_sayisi -= hasar_miktari

    def az_can(self):
        if self.can_sayisi < 2:
            self.image = self.hasarli
        else:
            self.image = self.orijinal

    def manevra(self):
        a = pg.mouse.get_pos()
        fare_pozisyonu.append(a)
        if len(fare_pozisyonu) == 4:
            fare_pozisyonu.pop(0)
        # En son yaptığım hareketin x konumu bir önceki yaptığım hareketin x konumundan büyükse sağa gidiyorumdur.
        if fare_pozisyonu[1][0] > fare_pozisyonu[0][0]:
            self.image = self.sag
        if fare_pozisyonu[1][0] < fare_pozisyonu[0][0]:
            self.image = self.sol
        if fare_pozisyonu[1][0] == fare_pozisyonu[0][0]:
            self.image = self.orijinal

class Meteor(pg.sprite.Sprite):
    def __init__(self,yol,x_poz,y_poz,x_hiz,y_hiz):
        super().__init__()
        self.image = pg.image.load(yol)
        self.rect = self.image.get_rect(center = (x_poz,y_poz))
        self.x_hizi = x_hiz
        self.y_hizi = y_hiz

    def update(self):
        self.rect.centerx += self.x_hizi
        self.rect.centery += self.y_hizi
        if self.rect.centery >= 750:
            self.kill()

class Lazer(pg.sprite.Sprite):
    def __init__(self,yol,pozisyon,hiz):
        super().__init__()
        self.image = pg.image.load(yol)
        self.rect = self.image.get_rect(center=(pozisyon))
        self.hiz = hiz

    def update(self):
        self.rect.centery -= self.hiz
        if self.rect.centery <= -50:
            self.kill()

class Lazer2(pg.sprite.Sprite):
    def __init__(self,yol,pozisyon,hiz):
        super().__init__()
        self.image = pg.image.load(yol)
        self.rect = self.image.get_rect(center=(pozisyon))
        self.hiz = hiz

    def update(self):
        self.rect.centery -= self.hiz
        if self.rect.centery <= -50:
            self.kill()

class LazerSag(pg.sprite.Sprite):
    def __init__(self,yol,pozisyon,hiz):
        super().__init__()
        self.image = pg.image.load(yol)
        self.rect = self.image.get_rect(center=(pozisyon))
        self.hiz = hiz
        self.hiz2 = hiz/2

    def update(self):
        self.rect.centery -= self.hiz
        self.rect.centerx += self.hiz2
        if self.rect.centery <= -50:
            self.kill()


class LazerSol(pg.sprite.Sprite):
    def __init__(self,yol,pozisyon,hiz):
        super().__init__()
        self.image = pg.image.load(yol)
        self.rect = self.image.get_rect(center=(pozisyon))
        self.hiz = hiz
        self.hiz2 = hiz/2

    def update(self):
        self.rect.centery -= self.hiz
        self.rect.centerx -= self.hiz2
        if self.rect.centery <= -50:
            self.kill()


def ana_oyun():
    global skor
    skor += 1
    uzayGemisiGrubu.update()
    uzayGemisiGrubu.draw(ekran)
    # .draw() fonksiyonu uzayGemisi sprite'ından self.image ve self.rect değişkenlerini alıyor. O yüzden bu iki değişkeni Sprite'ın içine özellikle tanımlamamız çok önemli.
    meteorGrubu.update()
    meteorGrubu.draw(ekran)

    for LAZER in lazerGrubuKirmizi:
        for METEOR in meteorGrubu:
            pg.sprite.spritecollide(METEOR,lazerGrubuKirmizi,True)
            pg.sprite.spritecollide(LAZER,meteorGrubu,True)

    
    for LAZER2 in lazerGrubuYesil:
        pg.sprite.spritecollide(LAZER2,meteorGrubu,True)


    if pg.sprite.spritecollide(uzayGemisiGrubu.sprite ,meteorGrubu,True):
        uzayGemisiGrubu.sprite.hasar(1)

    lazerGrubuKirmizi.update()
    lazerGrubuKirmizi.draw(ekran)
    lazerGrubuYesil.update()
    lazerGrubuYesil.draw(ekran)

def oyun_bitti():
    yazi_yuzeyi = oyun_fontu.render("Oyun Bitti !",True,(255,0,0))
    yazi_yuzeyi2 = oyun_fontu.render(f'Skorunuz: {skor}',True,(255,255,255))
    yazi_dortgeni = yazi_yuzeyi.get_rect(center = (700,340))
    yazi_dortgeni2 = yazi_yuzeyi2.get_rect(center = (700,400))
    ekran.blit(yazi_yuzeyi,yazi_dortgeni)
    ekran.blit(yazi_yuzeyi2,yazi_dortgeni2)


pg.init()
skor = 0
pg.mouse.set_visible(False)  # mousenin imlecini yok eder.
ekran = pg.display.set_mode((1400,750))
zaman = pg.time.Clock()
oyun_fontu = pg.font.Font(None,100)

uzayGemisi = UzayAraci("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\araç_düz.png","C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\araç_hasarlı.png","C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\araç_sağ.png","C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\araç_sol.png",700,500)
uzayGemisiGrubu = pg.sprite.GroupSingle()
uzayGemisiGrubu.add(uzayGemisi)

meteorGrubu = pg.sprite.Group()

lazerGrubuKirmizi = pg.sprite.Group()
lazerGrubuYesil = pg.sprite.Group()


METEOR_OLAYI = pg.USEREVENT  # Bize bağlı olmayan bir userevent
pg.time.set_timer(METEOR_OLAYI,500)

METEOR_OLAYI2 = pg.USEREVENT + 1
pg.time.set_timer(METEOR_OLAYI2,360)

METEOR_OLAYI3 = pg.USEREVENT + 2 
pg.time.set_timer(METEOR_OLAYI3,270)

METEOR_OLAYI4 = pg.USEREVENT + 3
pg.time.set_timer(METEOR_OLAYI4,180)

METEOR_OLAYI5 = pg.USEREVENT + 4
pg.time.set_timer(METEOR_OLAYI5,50)

arkaplan = pg.image.load("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\arkaplan.png")

SOL = 1
ORTA = 2
SAG = 3

lazer_zamani1 = 0
lazer_zamani2 = 0
lazer_zamani3 = 0

while True:
    gercek_zaman = pg.time.get_ticks()

    for olay in pg.event.get():
        if olay.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if gercek_zaman >= 0 and gercek_zaman < 20000:
            if olay.type == METEOR_OLAYI:
                meteorYolu = random.choice(("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorBüyük.png","C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorKüçük.png"))
                rastgele_x_poz = random.randint(100,1000)
                rastgele_y_poz = random.randint(-100,0)
                rastgele_x_hizi = random.randint(-1,1)
                rastgele_y_hizi = random.randint(4,10)
                yaratilmis_meteor = Meteor(meteorYolu,rastgele_x_poz,rastgele_y_poz,rastgele_x_hizi,rastgele_y_hizi)
                meteorGrubu.add(yaratilmis_meteor)

        if gercek_zaman >= 20000 and gercek_zaman < 40000:
            if olay.type == METEOR_OLAYI2:
                meteorYolu = random.choice(("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorBüyük.png","C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorKüçük.png"))
                rastgele_x_poz = random.randint(100,1000)
                rastgele_y_poz = random.randint(-100,0)
                rastgele_x_hizi = random.randint(-1,1)
                rastgele_y_hizi = random.randint(4,10)
                yaratilmis_meteor = Meteor(meteorYolu,rastgele_x_poz,rastgele_y_poz,rastgele_x_hizi,rastgele_y_hizi)
                meteorGrubu.add(yaratilmis_meteor)

        if gercek_zaman >= 40000 and gercek_zaman < 60000:
            if olay.type == METEOR_OLAYI3:
                meteorYolu = random.choice(("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorBüyük.png","C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorKüçük.png"))
                rastgele_x_poz = random.randint(100,1000)
                rastgele_y_poz = random.randint(-100,0)
                rastgele_x_hizi = random.randint(-1,1)
                rastgele_y_hizi = random.randint(4,10)
                yaratilmis_meteor = Meteor(meteorYolu,rastgele_x_poz,rastgele_y_poz,rastgele_x_hizi,rastgele_y_hizi)
                meteorGrubu.add(yaratilmis_meteor)

        if gercek_zaman >= 60000 and gercek_zaman < 80000:
            if olay.type == METEOR_OLAYI4:
                meteorYolu = random.choice(("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorBüyük.png","C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorKüçük.png"))
                rastgele_x_poz = random.randint(100,1000)
                rastgele_y_poz = random.randint(-100,0)
                rastgele_x_hizi = random.randint(-1,1)
                rastgele_y_hizi = random.randint(4,10)
                yaratilmis_meteor = Meteor(meteorYolu,rastgele_x_poz,rastgele_y_poz,rastgele_x_hizi,rastgele_y_hizi)
                meteorGrubu.add(yaratilmis_meteor)

        if gercek_zaman >= 80000:
            if olay.type == METEOR_OLAYI5:
                meteorYolu = random.choice(("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorBüyük.png","C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\meteorKüçük.png"))
                rastgele_x_poz = random.randint(100,1000)
                rastgele_y_poz = random.randint(-100,0)
                rastgele_x_hizi = random.randint(-1,1)
                rastgele_y_hizi = random.randint(4,10)
                yaratilmis_meteor = Meteor(meteorYolu,rastgele_x_poz,rastgele_y_poz,rastgele_x_hizi,rastgele_y_hizi)
                meteorGrubu.add(yaratilmis_meteor)

        if gercek_zaman - lazer_zamani1 > 750:
            if olay.type == pg.MOUSEBUTTONDOWN and olay.button == SOL:
                lazer_zamani1 = pg.time.get_ticks()
                yeni_lazer = Lazer("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\lazer_kırmızı.png",olay.pos,10)
                lazerGrubuKirmizi.add(yeni_lazer)
        
        if gercek_zaman - lazer_zamani2 > 1000:
            if olay.type == pg.MOUSEBUTTONDOWN and olay.button == SAG:
                lazer_zamani2 = pg.time.get_ticks()
                yeni_lazer = Lazer2("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\laser_yeşil.png",olay.pos,7)
                lazerGrubuYesil.add(yeni_lazer)

        if gercek_zaman - lazer_zamani3 > 1250:
            if olay.type == pg.MOUSEBUTTONDOWN and olay.button == ORTA:
                lazer_zamani3 = pg.time.get_ticks()
                yeni_lazer = Lazer("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\lazer_kırmızı.png",olay.pos,10)
                yeni_lazer2 = LazerSag("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\lazer_kırmızı.png",olay.pos,10)
                yeni_lazer3 = LazerSol("C:\\Users\\Melike\\Desktop\\Pygame ile 2 Boyutlu Oyun ve Algoritma Geliştirmeye Giriş\\Proje#2\\lazer_kırmızı.png",olay.pos,10)
                lazerGrubuKirmizi.add(yeni_lazer)
                lazerGrubuKirmizi.add(yeni_lazer2)
                lazerGrubuKirmizi.add(yeni_lazer3)

        if olay.type == pg.MOUSEBUTTONDOWN and uzayGemisiGrubu.sprite.can_sayisi == 0:
            uzayGemisiGrubu.sprite.can_sayisi = 5
            meteorGrubu.empty()
            skor = 0

    ekran.blit(arkaplan,(0,0))

    if uzayGemisiGrubu.sprite.can_sayisi > 0:
        ana_oyun()

    else :
        oyun_bitti()
        
    # ekran.fill((255,255,0))
    pg.display.update()
    zaman.tick(120) # While döngüsü saniyede 120 kere dönüyor.

    # Lazer ve meteor birbirine dokunursa ikisi de kaybolsun.
    # Uzay aracına meteor dokunursa can azalsın.


