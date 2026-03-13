import pygame
import random
import sys

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA = 600
ALTURA = 600
TAMANHO_BLOCO = 20

# Cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (40, 40, 40)

# Cria tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Cobrinha 🐍")

# Controle de FPS
clock = pygame.time.Clock()
FPS = 10

# Fonte
fonte = pygame.font.SysFont("Arial", 30)


def desenhar_texto(texto, cor, x, y):
    render = fonte.render(texto, True, cor)
    tela.blit(render, (x, y))


def gerar_comida():
    x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    return x, y


def desenhar_grade():
    for x in range(0, LARGURA, TAMANHO_BLOCO):
        pygame.draw.line(tela, CINZA, (x, 0), (x, ALTURA))
    for y in range(0, ALTURA, TAMANHO_BLOCO):
        pygame.draw.line(tela, CINZA, (0, y), (LARGURA, y))


def main():
    snake = [(300, 300)]
    direcao = (TAMANHO_BLOCO, 0)

    comida = gerar_comida()
    pontuacao = 0

    rodando = True
    game_over = False

    while rodando:
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and direcao != (0, TAMANHO_BLOCO):
                    direcao = (0, -TAMANHO_BLOCO)
                if evento.key == pygame.K_DOWN and direcao != (0, -TAMANHO_BLOCO):
                    direcao = (0, TAMANHO_BLOCO)
                if evento.key == pygame.K_LEFT and direcao != (TAMANHO_BLOCO, 0):
                    direcao = (-TAMANHO_BLOCO, 0)
                if evento.key == pygame.K_RIGHT and direcao != (-TAMANHO_BLOCO, 0):
                    direcao = (TAMANHO_BLOCO, 0)

                if game_over and evento.key == pygame.K_r:
                    main()

        if not game_over:
            # Move a cobra
            cabeca = (snake[0][0] + direcao[0], snake[0][1] + direcao[1])

            # Verifica colisão com parede
            if (
                cabeca[0] < 0
                or cabeca[0] >= LARGURA
                or cabeca[1] < 0
                or cabeca[1] >= ALTURA
                or cabeca in snake
            ):
                game_over = True

            snake.insert(0, cabeca)

            # Verifica se comeu a comida
            if cabeca == comida:
                pontuacao += 1
                comida = gerar_comida()
            else:
                snake.pop()

        # Desenho
        tela.fill(PRETO)
        desenhar_grade()

        # Desenha cobra
        for bloco in snake:
            pygame.draw.rect(tela, VERDE, (bloco[0], bloco[1], TAMANHO_BLOCO, TAMANHO_BLOCO))

        # Desenha comida
        pygame.draw.rect(tela, VERMELHO, (comida[0], comida[1], TAMANHO_BLOCO, TAMANHO_BLOCO))

        desenhar_texto(f"Pontuação: {pontuacao}", BRANCO, 10, 10)

        if game_over:
            desenhar_texto("GAME OVER", VERMELHO, 200, 250)
            desenhar_texto("Pressione R para reiniciar", BRANCO, 130, 300)

        pygame.display.update()


if __name__ == "__main__":
    main()