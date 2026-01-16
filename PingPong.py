import sys, pygame, os
from pygame import font

'''pendente: 
fazer tela de saída
ajustar velocidade da bolinha
reiniciar velocidade da bolinha'''

pygame.init()

#Definindo constantes do jogo
Largura = 500
Altura = 400
icon = pygame.image.load("img/icone.png")
pygame.display.set_icon(icon)

#janela
win = pygame.display.set_mode((Largura, Altura))
pygame.display.set_caption("Ping Pong")
fps = pygame.time.Clock()

#variáveis
running = True
LoopJogo = False
Pause = False
Final = False
SomAtivado = True
PontosJogador = 0
PontosBot = 0
VelBot = 2
final = None
sizeImage = (100,50)
sizeImageS = (35,35)

# configurando o som
Musica_Sound = pygame.mixer.Sound("sons/Musica_Sound.mp3")
Bolinha_Sound = pygame.mixer.Sound("sons/Bolinha_Sound.mp3")
Vitoria_Sound = pygame.mixer.Sound("sons/Vitoria_Sound.mp3")
Derrota_Sound = pygame.mixer.Sound("sons/Derrota_Sound.mp3")
Musica_Sound.set_volume(0.2)
Bolinha_Sound.set_volume(0.2)
Vitoria_Sound.set_volume(0.2)
Derrota_Sound.set_volume(0.2)
pygame.mixer.music.load("sons/Musica_Sound.mp3")
pygame.mixer.music.play(-1, 0.0)

#Cores
Branco = (255,255,255)
Vermelho = (255,0,0)
Verde = (124,252,0)
Azul = (109, 158, 237)
Vermelho2 = (217, 48, 15)
Amarelo = (218, 237, 109)

#Texto
fonte = pygame.font.Font(None,30)

#Cenário

TelaPause = {
    'objRect': pygame.Rect(0,0,500,400),
    'cor': Amarelo
}
TelaFinal = {
    'objRect': pygame.Rect(0,0,500,400)
}

TimeAzul ={
    'objRect': pygame.Rect(0,0,251,400),
    'cor': Azul
}

TimeVermelho ={
    'objRect': pygame.Rect(251,0,250,400),
    'cor': Vermelho2
}

#Jogador definições
jogador = {
    'objRect': pygame.Rect(10, 160, 10, 70),
    'cor': Branco,
    'vel': [0, 0]
}

#Bot Definições
bot = {
    'objRect': pygame.Rect(480, 160, 10, 70),
    'cor': Branco,
    'vel': [3,3]
}

#Bolinha Definições

bola = {
    'objRect': pygame.Rect(240, 190, 20, 20), 
    'cor': Branco,
    'vel': [3, 3]
}

#Resetar bola
def resetar_bola(bola):
    if bola['objRect'].left < 0:
        bola['objRect'].center = (150,200)
    if bola['objRect'].right >= 400:
        bola['objRect'].center = (300,200)
    bola['vel'][0] *= -1

#Botão Iniciar
def Iniciar():
    global LoopJogo, BotãoIniciar
    LoopJogo = True

