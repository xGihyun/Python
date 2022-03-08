import pygame, sys, time, random

speed=15

frameX=720
frameY=480

check_errors=pygame.init()

if(check_errors[1]>0):
    print("Error "+check_errors[1])
else:
    print("Game Initialized!")

#window
pygame.display.set_caption("Snake Game")
window=pygame.display.set_mode((frameX, frameY))
pygame.display.update()

#colors
red=pygame.Color(255,0,0)
green=pygame.Color(0,255,0)
black=pygame.Color(0,0,0)
white=pygame.Color(255,255,255)

fps=pygame.time.Clock()

square_size=20

def init_vars():
    global body, head_pos, food_pos, food_spawn, score, direc
    direc="RIGHT"
    head_pos=[120,60]
    body=[[120,60]]
    food_pos=[random.randrange(1, (frameX//square_size))*square_size, random.randrange(1, (frameY//square_size))*square_size]
    food_spawn=True
    score=0

init_vars()

def show_score(choice, color, font, size):
    font=pygame.font.SysFont(font, size)
    surf=font.render("Score: "+str(score), True, color)
    rect=surf.get_rect()
    if choice==1:
        rect.midtop=(frameX/10, 15)
    else:
        rect.midtop=(frameX/2, frameY/1.25)

    window.blit(surf, rect)

while(True):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif(event.type==pygame.KEYDOWN):
            if(event.key==pygame.K_UP or event.key==ord("w") and direc!="DOWN"):
                direc="UP"
            elif(event.key==pygame.K_DOWN or event.key==ord("s") and direc!="UP"):
                direc="DOWN"
            elif(event.key==pygame.K_LEFT or event.key==ord("a") and direc!="RIGHT"):
                direc="LEFT"
            elif(event.key==pygame.K_RIGHT or event.key==ord("d") and direc!="LEFT"):
                direc="RIGHT"
        
    if direc=="UP":
        head_pos[1]-=square_size
    elif direc=="DOWN":
        head_pos[1]+=square_size
    elif direc=="LEFT":
        head_pos[0]-=square_size
    else:
        head_pos[0]+=square_size
    
    if head_pos[0]<0:
        head_pos[0]=frameX-square_size
    elif head_pos[0]>frameX-square_size:
        head_pos[0]=0
    elif head_pos[1]<0:
        head_pos[1]=frameY-square_size
    elif head_pos[1]>frameY-square_size:
        head_pos[1]=0

    #eat food
    body.insert(0, list(head_pos))

    if(head_pos[0]==food_pos[0] and head_pos[1]==food_pos[1]):
        score+=1
        food_spawn=False
    else:
        body.pop()

    #spawn food
    if not food_spawn:
        food_pos=[random.randrange(1, (frameX//square_size))*square_size, random.randrange(1, (frameY//square_size))*square_size]
        food_spawn=True

    #GFX
    window.fill(black)

    for i in body:
        pygame.draw.rect(window, green, pygame.Rect(i[0]+2, i[1]+2, square_size-2, square_size))

    pygame.draw.rect(window, red, pygame.Rect(food_pos[0], food_pos[1], square_size, square_size))

    #game over
    for block in body[1:]:
        if head_pos[0]==block[0] and head_pos[1]==block[1]:
            init_vars()

    show_score(1, white, 'consolas', 20)
    pygame.display.update()
    fps.tick(speed)
