from src.setting import *
from src.game_value import *


class Ground:
    def __init__(self, speed=-5, loc = DEFAULT_HEIGHT):
        self.image, self.rect = load_image('ground2.png', -1, -1, -1)
        self.image1, self.rect1 = load_image('ground2.png', -1, -1, -1)
        self.rect.top = int(loc*height)
        self.rect1.top = int(loc*height)
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image('cloud.png', int(90*30/42), 30, -1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Heart:
    def __init__(self, sizex=-1, sizey=-1, x=-1, y=-1, heart_color = 0):
        self.images, self.rect = load_sprite_sheet("heart_for_character.png", 2, 1, sizex, sizey, -1)
        self.image = self.images[heart_color]
        if x == -1:
            self.rect.left = width * 0.01
        else:
            self.rect.left = x

        if y == -1:
            self.rect.top = height * 0.02
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)

class HeartIndicator:
    def __init__(self, life, loc = -1):
        self.life = life
        if loc == -1:
            self.position_x = 0.01
            self.position_y = 0.02
            self.position_x2 = 0.065
            self.position_y2 = 0.02
            self.heart_color = 0
        elif loc == 2:
            self.position_x = 0.85
            self.position_y = 0.02
            self.position_x2 = 0.90
            self.position_y2 = 0.02
            self.heart_color = 1
        else:
            self.position_x = 0.01
            self.position_y = 0.54
            self.position_x2 = 0.065
            self.position_y2 = 0.54
            self.heart_color = 1

    def draw(self):
        self.life_set.draw()
        self.draw_heart_count()

    def update(self, life):
        self.life = life
        self.life_set = Heart(object_size[0], object_size[1], x = width * self.position_x, y = height * self.position_y, heart_color = self.heart_color)
        self.draw_heart_count()

    def draw_heart_count(self):
        life_count_text = font.render(f"x {self.life}", True, black)
        two_left_life_text = font.render(f"x {self.life}", True, black)
        one_left_life_text = font.render(f"x {self.life}", True, black)
        no_left_life_text = font.render(f"x {self.life}", True, black)
        if self.life == 2:
            screen.blit(two_left_life_text, (width * self.position_x2, height * self.position_y))
        elif self.life == 1:
            screen.blit(one_left_life_text, (width * self.position_x2, height * self.position_y))
        elif self.life == 0 :
            screen.blit(no_left_life_text, (width * self.position_x2, height * self.position_y))
        else:
            screen.blit(life_count_text, (width * self.position_x2, height * self.position_y))

class Potion:
    def __init__(self, sizex=-1, sizey=-1, x=-1, y=-1):
        self.images, self.rect = load_image("green_potion.png", sizex, sizey, -1)
        if x == -1:
            self.rect.left = width * 0.01
        else:
            self.rect.left = x

        if y == -1:
            self.rect.top = height * 0.02
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.images, self.rect)

class PotionIndicator:
    def __init__(self, count, loc = -1):
        self.count = count
        if loc == -1: # 2p
            self.position_x = 0.20
            self.position_y = 0.02
            self.position_x2 = 0.25
            self.position_y2 = 0.02
        else: # 1p
            self.position_x = 0.20
            self.position_y = 0.54
            self.position_x2 = 0.25
            self.position_y2 = 0.54

    def draw(self):
        self.count_set.draw()
        self.draw_potion_count()

    def update(self, count):
        self.count = count
        self.count_set = Potion(object_size[0], object_size[1], x = width * self.position_x, y = height * self.position_y)
        self.draw_potion_count()

    def draw_potion_count(self):
        potion_count_text = font.render(f"x {self.count}", True, black)
        screen.blit( potion_count_text, (width * self.position_x2, height * self.position_y))

class Scoreboard:

    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.pos_x = 0
        self.pos_y = 0
        self.my_font = pygame.font.Font('DungGeunMo.ttf', 30)
        if x == -1:
            self.pos_x = width * 0.89
        else:
            self.pos_x = x
        if y == -1:
            self.pos_y = height * 0.15
        else:
            self.pos_y = y

    def draw(self):
        screen.blit(self.sc, self.sc_rect)

    def update(self,score):
        score_digits = extract_digits(score)
        # self.image.fill(background_col)
        # for s in score_digits:
        #     self.image.blit(self.tempimages[s], self.temprect)
        #     self.temprect.left += self.temprect.width
        # self.temprect.left = 0
        self.sc = self.my_font.render(f'{score}'.zfill(5), True, black)
        self.sc_rect = self.sc.get_rect()
        self.sc_rect.left = self.pos_x
        self.sc_rect.top = self.pos_y

