import pygame
import random
import sys

# 1. Inicialização do Pygame
pygame.init()

# 2. Configurações da Tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Coleta de Itens - Desafio Visível")

# 3. Definição de Cores (RGB)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 120, 255)       # Jogador
VERDE = (0, 255, 100)      # Item
VERMELHO = (255, 50, 50)   # Inimigos
AMARELO = (255, 255, 0)    # Texto de aviso

# 4. Configuração de Fontes e Relógio (FPS)
fonte_placar = pygame.font.SysFont(None, 40)
fonte_alerta = pygame.font.SysFont(None, 60)
relogio = pygame.time.Clock()

# 5. Variáveis de Tamanho
tamanho_jogador = 30
tamanho_item = 20
tamanho_inimigo = 30

def gerar_coordenadas(tamanho_objeto):
    """Gera coordenadas aleatórias garantindo que o objeto fique dentro da tela."""
    x = random.randint(0, LARGURA - tamanho_objeto)
    y = random.randint(0, ALTURA - tamanho_objeto)
    return x, y

def adicionar_inimigo():
    """Cria um novo inimigo em uma posição e com direções aleatórias."""
    x, y = gerar_coordenadas(tamanho_inimigo)
    # Define uma velocidade aleatória entre positiva ou negativa para x e y
    vx = random.choice([-5, -4, 4, 5])
    vy = random.choice([-5, -4, 4, 5])
    
    # Adicionamos as propriedades do inimigo como um dicionário na lista
    inimigos.append({"x": x, "y": y, "vx": vx, "vy": vy})

def resetar_jogo():
    """Reinicia todas as variáveis para começar ou recomeçar a partida."""
    global jogador_x, jogador_y, vel_jogador
    global item_x, item_y
    global pontuacao, fim_de_jogo, inimigos, tempo_aviso
    
    jogador_x = LARGURA // 2
    jogador_y = ALTURA // 2
    vel_jogador = 6
    
    item_x, item_y = gerar_coordenadas(tamanho_item)
    
    pontuacao = 0
    fim_de_jogo = False
    tempo_aviso = 0 # Temporizador para o texto de "Novo Inimigo!" sumir da tela
    
    # Esvazia a lista de inimigos e adiciona o primeiro
    inimigos = []
    adicionar_inimigo()

# Inicializa o jogo pela primeira vez
resetar_jogo()

# 6. Loop Principal do Jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill(PRETO)

    if not fim_de_jogo:
        # --- MOVIMENTAÇÃO DO JOGADOR ---
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jogador_x > 0:
            jogador_x -= vel_jogador
        if teclas[pygame.K_RIGHT] and jogador_x < LARGURA - tamanho_jogador:
            jogador_x += vel_jogador
        if teclas[pygame.K_UP] and jogador_y > 0:
            jogador_y -= vel_jogador
        if teclas[pygame.K_DOWN] and jogador_y < ALTURA - tamanho_jogador:
            jogador_y += vel_jogador

        rect_jogador = pygame.Rect(jogador_x, jogador_y, tamanho_jogador, tamanho_jogador)
        rect_item = pygame.Rect(item_x, item_y, tamanho_item, tamanho_item)

        # --- CHECAGEM DE COLETA DE ITEM ---
        if rect_jogador.colliderect(rect_item):
            pontuacao += 1
            item_x, item_y = gerar_coordenadas(tamanho_item)
            
            # Incremento Visível de Dificuldade!
            if pontuacao % 5 == 0:
                adicionar_inimigo()
                tempo_aviso = 90 # O aviso durará 90 frames (1,5 segundos a 60 FPS)

        # --- LÓGICA DE TODOS OS INIMIGOS ---
        for inimigo in inimigos:
            # Movimenta
            inimigo["x"] += inimigo["vx"]
            inimigo["y"] += inimigo["vy"]

            # Quica nas bordas
            if inimigo["x"] <= 0 or inimigo["x"] >= LARGURA - tamanho_inimigo:
                inimigo["vx"] *= -1
            if inimigo["y"] <= 0 or inimigo["y"] >= ALTURA - tamanho_inimigo:
                inimigo["vy"] *= -1

            # Checa colisão com o jogador
            rect_inimigo = pygame.Rect(inimigo["x"], inimigo["y"], tamanho_inimigo, tamanho_inimigo)
            pygame.draw.rect(tela, VERMELHO, rect_inimigo) # Desenha o inimigo

            if rect_jogador.colliderect(rect_inimigo):
                fim_de_jogo = True

        # --- DESENHO DE ITENS E TEXTOS ---
        pygame.draw.rect(tela, AZUL, rect_jogador)
        pygame.draw.rect(tela, VERDE, rect_item)

        # Placar
        texto_placar = fonte_placar.render(f"Pontuação: {pontuacao}", True, BRANCO)
        tela.blit(texto_placar, (10, 10))

        # Aviso Visual de Dificuldade
        if tempo_aviso > 0:
            texto_aviso = fonte_alerta.render("NOVO INIMIGO!", True, AMARELO)
            tela.blit(texto_aviso, (LARGURA//2 - texto_aviso.get_width()//2, 50))
            tempo_aviso -= 1 # Reduz o tempo até chegar a 0 e parar de desenhar

    else:
        # --- TELA DE GAME OVER ---
        texto_fim = fonte_alerta.render("FIM DE JOGO!", True, VERMELHO)
        texto_pontos = fonte_placar.render(f"Sua Pontuação: {pontuacao}", True, BRANCO)
        texto_reiniciar = fonte_placar.render("Pressione 'R' para reiniciar", True, VERDE)
        
        tela.blit(texto_fim, (LARGURA//2 - texto_fim.get_width()//2, ALTURA//2 - 50))
        tela.blit(texto_pontos, (LARGURA//2 - texto_pontos.get_width()//2, ALTURA//2))
        tela.blit(texto_reiniciar, (LARGURA//2 - texto_reiniciar.get_width()//2, ALTURA//2 + 50))

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_r]:
            resetar_jogo()

    # Atualiza a tela e define o FPS
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()