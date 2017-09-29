# --------------------------------- #
# --- Importation des libraries --- #
from sense_hat import SenseHat
import time
import random

# --------------------------------- #
# --- Declaration des variables --- #
s = SenseHat()
#s.set_imu_config(False, True, False)
last_direction = 'right'

red = (255, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
nothing = (0, 0, 0)

listX = [3, 2, 1, 0]
listY = [3, 3, 3, 3]

appleX = 0
appleY = 0
score = 0
level = 1
appleCount = 0

#Variables pour gyroscope
'''
global orientation
orientation = s.get_orientation()

global left
left = False
global leftOr
leftOr = 0
global right
right = False
global rightOr
rightOr = 0
global top
top = False
global topOr
topOr = 0
global bottom
bottom = False
global bottomOr
bottomOr = 0

global playModeRoll
playModeRoll = True
'''
# Variable de vérification
global on
on = True


def getOn():
    return on


def setOn(temp):
    global on
    on = temp

# --------------------------------- #
# ----------- Fonctions ----------- #
# Fonction pour l'affichage du snake et des pommes
def update_screen():
    s.clear()
    s.set_pixel(listX[0], listY[0], white)
    s.set_pixel(listX[1], listY[1], white)
    s.set_pixel(listX[2], listY[2], white)
    s.set_pixel(listX[3], listY[3], white)
    s.set_pixel(appleX, appleY, red)

# Fonction de génération aléatoire de pommes ( une à la fois )
def setup_apple():
    global appleX
    global appleY
    posOK = False
    while not posOK:
        appleX = random.randint(0, 7)
        appleY = random.randint(0, 7)
        i = 0
        posOK = True
        while i < 4:
            if listX[i] == appleX and listY[i] == appleY:
                posOK = False
            i += 1

# Fonction de vérification si une pomme a été mangée
def check_apple():
    global score
    global appleCount
    global level
    if listX[0] == appleX and listY[0] == appleY:
        score += 1*level
        appleCount += 1
        if appleCount % 2 == 0:
            level += 1
            setOn(False)
            s.show_message("Level " + str(level), 0.05, green)
            s.stick.get_events().clear()
            update_screen()
        setup_apple()
    setOn(True)

# Fonction qui met à jour la position du snake sur le tableau de pixels
def move_body():
    listX[3] = listX[2]
    listX[2] = listX[1]
    listX[1] = listX[0]
    listY[3] = listY[2]
    listY[2] = listY[1]
    listY[1] = listY[0]

# Fonction lié aux événements du joystick
def move(event):
    global appleCount
    if getOn():
        if event.action in ('pressed', 'held'):
            global last_direction
            if event.direction == 'up': # Avance vers le haut
                if last_direction != 'down':
                    if listY[0] > 0:
                        move_body() # Déplacement du snake
                        listY[0] = listY[0] - 1
                        check_apple() # Vérification si une pomme a été mangée
                        last_direction = event.direction # Pour le move auto
                    else:
                        game_over()
            elif event.direction == 'down': # Avance vers le bas
                if last_direction != 'up':
                    if listY[0] < 7:
                        move_body()
                        listY[0] = listY[0] + 1
                        check_apple()
                        last_direction = event.direction
                    else:
                        game_over()
            elif event.direction == 'left': # Avance vers la gauche
                if last_direction != 'right':
                    if listX[0] > 0:
                        move_body()
                        listX[0] = listX[0] - 1
                        check_apple()
                        last_direction = event.direction
                    else:
                        game_over()
            elif event.direction == 'right': # Avance vers la droite
                if last_direction != 'left':
                    if listX[0] < 7:
                        move_body()
                        listX[0] = listX[0] + 1
                        check_apple()
                        last_direction = event.direction
                    else:
                        game_over()

# Fonction qui gère le déplacement automatique du snake
def move_auto():
    if last_direction == 'left': # Avance automatiquement vers la gauche
        if listX[0] > 0:
            move_body()
            listX[0] = listX[0] - 1
            check_apple()
            update_screen()
        else:
            game_over()
    elif last_direction == 'right': # Avance automatiquement vers la droite
        if listX[0] < 7:
            move_body()
            listX[0] = listX[0] + 1
            check_apple()
            update_screen()
        else:
            game_over()
    elif last_direction == 'up': # Avance automatiquement vers le haut
        if listY[0] > 0:
            move_body()
            listY[0] = listY[0] - 1
            check_apple()
            update_screen()
        else:
            game_over()
    elif last_direction == 'down': # Avance automatiquement vers le bas
        if listY[0] < 7:
            move_body()
            listY[0] = listY[0] + 1
            check_apple()
            update_screen()
        else:
            game_over()


#Fonctions pour mouvements avec gyroscope
'''
def check():
    if orientation['pitch'] > 300 and orientation['pitch'] < 345:
        #droite
        global right
        global rightOr
        right = True
        rightOr = 345 - orientation['pitch']
    
    if orientation['pitch'] > 15 and orientation['pitch'] < 60:
        #gauche
        global left
        global leftOr
        left = True
        leftOr = 15 + orientation['pitch']
    
    if orientation['roll'] > 300 and orientation['roll'] < 345:
        #haut
        global top
        global topOr
        top = True
        topOr = 345 - orientation['roll']

    if orientation['roll'] > 15 and orientation['roll'] < 60:
        #bas
        global bottom
        global bottomOr
        bottom = True
        bottomOr = 15 + orientation['roll']
    
    doTheMove()


def doTheMove():
    if left:
        if top:
            if leftOr > topOr:
                if listX[0] > 0:
                    move_body()
                    listX[0] = listX[0] - 1
                    check_apple()
                    update_screen()
                    last_direction = 'left'
                else:
                    game_over()
            elif topOr >= leftOr:
                 if listY[0] > 0:
                    move_body()
                    listY[0] = listY[0] - 1
                    check_apple()
                    update_screen()
                    last_direction = 'up'
                else:
                    game_over()
        elif bottom:
            if leftOr > bottomOr:
                if listX[0] > 0:
                    move_body()
                    listX[0] = listX[0] - 1
                    check_apple()
                    update_screen()
                    last_direction = 'left'
                else:
                    game_over()
            elif bottomOr >= leftOr:
                if listY[0] < 7:
                    move_body()
                    listY[0] = listY[0] + 1
                    check_apple()
                    update_screen()
                    last_direction = 'down'
                else:
                    game_over()
        else:
            if listX[0] > 0:
                move_body()
                listX[0] = listX[0] - 1
                check_apple()
                update_screen()
                last_direction = 'left'
            else:
                game_over()
    elif right:
        if top:
            if rightOr > topOr:
                if listX[0] > 0:
                    move_body()
                    listX[0] = listX[0] - 1
                    check_apple()
                    update_screen()
                    last_direction = 'right'
                else:
                    game_over()
            elif topOr >= rightOr:
                if listY[0] > 0:
                    move_body()
                    listY[0] = listY[0] - 1
                    check_apple()
                    update_screen()
                    last_direction = 'up'
                else:
                    game_over()
        elif bottom:
            if rightOr > bottomOr:
                if listX[0] > 0:
                    move_body()
                    listX[0] = listX[0] - 1
                    check_apple()
                    update_screen()
                    last_direction = 'right'
                else:
                    game_over()
            elif bottomOr >= rightOr:
                if listY[0] < 7:
                    move_body()
                    listY[0] = listY[0] + 1
                    check_apple()
                    update_screen()
                    last_direction = 'down'
                else:
                    game_over()
        else:
            if listX[0] > 0:
                move_body()
                listX[0] = listX[0] - 1
                check_apple()
                update_screen()
                last_direction = 'right'
            else:
                game_over()
    elif top:
        if listY[0] > 0:
            move_body()
            listY[0] = listY[0] - 1
            check_apple()
            update_screen()
            last_direction = 'up'
        else:
            game_over()
    elif bottom:
        if listY[0] < 7:
            move_body()
            listY[0] = listY[0] + 1
            check_apple()
            update_screen()
            last_direction = 'down'
        else:
            game_over()
    else:
        move_auto()

'''

# Fonction de fin de jeu
def game_over():
    global last_direction
    global score
    global level
    global appleCount
    s.clear()
    setOn(False)
    s.show_message("GAME OVER: " + str(score) + " points", 0.05, red)
    setOn(True)
    # Réinitialisation des variables pour une nouvelle partie
    listX[3] = 0
    listX[2] = 1
    listX[1] = 2
    listX[0] = 3
    listY[3] = 3
    listY[2] = 3
    listY[1] = 3
    listY[0] = 3
    last_direction = 'right'
    setup_apple()
    score = 0
    level = 1
    appleCount = 0

# Fonction principale qui fait tourner le jeu et qui gère la difficulté
def run():
    global orientation
    while True:
        while getOn():
            move_auto()
            if level < 34:
                time.sleep(2 - (level * 0.1))
            else:
                time.sleep(0.3)
        
        #Boucle pour jouer avec le gyroscope
        '''
        while playModeRoll:
            check()
            orientation = s.get_orientation()
            left = False
            right = False
            top = False
            bottom = False
            if level < 34:
                time.sleep(2 - (level * 0.1))
            else:
                time.sleep(0.3)

        '''
        time.sleep(1)

# --------------------------------- #
# ---- Gestion des événements ----- #
s.stick.direction_up = move
s.stick.direction_down = move
s.stick.direction_left = move
s.stick.direction_right = move
s.stick.direction_any = update_screen

# --------------------------------- #
# --- Appel des fonctions de jeu ---#
setup_apple()
update_screen()

run()