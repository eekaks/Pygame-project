import pygame
from random import randint, choice

class Hirvio:
    def __init__(self):
        self.kuva = pygame.image.load("hirvio.png")
        self.x = 400
        self.y = 150
        self.liike = choice([-2, 2])
        self.suunta = choice([1, 2])
    
    def liiku(self):
        if self.suunta == 1:
            self.liiku_x()
        elif self.suunta == 2:
            self.liiku_y()
    
    def liiku_x(self):
        if self.liike == 2:
            if self.x < 639-self.kuva.get_width():
                self.x += self.liike
            elif self.x >= 640-self.kuva.get_width():
                self.liike = -2
        if self.liike == -2:
            if self.x > 0:
                self.x += self.liike
            elif self.x <= 0:
                self.liike = 2

    def liiku_y(self):
        if self.liike == 2:
            if self.y < 479-self.kuva.get_height():
                self.y += self.liike
            elif self.y >= 480-self.kuva.get_height():
                self.liike = -2
        if self.liike == -2:
            if self.y > 0:
                self.y += self.liike
            elif self.y <= 0:
                self.liike = 2

class Robotti:
    def __init__(self):
        self.kuva = pygame.image.load("robo.png")
        self.x = 100
        self.y = 150
        self.oikealle = False
        self.vasemmalle = False
        self.ylos = False
        self.alas = False
        self.pisteet = 0
        
    def liiku(self):
        if self.oikealle:
            self.liiku_oikealle()
        if self.vasemmalle:
            self.liiku_vasemmalle()
        if self.ylos:
            self.liiku_ylos()
        if self.alas:
            self.liiku_alas()

    def liiku_oikealle(self):
        if self.x < 638-self.kuva.get_width():
            self.x += 4

    def liiku_vasemmalle(self):
        if self.x > 2:
            self.x -= 4

    def liiku_ylos(self):
        if self.y > 2:
            self.y -= 4

    def liiku_alas(self):
        if self.y < 478-self.kuva.get_height():
            self.y += 4

class Kolikko:
    def __init__(self):
        self.kuva = pygame.image.load("kolikko.png")
        self.x = randint(0, 640-self.kuva.get_width())
        self.y = randint(0, 480-self.kuva.get_height())

