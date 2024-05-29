import pygame
import random
import time
import os

TAMANO_CUADRO = 64
FILAS = 15
COLUMNAS = 10
WIDTH = FILAS * TAMANO_CUADRO
HEIGHT = COLUMNAS * TAMANO_CUADRO
FPS = 60

TITLE, GAME, END, RANKING, OPCION = 0, 1, 2, 3, 4
currentScreen = TITLE
selectedOption = 0
selectedOptionInOptions = 0

comidaPos = [0, 0]
serpientePos = [0, 0]
direccionSerpiente = 0
perdido = False
enfriamientoJuego = 0
tiempoParteSerpiente = [[0] * COLUMNAS for _ in range(FILAS)]
poderCreacion = 2
framesCounter = 0
score = 0

dificultad = 1
serpiente_speed = 0.5

notification_start_time = None
notification_text = ""

MAX_RANKINGS = 10
rankings = [0] * MAX_RANKINGS
rankingsFilePath = "Docs/rankings.txt"


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Serpiente")
clock = pygame.time.Clock()


fruit = pygame.image.load("IMG/Graphics/Cake.png")
backgroundImage = pygame.image.load("IMG/Menu_img.png")
loseImage = pygame.image.load("IMG/Lose_img.png")
rankingImage = pygame.image.load("IMG/Ranking_img.png")


apariencias = [
    {
        "snakeUp": pygame.image.load("IMG/Graphics/head_up.png"),
        "snakeDown": pygame.image.load("IMG/Graphics/head_down.png"),
        "snakeLeft": pygame.image.load("IMG/Graphics/head_left.png"),
        "snakeRight": pygame.image.load("IMG/Graphics/head_right.png"),
        "body": pygame.image.load("IMG/Graphics/body.png"),
        "eatSoundPath": "FX/Yoshi.mp3",
        "backgroundMusicPath": "FX/Back.wav"
    },
    
    {
        "snakeUp": pygame.image.load("IMG/Graphics/Kirby_up.png"),
        "snakeDown": pygame.image.load("IMG/Graphics/Kirby_down.png"),
        "snakeLeft": pygame.image.load("IMG/Graphics/Kirby_left.png"),
        "snakeRight": pygame.image.load("IMG/Graphics/Kirby_right.png"),
        "body": pygame.image.load("IMG/Graphics/star.png"),
        "eatSoundPath": "FX/Kirby_Poyo.mp3",
        "backgroundMusicPath": "FX/Gourmet_Race.mp3"
    },
    
    {
        "snakeUp": pygame.image.load("IMG/Graphics/assets/La_creatura_up.png"),
        "snakeDown": pygame.image.load("IMG/Graphics/assets/La_creatura_down.png"),
        "snakeLeft": pygame.image.load("IMG/Graphics/assets/La_creatura_left.png"),
        "snakeRight": pygame.image.load("IMG/Graphics/assets/La_creatura_right.png"),
        "body": pygame.image.load("IMG/Graphics/assets/La_creatura_body.png"),
        "eatSoundPath": "FX/eating.mp3",
        "backgroundMusicPath": "FX/Classic.mp3"
    },
    
]

apariencia = 0
current_apariencia = apariencias[apariencia]
eatSound = pygame.mixer.Sound(current_apariencia["eatSoundPath"])


gameBackground = pygame.image.load("IMG/Graphics/Background.png")
backgroundMusicPath = "FX/Back.wav"
loseSoundPath = "FX/Lose_Sound.mp3"

pygame.mixer.music.load(backgroundMusicPath)
loseSound = pygame.mixer.Sound(loseSoundPath)

pygame.mixer.music.set_volume(0.10)
eatSound.set_volume(0.5)

def updateRanking(newScore):
    for i in range(MAX_RANKINGS):
        if newScore > rankings[i]:
            for j in range(MAX_RANKINGS - 1, i, -1):
                rankings[j] = rankings[j - 1]
            rankings[i] = newScore
            break

