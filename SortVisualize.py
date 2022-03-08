from pickle import FALSE
import pygame, random, math

check_errors=pygame.init()

if(check_errors[1]>0):
    print("Error "+check_errors[1])
else:
    print("Algorithm Initialized!")

class drawInfo:
    red=pygame.Color(165,124,214)
    green=pygame.Color(150,255,136)
    black=pygame.Color(0,0,0)
    dark_gray=pygame.Color(40,40,60)
    gray=pygame.Color(180,180,180)
    white=pygame.Color(255,255,255)
    bg_col=dark_gray
    gradient=[(144,175,197), (157,184,204)]

    side_pad=100
    top_pad=150
    font=pygame.font.SysFont('gotham', 30)
    big_font=pygame.font.SysFont('gotham', 40)

    def __init__(self, width, height, lst):
        self.width=width
        self.height=height

        self.window=pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sort Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst=lst
        self.min_val=min(lst)
        self.max_val=max(lst)
        self.block_width=((self.width-self.side_pad)/len(lst))
        self.block_height=((self.height-self.top_pad)/(self.max_val-self.min_val))
        self.start_x=self.side_pad//2

def draw(draw_info, sort_algo_name, ascend):
    draw_info.window.fill(draw_info.bg_col)

    pygame.draw.rect(draw_info.window, draw_info.black, (0,0,1280,100))
    title=draw_info.big_font.render(f"{sort_algo_name}  -  {'Ascending' if ascend else 'Descending'}", 1, draw_info.white)
    draw_info.window.blit(title, (draw_info.width/2-title.get_width()/2, 25))

    #controls=draw_info.font.render("R - Reset | SPACE - Start sorting | A - Ascend | D - Descend", 1, draw_info.white)
    #draw_info.window.blit(controls, (draw_info.width/2-controls.get_width()/2, 45))

    sort_type=draw_info.font.render("I - Insertion Sort     |     B - Bubble Sort", 1, draw_info.gray)
    draw_info.window.blit(sort_type, (draw_info.width/2-sort_type.get_width()/2, 65))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_pos={}, clear_bg=False):
    lst=draw_info.lst

    if clear_bg:
        clear_rect=(draw_info.side_pad//2, draw_info.top_pad, draw_info.width-draw_info.side_pad, draw_info.height-draw_info.top_pad)
        pygame.draw.rect(draw_info.window, draw_info.bg_col, clear_rect)

    for i, val in enumerate(lst):
        x=draw_info.start_x+i*draw_info.block_width
        y=draw_info.height-(val-draw_info.min_val)*draw_info.block_height

        color=draw_info.gradient[i%2]

        if i in color_pos:
            color=color_pos[i]

        pygame.draw.rect(draw_info.window, color, pygame.Rect(x, y, draw_info.block_width-2, draw_info.height))

    if clear_bg:
        pygame.display.update()

def genList(n, min_val, max_val):
    lst=[]

    for _ in range(n):
        val=random.randint(min_val, max_val)
        lst.append(val)

    return lst

def bubble_sort(draw_info, ascend=True):
    lst=draw_info.lst
    n=len(lst)

    for i in range(n-1):
        for j in range(n-1-i):
            num1=lst[j]
            num2=lst[j+1]

            if(num1>num2 and ascend) or (num1<num2 and not ascend):
                lst[j], lst[j+1]=lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.green, j+1: draw_info.red}, True)
                yield True

    return lst

def insertion_sort(draw_info, ascend=True):
    lst=draw_info.lst
    n=len(lst)

    for i in range(1, n):
        cur=lst[i]

        while True:
            ascend_sort=i>0 and lst[i-1]>cur and ascend
            descend_sort=i>0 and lst[i-1]<cur and not ascend

            if not ascend_sort and not descend_sort:
                break
                
            lst[i]=lst[i-1]
            i=i-1
            lst[i]=cur
            draw_list(draw_info, {i-1: draw_info.green, i: draw_info.red}, True)
            yield True

def main():
    run=True
    fps=pygame.time.Clock()

    n=100
    min_val=1
    max_val=300

    lst=genList(n, min_val, max_val)
    draw_info=drawInfo(1280, 800, lst)
    sort=False
    ascend=True

    sort_algo=bubble_sort
    sort_algo_name="Bubble Sort"
    sort_algo_gen=None

    while run:
        fps.tick(120)

        if sort:
            try:
                next(sort_algo_gen)
            except StopIteration:
                sort=False
        else:
            draw(draw_info, sort_algo_name, ascend)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type!=pygame.KEYDOWN:
                continue
            if event.key==pygame.K_r:
                lst=genList(n, min_val, max_val)
                draw_info.set_list(lst)
                sort=False
            elif event.key==pygame.K_SPACE and sort==False:
                sort=True
                sort_algo_gen=sort_algo(draw_info, ascend)
            elif event.key==pygame.K_a and not sort:
                ascend=True
            elif event.key==pygame.K_d and not sort:
                ascend=False
            elif event.key==pygame.K_i and not sort:
                sort_algo=insertion_sort
                sort_algo_name="Insertion Sort"
            elif event.key==pygame.K_b and not sort:
                sort_algo=bubble_sort
                sort_algo_name="Bubble Sort"

    pygame.quit()

if __name__=="__main__":
    main()