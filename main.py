from PPlay.window import *
from PPlay.gameimage import GameImage
from PPlay.sprite import *
from random import *

images = "Assets/images/"

#Janela
janela = Window(800,600)
janela.set_title("Pong")

#fundo da janela
fundo = GameImage(images + "fundo.png")

#bolinha
ball = Sprite(images + "ball.png")
ball.set_position(janela.width/2 - ball.width ,janela.height/2 - ball.height)
velox = 200
veloy = 200

#Pads
padbot = Sprite(images + "pad1.png")
pad2 = Sprite(images + "pad2.png")
padbot.set_position(2,(janela.height - padbot.height)/2)
pad2.set_position(janela.width - pad2.width - 2,(janela.height - pad2.height)/2)
velby = 0

#Teclado
teclado = Window.get_keyboard()

#restart
restart = False
gameover = False
gamewinner = False
pontoesq = 0
pontodir = 0 

#GameMode
game_mode = "pause"

#Gerando a janela
while True:

    if teclado.key_pressed("space"):
        game_mode = 'jogando'
    if  not restart == True and game_mode == "jogando":
        ball.x += velox * janela.delta_time()
        ball.y += veloy * janela.delta_time()

    padbot.y += velby
    
    fundo.draw()
    ball.draw()
    padbot.draw()
    pad2.draw()

    if not gameover:
        #Detectando colisões
            #Barras horizontais
        if ball.y + ball.height >= janela.height or ball.y <= 0:
            veloy *= -1

        #Verificando pontos
        if ball.x + ball.width >= janela.width: 
            ball.set_position(janela.width/2 - ball.width ,janela.height/2 - ball.height)
            padbot.set_position(2,(janela.height - padbot.height)/2)
            pad2.set_position(janela.width - pad2.width,(janela.height - pad2.height)/2)
            restart = True
            veloy = 0
            pontodir += 1
            game_mode = "pause"
        elif ball.x <= 0:
            ball.set_position(janela.width/2 - ball.width ,janela.height/2 - ball.height)
            padbot.set_position(2,(janela.height - padbot.height)/2)
            pad2.set_position(janela.width - pad2.width,(janela.height - pad2.height)/2)
            restart = True
            veloy = 0
            pontoesq += 1
            game_mode = "pause"

        if teclado.key_pressed("space") and restart:
                restart = False
                veloy = 200

        #Movendo o pad2
        if teclado.key_pressed("up") and pad2.y >= 0 and game_mode == "jogando": 
            pad2.move_key_y(200 * janela.delta_time())
        if teclado.key_pressed("down") and (pad2.y + pad2.height) <= janela.height and game_mode == "jogando":
            pad2.move_key_y(200 * janela.delta_time())

        #Colisao bolinha
        if ball.collided(pad2): #Colisao bolinha-player
            velox *= -1
        elif ball.collided(padbot): #Colisao bolinha-bot
            velox *= -1

        #Controle do bot
        if veloy > 0 and (padbot.y + padbot.height) <= janela.height and game_mode == "jogando":
            velby = 120 * janela.delta_time()
        elif veloy < 0 and padbot.y >=0 :
            velby = -120 * janela.delta_time()
        elif veloy == 0:
            velby = 0 * janela.delta_time()
        
        timer = 0
        #Verificar GameOver
        if pontoesq == 3:
            gamewinner = True
            game_mode = "End"
            timer = janela.time_elapsed()
        elif pontodir == 3:
            gameover = True
            game_mode = "End"
            timer = janela.time_elapsed()

        #Placar 
        janela.draw_text(str(pontodir),200,30, size=40, color =(255,255,255))
        janela.draw_text(str(pontoesq),600,30, size=40, color =(255,255,255))
        
    #GameOver
    if gameover:
        janela.draw_text("Game Over", 250, 150, size=60, color =(255,255,255))
        janela.draw_text("Jogador da Esquerda venceu!", 205, 225, size=30, color =(255,255,255))
    elif gamewinner:
        janela.draw_text("Game Winner", 225, 150, size=60, color =(255,255,255))
        janela.draw_text("Você venceu!", (janela.width/2)-100, 225, size=30, color =(255,255,255))

    clock = janela.time_elapsed() - timer 
    if game_mode == "End" and clock >= 5000:
        janela.close()
        
    
    janela.update()