class ImgBack:
    def __init__(self, speed=-5, name='spring',type = -1):
        self.name = name
        if type == 1: #1p -> 아래
            self.image, self.rect = load_image(f'{self.name}.png', width, height/2)
            self.image1, self.rect1 = load_image(f'{self.name}.png', width, height/2)
            self.rect.bottom = height
            self.rect1.bottom = height
            self.rect1.left = self.rect.right
            # 화면 맞추기
            self.rect.bottom = height
            self.rect1.bottom = height
            self.rect.top = height/2
            self.rect1.top = height/2
            # image1 우측에 붙이기
            self.rect.left = 0
            self.rect1.left = self.rect.right
            self.speed = speed
        
        elif type == 2:
            self.image, self.rect = load_image(f'{self.name}.png', width, height/2)
            self.image1, self.rect1 = load_image(f'{self.name}.png', width, height/2)
            self.rect.bottom = height/2
            self.rect1.bottom = height/2
            self.rect1.left = self.rect.right
            # 화면 맞추기
            self.rect.bottom = height/2
            self.rect1.bottom = height/2
            self.rect.top = 0
            self.rect1.top = 0
            # image1 우측에 붙이기
            self.rect.left = 0
            self.rect1.left = self.rect.right
            self.speed = speed

        else:
            self.image, self.rect = load_image(f'{self.name}.png', width, height)
            self.image1, self.rect1 = load_image(f'{self.name}.png', width, height)
            self.rect.bottom = height
            self.rect1.bottom = height
            self.rect1.left = self.rect.right
            # 화면 맞추기
            self.rect.bottom = height
            self.rect1.bottom = height
            self.rect.top = 0
            self.rect1.top = 0
            # image1 우측에 붙이기
            self.rect.left = 0
            self.rect1.left = self.rect.right
            self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self,name='spring',type = -1):
        self.name = name
        if type == 1:
            self.image, self.rect = load_image(f'{self.name}.png', width, height/2)
            self.image1, self.rect1 = load_image(f'{self.name}.png', width, height/2)
            self.rect.bottom = height/2
            self.rect1.bottom = height/2
            self.rect1.left = self.rect.right
            # 화면 맞추기
            self.rect.bottom = height/2
            self.rect1.bottom = height/2
            self.rect.top = 0
            self.rect1.top = 0
            # image1 우측에 붙이기
            self.rect.left = 0
            self.rect1.left = self.rect.right
        elif type == 2:
            self.image, self.rect = load_image(f'{self.name}.png', width, height/2)
            self.image1, self.rect1 = load_image(f'{self.name}.png', width, height/2)
            self.rect.bottom = height
            self.rect1.bottom = height
            self.rect1.left = self.rect.right
            # 화면 맞추기
            self.rect.bottom = height
            self.rect1.bottom = height
            self.rect.top = height/2
            self.rect1.top = height/2
            # image1 우측에 붙이기
            self.rect.left = 0
            self.rect1.left = self.rect.right



        self.rect.left += self.speed
        self.rect1.left += self.speed
        if self.rect.right < width:
            self.rect1.left = self.rect.right
        if self.rect1.right < width:
            self.rect.left = self.rect1.right

class Mask_time:
    def __init__(self, x=-1, y=-1):
        self.pos_x = 0
        self.pos_y = 0
        if x == -1:
            self.pos_x = width * 0.63
        else:
            self.pos_x = x
        if y == -1:
            self.pos_y = height * 0.15
        else:
            self.pos_y = y
    def draw(self):
        screen.blit(self.sc, self.sc_rect)

    def update(self, hp):
        self.sc = font.render(f'Mask Time : {100-hp}'.zfill(2), True, black)
        self.sc_rect = self.sc.get_rect()
        self.sc_rect.left = self.pos_x
        self.sc_rect.top = self.pos_y

class Item_status:

    def __init__(self, x=-1, y=-1):
        self.pos_x = 0
        self.pos_y = 0
        if x == -1:
            self.pos_x = width * 0.3
        else:
            self.pos_x = x
        if y == -1:
            self.pos_y = height * 0.05
        else:
            self.pos_y = y
    def draw(self):
        screen.blit(self.sc, self.sc_rect)

    def update(self, cnt1, cnt2, cnt3, cnt4):
        self.sc = font.render(f' {cnt1}    {cnt2}    {cnt3}    {cnt4} '.zfill(1), True, black)
        self.sc_rect = self.sc.get_rect()
        self.sc_rect.left = self.pos_x
        self.sc_rect.top = self.pos_y