class KauhuHuone():
    def __init__(self):
        pygame.init()
        self.pelin_aloitus()
        self.aloitusruutu()
    
    def pelin_aloitus(self):
        self.naytto = pygame.display.set_mode((640, 480))
        self.kolikot = []
        self.hirviot = []
        self.hirvioiden_maara = 0
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.kello = pygame.time.Clock()
        self.pelaaja = Robotti()
        self.koska_viimeksi_kolikko = 0
        self.koska_viimeksi_suunnan_vaihto = 0
        self.vihollisen_pisteet = 0
        self.peli_kaynnissa = False

    def aloitusruutu(self):
        self.naytto.fill((35, 35, 35))
        alkuteksti1 = self.fontti.render(f"Kuinka monta hirviötä haluat? 1-9", True, (0, 255, 0))
        self.naytto.blit(alkuteksti1, (100, 210))
        alkuteksti2 = self.fontti.render(f"Varo hirviöitä ja kerää kolikoita!", True, (0, 255, 0))
        self.naytto.blit(alkuteksti2, (100, 250))

        pygame.display.flip()

        jatkuuko = True
        while jatkuuko:
            self.kello.tick(60)
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    jatkuuko = False
                    if tapahtuma.key == pygame.K_1:
                        self.hirvioiden_maara = 1
                    if tapahtuma.key == pygame.K_2:
                        self.hirvioiden_maara = 2
                    if tapahtuma.key == pygame.K_3:
                        self.hirvioiden_maara = 3
                    if tapahtuma.key == pygame.K_4:
                        self.hirvioiden_maara = 4
                    if tapahtuma.key == pygame.K_5:
                        self.hirvioiden_maara = 5
                    if tapahtuma.key == pygame.K_6:
                        self.hirvioiden_maara = 6
                    if tapahtuma.key == pygame.K_7:
                        self.hirvioiden_maara = 7
                    if tapahtuma.key == pygame.K_8:
                        self.hirvioiden_maara = 8
                    if tapahtuma.key == pygame.K_9:
                        self.hirvioiden_maara = 9

        for i in range(self.hirvioiden_maara):
            self.hirviot.append(Hirvio())      
        self.peli_kaynnissa = True
        self.silmukka()

    def silmukka(self):
        while self.peli_kaynnissa:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            self.edista_peli()
        self.peli_loppu()

    def piirra_naytto(self):
        pygame.display.set_caption(f"{' ':<85}{'Kauhuhuone'}")
        self.naytto.fill((35, 35, 35))
        self.naytto.blit(self.pelaaja.kuva, (self.pelaaja.x, self.pelaaja.y))

        for hirvio in self.hirviot:
            self.naytto.blit(hirvio.kuva, (hirvio.x, hirvio.y))

        teksti1 = self.fontti.render(f"Robotti: {self.pelaaja.pisteet}", True, (0, 255, 0))
        self.naytto.blit(teksti1, (50, 5))
        teksti2 = self.fontti.render(f"Hirviöt: {self.vihollisen_pisteet}", True, (225, 0, 0))
        self.naytto.blit(teksti2, (500, 5))

        for kolikko in self.kolikot:
            self.naytto.blit(kolikko.kuva, (kolikko.x, kolikko.y))    
        
        pygame.display.flip()

    def edista_peli(self):
        aika_nyt = pygame.time.get_ticks()

        if aika_nyt - self.koska_viimeksi_kolikko > 1000:
            self.koska_viimeksi_kolikko = aika_nyt
            self.kolikot.append(Kolikko())
        
        self.pelaaja.liiku()
        for hirvio in self.hirviot:
            hirvio.liiku()
    
        if aika_nyt - self.koska_viimeksi_suunnan_vaihto > 2000:
            self.koska_viimeksi_suunnan_vaihto = aika_nyt
            for hirvio in self.hirviot:
                hirvio.liike = choice([-2, 2])
                hirvio.suunta = choice([1, 2])

        self.kolikot = [kolikko for kolikko in self.kolikot if not self.tormays(kolikko, self.pelaaja)]

        for hirvio in self.hirviot:
            self.kolikot = [kolikko for kolikko in self.kolikot if not self.tormays(kolikko, hirvio)]

        for hirvio in self.hirviot:
            if self.tormays(self.pelaaja, hirvio):
                self.peli_kaynnissa = False

        self.kello.tick(60)

    def tutki_tapahtumat(self):
         for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.pelaaja.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.pelaaja.oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.pelaaja.ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.pelaaja.alas = True
                
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.pelaaja.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.pelaaja.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.pelaaja.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.pelaaja.alas = False
                
            if tapahtuma.type == pygame.QUIT:
                exit()

    def tormays(self, hahmo1, hahmo2):
        if hahmo1.x < hahmo2.x + hahmo2.kuva.get_width():
            if hahmo1.x + hahmo1.kuva.get_width() > hahmo2.x:
                if hahmo1.y < hahmo2.y + hahmo2.kuva.get_height():
                    if hahmo1.y + hahmo1.kuva.get_height() > hahmo2.y:
                        if isinstance(hahmo2, Robotti):
                            hahmo2.pisteet += 1
                        if isinstance(hahmo2, Hirvio):
                            if not isinstance(hahmo1, Robotti):
                                self.vihollisen_pisteet += 1
                        return True
        return False
    
    def peli_loppu(self):
        self.naytto.fill((35, 35, 35))
        lopputeksti1 = self.fontti.render(f"Robotti: {self.pelaaja.pisteet}", True, (0, 255, 0))
        self.naytto.blit(lopputeksti1, (50, 210))
        lopputeksti2 = self.fontti.render(f"Hirviöt: {self.vihollisen_pisteet}", True, (225, 0, 0))
        self.naytto.blit(lopputeksti2, (500, 210))
        lopputeksti3 = self.fontti.render(f"Paina Space pelataksesi uudestaan", True, (225, 0, 0))
        self.naytto.blit(lopputeksti3, (150, 300))

        pygame.display.flip()
        while True:
            self.kello.tick(60)
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_SPACE:
                        self.pelin_aloitus()
                        self.aloitusruutu()

KauhuHuone()