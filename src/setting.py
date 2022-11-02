import os
import sys
import random
import pygame
from pygame import *
from pygame import transform # 11/1 추가
from pygame.locals import RESIZABLE, RLEACCEL # 11/1 추가


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
gamername=''
scr_size = (width, height) = (800, 400)
FPS = 60
gravity = 0.65
font = pygame.font.Font('DungGeunMo.ttf', 32)
full_screen=False
monitor_size = (monitor_width, monitor_height) = (pygame.display.Info().current_w, pygame.display.Info().current_h)

black = (0,0,0)
white = (255,255,255)
background_col = (235,235,235)
green = (0,200,0)
orange = (255,127,0)
blue = (0,0,225)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_orange = (255,215,0)

large_font = pygame.font.Font('DungGeunMo.ttf', 75) # 11/1 추가 pvp에서 폰트입력

high_score = 0
resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)
screen = resized_screen.copy()
resized_screen_centerpos = (0,0)
rwidth = resized_screen.get_width()
rheight = resized_screen.get_height()
button_offset = 0.18

clock = pygame.time.Clock()
pygame.display.set_caption("Milk Dragon's Adventure by_MilkDragon")

bgm_on=True
on_pushtime=0
off_pushtime=0
jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')
#background_music = pygame.mixer.Sound('sprites/t-rex_bgm1.mp3')

# HERE: REMOVE SOUND!!
# pygame.mixer.music.load('sprites/t-rex_bgm1.mp3')


dino_size = [44, 47]
object_size = [40, 40]
ptera_size = [46, 40]
collision_immune_time = 500
shield_time = 2000
speed_up_limit_count = 700

# 게임 내에 text를 넣을때 쓰는 함수
def draw_text(text,font,surface,x,y,main_color) :
    text_obj = font.render(text,True,main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj,text_rect)

def text_objects(text, font):
    textSurface = font.render(text, True, (black))
    return textSurface, textSurface.get_rect()

# 투명한 이미지 불러오기 11/1 투석투주에서 추가
def alpha_image(name, sizex=-1, sizey=-1,color_key=None):
    full_name = os.path.join('sprites', name)
    img = pygame.image.load(full_name)
    if color_key is not None:
        if color_key == -1:
            color_key = img.get_at((0, 0))
        img.set_colorkey(color_key, RLEACCEL)
    if sizex != -1 or sizey != -1:
        img = transform.scale(img, (sizex, sizey))
    img.convert_alpha()
    return (img, img.get_rect())

# 게임 내 image를 넣을 때 쓰는 함수
def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    fullname = os.path.join('sprites', sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect

def disp_gameOver_msg(gameover_image):

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(gameover_image, gameover_rect)

def disp_intro_buttons(btn_gamestart, btn_board, btn_option):
    btn_gamestart_rect = btn_gamestart.get_rect()
    btn_board_rect = btn_board.get_rect()
    btn_option_rect = btn_option.get_rect()

    btn_gamestart_rect.centerx, btn_board_rect.centerx, btn_option_rect.centerx = width * 0.72, width * 0.72, width * 0.72
    btn_gamestart_rect.centery, btn_board_rect.centery, btn_option_rect.centery = height * 0.5, height * (0.5+button_offset), height * (0.5+2*button_offset)
    
    screen.blit(btn_gamestart, btn_gamestart_rect)
    screen.blit(btn_board, btn_board_rect)
    screen.blit(btn_option, btn_option_rect)

# pvp 사용함수 추가
def disp_pvp_gameover_buttons(btn_restart, btn_exit):
    btn_restart_rect = btn_restart.get_rect()
    btn_exit_rect = btn_exit.get_rect()
    btn_restart_rect.centerx = width * 0.35
    btn_exit_rect.centerx = width * 0.65
    btn_restart_rect.centery = height * 0.55
    btn_exit_rect.centery = height * 0.55
    screen.blit(btn_restart, btn_restart_rect)
    screen.blit(btn_exit, btn_exit_rect)

# pvp 사용함수 추가
def disp_pvp_winner_loser(player1):
    win = large_font.render("WIN", True, black)
    lose = large_font.render("LOSE", True, black)
    if not player1.is_dead:
        win_width = width * 0.17
        lose_width = width * 0.70
    else:
        win_width = width * 0.70
        lose_width = width * 0.17

    screen.blit(win, (win_width, height * 0.2))
    screen.blit(lose, (lose_width, height * 0.2))

# 표기법 수정 필요
def checkscrsize(eventw, eventh):
    if (eventw < width and eventh < height) or eventw < width or eventh < height: #최소해상도
        resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)
    else:
        if eventw/eventh!=width/height: #고정화면비
            adjusted_height=int(eventw/(width/height))
            resized_screen = pygame.display.set_mode((eventw,adjusted_height), RESIZABLE)

def full_screen_issue():
    global scr_size
    resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)
    resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)

def extractDigits(number):
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number%10)
            number = int(number/10)

        digits.append(number%10)
        for i in range(len(digits),5):
            digits.append(0)
        digits.reverse()
        return digits

def resize(name, w, h, color):
        global width, height, resized_screen
        print("resized_screen: (",resized_screen.get_width(),",",resized_screen.get_height(),")")
        return (name, w*resized_screen.get_width()//width, h*resized_screen.get_height()//height, color)

def textsize(size):
    font = pygame.font.Font('DungGeunMo.ttf', size)
    return font