def loadRanking():
    try:
        with open(rankingsFilePath, "r") as file:
            for i in range(MAX_RANKINGS):
                rankings[i] = int(file.readline().strip())
    except FileNotFoundError:
        pass

def saveRanking():
    with open(rankingsFilePath, "w") as file:
        for i in range(MAX_RANKINGS):
            file.write(f"{rankings[i]}\n")

loadRanking()
pygame.mixer.music.play(-1)

comidaPos[0] = random.randint(0, FILAS - 1)
comidaPos[1] = random.randint(0, COLUMNAS - 1)
serpientePos[0] = FILAS // 2
serpientePos[1] = COLUMNAS // 2

estructura1Pos = [random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)]
estructura2Pos = [random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)]
estructura3Pos = [random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)]
estructura4Pos = [random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)]


arrow_released = True
space_released = True

running = True

while running:
    
    screen.fill((0, 0, 0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if currentScreen == TITLE:
        screen.blit(backgroundImage, (0, 0))
        

        custom_font = pygame.font.Font("Font/Minecraft.ttf", 35)

        opciones = ["Iniciar", "Ranking", "Opciones", "Cerrar juego"]
        posY = [HEIGHT // 2 - 120, HEIGHT // 2 - 40, HEIGHT // 2 + 40, HEIGHT // 2 + 120]

        for i, opcion in enumerate(opciones):
            text = custom_font.render(opcion, True, (0, 0, 0) if selectedOption == i else (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, posY[i]))
            
            if selectedOption == i:
                pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(20, 20))
                
            screen.blit(text, text_rect)

        
        if (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and arrow_released:
            arrow_released = False
            
            if keys[pygame.K_DOWN]:
                selectedOption = (selectedOption + 1) % 4
            elif keys[pygame.K_UP]:
                selectedOption = (selectedOption - 1) % 4

        if not (keys[pygame.K_DOWN] or keys[pygame.K_UP]):
            arrow_released = True

        if keys[pygame.K_SPACE] and space_released:
            space_released = False
            
            if selectedOption == 0:
                
                perdido = False
                poderCreacion = 2
                score = 0
                comidaPos[0] = random.randint(0, FILAS - 1)
                comidaPos[1] = random.randint(0, COLUMNAS - 1)
                serpientePos[0] = FILAS // 2
                serpientePos[1] = COLUMNAS // 2
                tiempoParteSerpiente = [[0] * COLUMNAS for _ in range(FILAS)]
                currentScreen = GAME
                
            elif selectedOption == 1:
                currentScreen = RANKING
                
            elif selectedOption == 2:
                currentScreen = OPCION
                    
            else:
                running = False

        if not keys[pygame.K_SPACE]:
            space_released = True

    elif currentScreen == GAME:
        
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.music.unpause()
        
        framesCounter += 1
        
        if framesCounter >= 3 / serpiente_speed: 
            serpientePos[0] += 1 if direccionSerpiente == 0 else (-1 if direccionSerpiente == 1 else 0)
            serpientePos[1] += 1 if direccionSerpiente == 2 else (-1 if direccionSerpiente == 3 else 0)

            if serpientePos[0] < 0 or serpientePos[1] < 0 or serpientePos[0] >= FILAS or serpientePos[1] >= COLUMNAS or tiempoParteSerpiente[serpientePos[0]][serpientePos[1]] > 1:
                pygame.mixer.music.pause()
                updateRanking(score)
                perdido = True
                saveRanking()
                loseSound.play()
                currentScreen = END

            if not perdido:
                tiempoParteSerpiente[serpientePos[0]][serpientePos[1]] = poderCreacion

            for i in range(FILAS):
                
                for j in range(COLUMNAS):
                    
                    if tiempoParteSerpiente[i][j] > 0:
                        tiempoParteSerpiente[i][j] -= 1

            framesCounter = 0

        enfriamientoJuego += 1

        direccionSerpiente = 1 if keys[pygame.K_LEFT] else (0 if keys[pygame.K_RIGHT] else (3 if keys[pygame.K_UP] else (2 if keys[pygame.K_DOWN] else direccionSerpiente)))

        if serpientePos[0] == comidaPos[0] and serpientePos[1] == comidaPos[1]:
            
            while tiempoParteSerpiente[comidaPos[0]][comidaPos[1]] > 0:
                comidaPos[0] = random.randint(0, FILAS - 1)
                comidaPos[1] = random.randint(0, COLUMNAS - 1)

            poderCreacion += 1
            score += 10
            eatSound.play()
            

        if (serpientePos == estructura1Pos) or (serpientePos == estructura2Pos) or (serpientePos == estructura3Pos) or (serpientePos == estructura4Pos):
            comidaPos[0] = random.randint(0, FILAS - 1)
            comidaPos[1] = random.randint(0, COLUMNAS - 1)

            while True:
                nueva_pos_estructura1 = [random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)]
                if nueva_pos_estructura1 != serpientePos and nueva_pos_estructura1 != comidaPos:
                    estructura1Pos = nueva_pos_estructura1
                    break

            while True:
                nueva_pos_estructura2 = [random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)]
                if nueva_pos_estructura2 != serpientePos and nueva_pos_estructura2 != comidaPos and nueva_pos_estructura2 != estructura1Pos:
                    estructura2Pos = nueva_pos_estructura2
                    break

            while True:
                nueva_pos_estructura3 = [random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)]
                if nueva_pos_estructura3 != serpientePos and nueva_pos_estructura3 != comidaPos and nueva_pos_estructura3 != estructura1Pos and nueva_pos_estructura3 != estructura2Pos:
                    estructura3Pos = nueva_pos_estructura3
                    break

            while True:
                nueva_pos_estructura4 = [random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)]
                if nueva_pos_estructura4 != serpientePos and nueva_pos_estructura4 != comidaPos and nueva_pos_estructura4 != estructura1Pos and nueva_pos_estructura4 != estructura2Pos and nueva_pos_estructura4 != estructura3Pos:
                    estructura4Pos = nueva_pos_estructura4
                    break


        if not perdido:
            screen.blit(gameBackground, (0, 0))
            screen.blit(fruit, (comidaPos[0] * TAMANO_CUADRO, comidaPos[1] * TAMANO_CUADRO))

            pygame.draw.rect(screen, (255, 0, 0), (estructura1Pos[0] * TAMANO_CUADRO, estructura1Pos[1] * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
            pygame.draw.rect(screen, (255, 0, 0), (estructura2Pos[0] * TAMANO_CUADRO, estructura2Pos[1] * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
            pygame.draw.rect(screen, (255, 0, 0), (estructura3Pos[0] * TAMANO_CUADRO, estructura3Pos[1] * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
            pygame.draw.rect(screen, (255, 0, 0), (estructura4Pos[0] * TAMANO_CUADRO, estructura4Pos[1] * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))

            for i in range(FILAS):
                for j in range(COLUMNAS):
                    if tiempoParteSerpiente[i][j] > 0:
                        
                        if i == serpientePos[0] and j == serpientePos[1]:
                            continue
                        
                        screen.blit(current_apariencia["body"], (i * TAMANO_CUADRO, j * TAMANO_CUADRO))
                        
            currentTexture = (current_apariencia["snakeRight"] if direccionSerpiente == 0 else 
                            current_apariencia["snakeLeft"] if direccionSerpiente == 1 else 
                            current_apariencia["snakeDown"] if direccionSerpiente == 2 else 
                            current_apariencia["snakeUp"])
            screen.blit(currentTexture, (serpientePos[0] * TAMANO_CUADRO, serpientePos[1] * TAMANO_CUADRO))
            
            if serpientePos[0] == comidaPos[0] and serpientePos[1] == comidaPos[1]:
                eatSound.play()


    elif currentScreen == END:
        screen.fill((0, 0, 0))
        screen.blit(loseImage, (0, 0))
        text = custom_font.render(f"Puntaje: {score}", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + HEIGHT // 6 - 40))
        screen.blit(text, text_rect)
        
        if keys[pygame.K_SPACE] and space_released:
            space_released = False
            currentScreen = TITLE

        if not keys[pygame.K_SPACE]:
            space_released = True

    elif currentScreen == RANKING:
        screen.fill((0, 0, 0))
        screen.blit(rankingImage, (0, 0))
        text = custom_font.render("Ranking", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 50 + HEIGHT // 10))
        screen.blit(text, text_rect)

        for i in range(MAX_RANKINGS):
            text = custom_font.render(f"{i + 1}. {rankings[i]}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, 100 + HEIGHT // 10 + i * 40))
            screen.blit(text, text_rect)
        
        if keys[pygame.K_SPACE] and space_released:
            space_released = False
            currentScreen = TITLE

        if not keys[pygame.K_SPACE]:
            space_released = True
            
    elif currentScreen == OPCION:
        screen.fill((0, 0, 0))
        screen.blit(rankingImage, (0, 0))  
        
        custom_font_large = pygame.font.Font("Font/Minecraft.ttf", 50) 

        text = custom_font_large.render("Opciones", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 50 + HEIGHT // 10 + 10))
        screen.blit(text, text_rect)

        custom_font = pygame.font.Font("Font/Minecraft.ttf", 35)
        opciones = ["Cambiar Apariencia", "Cambiar Dificultad", "Regresar"]
        posY = [HEIGHT // 2 - 40, HEIGHT // 2 + 40, HEIGHT // 2 + 120]

        for i, opcion in enumerate(opciones):
            text = custom_font.render(opcion, True, (0, 0, 0) if selectedOptionInOptions == i else (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, posY[i]))
            
            if selectedOptionInOptions == i:
                pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(20, 20))
                
            screen.blit(text, text_rect)

        if (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and arrow_released:
            arrow_released = False
            
            if keys[pygame.K_DOWN]:
                selectedOptionInOptions = (selectedOptionInOptions + 1) % 3
            elif keys[pygame.K_UP]:
                selectedOptionInOptions = (selectedOptionInOptions - 1) % 3

        if not (keys[pygame.K_DOWN] or keys[pygame.K_UP]):
            arrow_released = True

        if keys[pygame.K_SPACE] and space_released:
            space_released = False
            
            if selectedOptionInOptions == 0:
                apariencia = (apariencia + 1) % len(apariencias)
                current_apariencia = apariencias[apariencia]
                eatSound = pygame.mixer.Sound(current_apariencia["eatSoundPath"])
                pygame.mixer.music.stop()
                pygame.mixer.music.load(current_apariencia["backgroundMusicPath"])
                pygame.mixer.music.play(-1)
                notification_text = "Apariencia cambiada"
                notification_start_time = time.time()
                
            elif selectedOptionInOptions == 1:
                dificultad = (dificultad % 3) + 1
                serpiente_speed = 0.5 * dificultad
                notification_text = f"Dificultad cambiada a {dificultad}"
                notification_start_time = time.time()
                
            elif selectedOptionInOptions == 2:
                currentScreen = TITLE

        if not keys[pygame.K_SPACE]:
            space_released = True

    if notification_start_time and time.time() - notification_start_time < 2:
        notification_font = pygame.font.Font("Font/Minecraft.ttf", 25)
        notification = notification_font.render(notification_text, True, (255, 255, 255))
        notification_rect = notification.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        pygame.draw.rect(screen, (0, 0, 0), notification_rect.inflate(20, 20))
        screen.blit(notification, notification_rect)
        
    else:
        notification_start_time = None

    pygame.display.flip()
    
    clock.tick(30)

serpiente_speed = 0.5

pygame.quit()