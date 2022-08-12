import pygame
import os

# IMAGENS
ESCALA_MENOR = (24, 24)
ESCALA_MAIOR = (48, 48)

DIGITOS = []
for t in range(10):
    DIGITOS.append(pygame.transform.scale(pygame.image.load(os.path.join('imgs', f'dig_0{t}.PNG')), ESCALA_MENOR))

NUMEROS = [0]
for t in range(1, 9):
    NUMEROS.append(pygame.transform.scale(pygame.image.load(os.path.join('imgs', f'num_0{t}.PNG')), ESCALA_MENOR))

CAMPO_LIMPO       = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'campo_limpo.PNG')), ESCALA_MENOR)
CAMPO_OCULTO      = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'campo_oculto.PNG')), ESCALA_MENOR)
DUVIDA            = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'duvida.PNG')), ESCALA_MENOR)
BANDEIRA          = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bandeira.PNG')), ESCALA_MENOR)
BOMBA             = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bomba.PNG')), ESCALA_MENOR)
BOMBA_EXPLOSAO    = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bomba_explosao.PNG')), ESCALA_MENOR)
BOMBA_ERRADA      = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bomba_errada.PNG')), ESCALA_MENOR)
BOTAO_DEFAULT     = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'botao_default.PNG')), ESCALA_MAIOR)
BOTAO_DERROTA     = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'botao_derrota.PNG')), ESCALA_MAIOR)
BOTAO_PRESSIONADO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'botao_pressionado.PNG')), ESCALA_MAIOR)
BOTAO_VITORIA     = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'botao_vitoria.PNG')), ESCALA_MAIOR)
BOTAO_SUSTO       = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'botao_susto.PNG')), ESCALA_MAIOR)

# BOTOES MOUSE
ESQUERDO = 1
DIREITO = 3

# TELA
MARGEM_SUPERIOR = 50

# CORES
GREY = (192, 192, 192)
