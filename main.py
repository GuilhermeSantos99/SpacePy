import pygame
import json
from random import randint

# Funções
def respawn():
    x = 1350
    y = randint(1, 640)
    return [x, y]

def respawn_missil():
    triggered = False
    respawn_missil_x = pos_player_x
    respawn_missil_y = pos_player_y
    vel_missil_x = 0
    return [respawn_missil_x, respawn_missil_y, triggered, vel_missil_x]

def colisions():
    global pontos
    if player_rect.colliderect(alien_rect) or alien_rect.x == 60:
        pontos -= 1
        return True
    elif missil_rect.colliderect(alien_rect):
        pontos += 1
        return True
    else:
        return False

def record_pontos():
    global pontos


pygame.init()

x = 1280
y = 720

# Geração de imagens
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("SpacePy")

# Imagem de fundo
bg = pygame.image.load('images/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

# Imagem nave
alien = pygame.image.load('images/spaceship.png').convert_alpha()
alien = pygame.transform.scale(alien, (50, 50))

# Imagem alien
playerImg = pygame.image.load('images/space.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerImg = pygame.transform.rotate(playerImg, -90)

# Imagem míssil
missil = pygame.image.load('images/missile.png').convert_alpha()
missil = pygame.transform.scale(missil, (25, 25))
missil = pygame.transform.rotate(missil, -45)

# Posicionamento de objetos na tela
pos_alien_x = 500
pos_alien_y = 300

pos_player_x = 200
pos_player_y = 300

vel_missil_x = 0
pos_missil_x = 200
pos_missil_y = 300

pontos = 1
triggered = False
rodando = True

# Carregamento de fonte
font = pygame.font.SysFont('font/FiraCode-VariableFont_wght.ttf', 50)

player_rect = playerImg.get_rect()
alien_rect = alien.get_rect()
missil_rect = missil.get_rect()

# Abrindo arquivo Json
file_json = open("record.json")
recordJson = json.load(file_json)

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    screen.blit(bg, (0, 0))

    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < 1280:
        screen.blit(bg, (rel_x, 0))

    # Comandos
    tecla = pygame.key.get_pressed()

     # Move para cima a nave
    if tecla[pygame.K_UP] and pos_player_y > 1:
        pos_player_y -= 1.5

        if not triggered:
            pos_missil_y -= 1.5

    # Move para baixo a nave
    if tecla[pygame.K_DOWN] and pos_player_y < 665:
        pos_player_y += 1.5

        if not triggered:
            pos_missil_y += 1.5

    # Move para a esquerda a nave
    if tecla[pygame.K_LEFT] and pos_player_x > 100:
        pos_player_x -= 1.5

        if not triggered:
            pos_missil_x -= 1.5

    # Move para a direita a nave
    if tecla[pygame.K_RIGHT] and pos_player_x < 400:
        pos_player_x += 1.5

        if not triggered:
            pos_missil_x += 1.5

    # Dispara a missil
    if tecla[pygame.K_SPACE]:
        triggered = True
        vel_missil_x = 100

    if pontos == -1:
        rodando = False

    # Regras

    if pos_alien_x == 50:
        pos_alien_x = respawn()[0]
        pos_alien_y = respawn()[1]

    if pos_missil_x == 1300:
        pos_missil_x, pos_missil_y, triggered, vel_missil_x = respawn_missil()

    if pos_alien_x == 50 or colisions():
        pos_alien_x = respawn()[0]
        pos_alien_y = respawn()[1]

    # Posição rect
    player_rect.y = pos_player_y
    player_rect.x = pos_player_x

    missil_rect.y = pos_missil_y
    missil_rect.x = pos_missil_x

    alien_rect.y = pos_alien_y
    alien_rect.x = pos_alien_x

    x -= 1

    pos_alien_x -= 2

    pos_missil_x += vel_missil_x

    pygame.draw.rect(screen, (255, 0, 0), player_rect, 4)
    pygame.draw.rect(screen, (255, 0, 0), missil_rect, 4)
    pygame.draw.rect(screen, (255, 0, 0), alien_rect, 4)

    # Mostra pontuação
    score = font.render(f' Pontos: {int(pontos)} ', True, (0, 0, 0))
    screen.blit(score, (50, 100))

    # Salva record
    recordPontos = recordJson["record"]

    if recordPontos < pontos:
        recordPontos = pontos

    else:
        pass

    # Monstra record
    record = font.render(f' Record: {str(recordPontos)} ', True, (0, 0, 0))
    screen.blit(record, (50, 50))

    # Criar imagens
    screen.blit(alien, (pos_alien_x, pos_alien_y))
    screen.blit(missil, (pos_missil_x, pos_missil_y))
    screen.blit(playerImg, (pos_player_x, pos_player_y))

    pygame.display.update()
    
# Salva record em arquivo Json
if pontos >= recordPontos:
    with open('record.json', 'w') as JsonRecord:
        pontosDict = {"record": pontos}
        json.dump(pontosDict, JsonRecord)