def aumentar_velocidade(bola, fator=1.2, max_vel=10):
    vx, vy = bola['vel']
    vx = max(min(vx * fator, max_vel), -max_vel)
    vy = max(min(vy * fator, max_vel), -max_vel)
    bola['vel'] = [vx, vy]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    teclas = pygame.key.get_pressed()


    if PontosJogador != 10 and PontosBot != 10:
        if not LoopJogo:
            win.fill(Amarelo)

            #MENU do Jogo

            PP_Logo = pygame.image.load('img/PingPong_Logo.png')
            PP_red = pygame.transform.scale(PP_Logo,(200,200)) #redimensionarimg
            win.blit(PP_red, (155, 30))

            BotãoIniciar = pygame.image.load('img/Iniciar.png')
            BI_red = pygame.transform.scale(BotãoIniciar,sizeImage)#redimensionarimg
            BI_rect = BI_red.get_rect(topleft=(140,230)) #transformar surface em rect
            win.blit(BI_red, (140, 230))

            BotãoSair = pygame.image.load('img/Sair.png')
            BS_red = pygame.transform.scale(BotãoSair,sizeImage)#redimensionarimg
            BS_rect = BS_red.get_rect(topleft=(260,230)) #transformar surface em rect
            win.blit(BS_red, (260, 230))

            if not SomAtivado:
                BotãoSound = pygame.image.load('img/Sound.png')
                icon_red = pygame.transform.scale(BotãoSound,sizeImageS)#redimensionarimg
            else:
                BotãoNoSound = pygame.image.load('img/NoSound.png')
                icon_red = pygame.transform.scale(BotãoNoSound,sizeImageS)#redimensionarimg

            icon_rect = icon_red.get_rect(topleft=(450,20)) #transformar surface em rect
            win.blit(icon_red, icon_rect)

            # detectar clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BI_rect.collidepoint(event.pos):
                    LoopJogo = True
                if BS_rect.collidepoint(event.pos):
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if icon_rect.collidepoint(event.pos):
                        if not SomAtivado:
                            SomAtivado = True
                            pygame.mixer.music.load("sons/Musica_Sound.mp3")
                            pygame.mixer.music.play(-1, 0.0)
                        else:
                            SomAtivado = False
                            pygame.mixer.music.stop()

            pygame.display.flip()
            fps.tick(60)
            continue  # volta pro início do while
        
        #Pause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Pause = True
        if not Pause:
            if LoopJogo:

                pygame.draw.rect(win, TimeAzul['cor'], TimeAzul['objRect'])
                pygame.draw.rect(win, TimeVermelho['cor'], TimeVermelho['objRect'])

                #Movimentação Jogador

                jogador['vel'][1] = 0  # zera a velocidade a cada frame

                if teclas[pygame.K_w]:
                    jogador['vel'][1] = -5
                if teclas[pygame.K_s]:
                    jogador['vel'][1] = 5

                jogador['objRect'].y += jogador['vel'][1]

                if jogador['objRect'].top < 0:
                    jogador['objRect'].top = 0
                if jogador['objRect'].bottom > Altura:
                    jogador['objRect'].bottom = Altura

                #Linha divisória do jogo
                for y in range(0, 400, 20): 
                    pygame.draw.line(win, Branco, (250, y), (250, y + 10),2)

                #Movimentação da bolinha
                bola['objRect'].x += bola['vel'][0]
                bola['objRect'].y += bola['vel'][1]

                if bola['objRect'].left < 0:
                    PontosBot += 1
                    aumentar_velocidade(bola, fator=1.05)
                    resetar_bola(bola)
                if bola['objRect'].right >= Largura:
                    PontosJogador += 1
                    aumentar_velocidade(bola, fator=1.05)
                    resetar_bola(bola)
                if bola['objRect'].top < 0 or bola['objRect'].bottom > Altura:
                    bola['vel'][1] = -bola['vel'][1]
                if bola['vel'][1] == 0: bola['vel'][1] = 1
            
                #Retorno bola
                retornar_jogador = bola['objRect'].colliderect(jogador['objRect'])
                retornar_bot = bola['objRect'].colliderect(bot['objRect'])

                if retornar_jogador:
                    Bolinha_Sound.play()
                    bola['vel'][0] = -bola['vel'][0]
                if retornar_bot:
                    Bolinha_Sound.play()
                    bola['vel'][0] = -bola['vel'][0]

                #Movimentação do bot
                
                if bola['objRect'].x > 150:
                    if bola['objRect'].centery < bot['objRect'].centery:
                        bot['vel'][1] = -VelBot
                    elif bola['objRect'].centery > bot['objRect'].centery:
                        bot['vel'][1] = VelBot
                    else:
                        bot['vel'][1] = 0
                else:
                    bot['vel'][1] = 0

                bot['objRect'].y += bot['vel'][1]
                #Desenho das personagens
                pygame.draw.rect(win, bot['cor'], bot['objRect'])
                pygame.draw.ellipse(win, bola['cor'], bola['objRect'])
                pygame.draw.rect(win, jogador['cor'], jogador['objRect'])

                #Jogador Pontuação
                texto = fonte.render("Wins:",True,Branco)
                win.blit(texto,[30,30])
                ponts_jogador = fonte.render(str(PontosJogador),True,Branco)
                win.blit(ponts_jogador,[90,30])
                #Bot Pontuação
                texto = fonte.render("Wins:",True,Branco)
                win.blit(texto,[400,30])
                ponts_bot = fonte.render(str(PontosBot),True,Branco)
                win.blit(ponts_bot,[460,30])

                # flip()
                pygame.display.flip()

                fps.tick(60)
        else:
            pygame.draw.rect(win,TelaPause['cor'],TelaPause['objRect'])

            #Logo
            PP_Logo = pygame.image.load('img/PingPong_Logo.png')
            PP_red = pygame.transform.scale(PP_Logo,(200,200)) #redimensionarimg
            win.blit(PP_red, (155, 30))

            #Botões

            #Botão de Reset
            BotãoResetar = pygame.image.load('img/Resetar.png')
            BR_red = pygame.transform.scale(BotãoResetar,sizeImage)#redimensionarimg
            BR_rect = BR_red.get_rect(topleft=(50,230)) #transformar surface em rect
            win.blit(BR_red, (50, 230))

            #Botão de Continuar
            BotãoC = pygame.image.load('img/Continuar.png')
            BC_red = pygame.transform.scale(BotãoC,sizeImage)#redimensionarimg
            BC_rect = BC_red.get_rect(topleft=(200,230)) #transformar surface em rect
            win.blit(BC_red, (200, 230))

            BotãoSair = pygame.image.load('img/Sair.png')
            BS_red = pygame.transform.scale(BotãoSair,sizeImage)#redimensionarimg
            BS_rect = BS_red.get_rect(topleft=(350,230)) #transformar surface em rect
            win.blit(BS_red, (350, 230))

            if not SomAtivado:
                BotãoSound = pygame.image.load('img/Sound.png')
                icon_red = pygame.transform.scale(BotãoSound,sizeImageS)#redimensionarimg
            else:
                BotãoNoSound = pygame.image.load('img/NoSound.png')
                icon_red = pygame.transform.scale(BotãoNoSound,sizeImageS)#redimensionarimg

            icon_rect = icon_red.get_rect(topleft=(450,20)) #transformar surface em rect
            win.blit(icon_red, icon_rect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BS_rect.collidepoint(event.pos):
                    running = False
                if BR_rect.collidepoint(event.pos):
                    Pause = False
                    PontosJogador = 0
                    PontosBot = 0
                    resetar_bola(bola)
                    jogador['objRect'].x = 10
                    jogador['objRect'].y = 160
                    bot['objRect'].x = 480
                    bot['objRect'].y = 160
                    bola['objRect'].x = 240
                    bola['objRect'].y = 190
                if BC_rect.collidepoint(event.pos):
                    Pause = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if icon_rect.collidepoint(event.pos):
                        if not SomAtivado:
                            SomAtivado = True
                            pygame.mixer.music.load("sons/Musica_Sound.mp3")
                            pygame.mixer.music.play(-1, 0.0)
                        else:
                            SomAtivado = False
                            pygame.mixer.music.stop()

            pygame.display.update()
    if (PontosBot == 10 or PontosJogador == 10) and final is None:
        if PontosBot == 10:
            pygame.mixer.music.stop()
            final = 'DERROTA'
            cor = Vermelho
            Derrota_Sound.play()

        elif PontosJogador == 10:
            pygame.mixer.music.stop()
            final = 'VITÓRIA'
            cor = Verde
            Vitoria_Sound.play()

    if final:
        pygame.draw.rect(win,Amarelo,TelaFinal['objRect'])
        bola['vel'] = [0,0]
        bot['vel'] = [0,0]
        jogador['vel'] = [0,0]
        texto = fonte.render(final, True, cor)
        win.blit(texto, (200, 100))
        #Botões

        BotãoJogarNov = pygame.image.load('img/JogarNovamente.png')
        BJN_red = pygame.transform.scale(BotãoJogarNov,sizeImage)#redimensionarimg
        BJN_rect = BJN_red.get_rect(topleft=(140,230)) #transformar surface em rect
        win.blit(BJN_red, (140,230))

        BotãoSair = pygame.image.load('img/Sair.png')
        BS_red = pygame.transform.scale(BotãoSair,sizeImage)#redimensionarimg
        BS_rect = BS_red.get_rect(topleft=(260,230)) #transformar surface em rect
        win.blit(BS_red, (260,230))

        if not SomAtivado:
            BotãoSound = pygame.image.load('img/Sound.png')
            icon_red = pygame.transform.scale(BotãoSound,sizeImageS)#redimensionarimg
        else:
            BotãoNoSound = pygame.image.load('img/NoSound.png')
            icon_red = pygame.transform.scale(BotãoNoSound,sizeImageS)#redimensionarimg

        icon_rect = icon_red.get_rect(topleft=(450,20)) #transformar surface em rect
        win.blit(icon_red, icon_rect)

            # detectar clique do mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if BJN_rect.collidepoint(event.pos):
                final = None
                Pause = False
                LoopJogo = True 
                PontosJogador = 0
                PontosBot = 0

                # resetar posições
                jogador['objRect'].x = 10
                jogador['objRect'].y = 160

                bot['objRect'].x = 480
                bot['objRect'].y = 160

                bola['objRect'].x = 240
                bola['objRect'].y = 190

                # reativar música
                if SomAtivado:
                    pygame.mixer.music.load("sons/Musica_Sound.mp3")
                    pygame.mixer.music.play(-1, 0.0)
            if BS_rect.collidepoint(event.pos):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if icon_rect.collidepoint(event.pos):
                    if not SomAtivado:
                        SomAtivado = True
                        pygame.mixer.music.load("sons/Musica_Sound.mp3")
                        pygame.mixer.music.play(-1, 0.0)
                    else:
                        SomAtivado = False
                        pygame.mixer.music.stop()
        pygame.display.flip()
    pygame.display.flip()

pygame.quit()