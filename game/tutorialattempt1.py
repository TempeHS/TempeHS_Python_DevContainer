import os
import pygame as pg 

if not pg.font:
    print("fonts disabled")
if not pg.mixer:
    print("sounds disabled")


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound

#for the sake of not messing up the tutorial i made a cursor sprite
#will figure out how to actually do the click interactions after i finish
class mouse(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("mouse.png", -1)
        self.fist_offset = (-235, -80)
        self.punching = False

    def update(self):
        pos = pg.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(self.fist_offset)
        if self.punching:
            self.rect.move_ip(15, 25)

    def punch(self, target):
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        self.punching = False

#they lobotomised youareanidiot :[
class smiley(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("you-are-an-idiot.png", -1, 4)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 90
        self.move = 18
        self.dizzy = False

    def update(self):
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, True, False)
        self.rect = newpos


    def _spin(self):
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = False
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        if not self.dizzy:
            self.dizzy = True
            self.original = self.image

#initialise pygame
pg.init()
print("test 1")
#set screen size
screen = pg.display.set_mode((1280, 480), pg.SCALED)
print("test 2")
pg.display.set_caption("test game")
print("test 3")
pg.mouse.set_visible(True)
print("test 4")

background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((170,238,17))
print("test 5")

if pg.font:
    font = pg.font.Font(None, 64)
    text = font.render("game", True, (10,10,10))
    textpos = text.get_rect(centerx=background.get_width()/2, y=10)
    background.blit(text, textpos)
0
screen.blit(background, (0,0))
pg.display.flip()
print("test 6")

mouse = mouse()
smiley = smiley()
allsprites = pg.sprite.RenderClear((mouse, smiley))
print("test 7")
clock = pg.time.Clock()
print("test7.5")

clock.tick(60)
for event in pg.event.get():
    if event.type == pg.QUIT:
        going = False
        print("uit")
    elif event.type == pg.KEYDOWN and event.key == pg.ESCAPE:
        going = False
        print("quite")
    elif event.type == pg.MOUSEBUTTONDOWN:
        if mouse.punch(smiley):
            smiley.punched
            print("test9 ")
    elif event.type == pg.MOUSEBUTTONUP:
        mouse.unpunch
        print("test 10")
    allsprites.update()

screen.blit(background, (0, 0))
allsprites.draw(screen)
pg.display.flip()
print("test 8")
pg.quit()