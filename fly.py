import pygame
from pygame.locals import *
import random
from itertools import cycle
#初始化参数

Fps = 30
    
screen_Width = 288

screen_Height = 512

Pipe_size = 80

base_y= screen_Height*0.79 #地面最低位置

image = {}#定义一个储存字典,存入所有图片

hit = {}#获取边框大小

#加载文件
Playbody = (
    'png\\body1.png',
    'png\\body2.png',
    'png\\body3.png',
)#只有蓝色小鸟

Sky = (
    'png\\day.png',
    'png\\night.png',
)#天空文件地址

Figure = (
    'png\\0.png',
    'png\\1.png',
    'png\\2.png',
    'png\\3.png',
    'png\\4.png',
    'png\\5.png',
    'png\\6.png',
    'png\\7.png',
    'png\\8.png',
    'png\\9.png',
)#数字文件地址

gameover = 'png\\gameover.png' #游戏结束语

message = 'png\\message.png' #开始界面图片

base = 'png\\base.png' #地面

Pipe = ( 
    'png\\pipe-green.png',
    'png\\pipe-red.png',
)#管道文件地址


def main():#游戏整合函数
    global Screen, Fpsclock#定义两个全局变量

    pygame.init()#初始化模块
    Fpsclock = pygame.time.Clock()#绑定一个时钟
    Screen = pygame.display.set_mode((screen_Width,screen_Height))#初始化屏幕
    pygame.display.set_caption("fly bird")

    #pygame 加载数据
    #加载数字
    image['number'] = (
        pygame.image.load(Figure[0]).convert_alpha(),
        pygame.image.load(Figure[1]).convert_alpha(),
        pygame.image.load(Figure[2]).convert_alpha(),
        pygame.image.load(Figure[3]).convert_alpha(),
        pygame.image.load(Figure[4]).convert_alpha(),
        pygame.image.load(Figure[5]).convert_alpha(),
        pygame.image.load(Figure[6]).convert_alpha(),
        pygame.image.load(Figure[7]).convert_alpha(),
        pygame.image.load(Figure[8]).convert_alpha(),
        pygame.image.load(Figure[9]).convert_alpha(),
    )

    #加载开始界面
    image['message'] = pygame.image.load(message).convert_alpha()
    #加载游戏结束界面
    image['overgame'] = pygame.image.load(gameover).convert_alpha()#循环加载
    #加载地面
    image['base'] = pygame.image.load(base).convert_alpha()
    #加载鸟 只有一只鸟
    image['bird'] = (
        pygame.image.load(Playbody[0]).convert_alpha(),
        pygame.image.load(Playbody[1]).convert_alpha(),
        pygame.image.load(Playbody[2]).convert_alpha(),
        )
    #加载背景,现在只有一个
    image['background'] = pygame.image.load(Sky[0]).convert()
    #加载管道 有上下管道
    image['pipe'] = (
        pygame.transform.rotate(pygame.image.load(Pipe[0]).convert_alpha(),180),
        pygame.image.load(Pipe[0]).convert_alpha(),
    )

    while True:#游戏题循环
        hit['pipe'] = (
            gethitmask(image['pipe'][0]),
            gethitmask(image['pipe'][1]),
        )
        hit['bird'] = (
            gethitmask(image['bird'][0]),
            gethitmask(image['bird'][1]),
            gethitmask(image['bird'][2]),
            )

        info_1 = welcomeMessage()
        info_2 = maingame(info_1)

        

def maingame(info):#核心函数
    
    score = 0
    Play_count = 0
    top = 0 #初始化一些变量

    #提取值
    play_style_ = info['player_style']
    player_x_ = info['player_x']
    player_y_ = info['player_y']
    base_move_max_ = info['base_move_max']
    base_x_ = info['base_x']

    #初始化鸟的速度变量
    player_speed = -7 #鸟儿的速度
    player_max_speed = 10 #鸟儿最大的掉落速度
    player_bool = False

    player_rot = 45#小鸟角度

    #生成管道
    gap_1 = getRandomPipe()
    gap_2 = getRandomPipe()
    gap_2[0]['x'] += screen_Width /2
    gap_2[1]['x'] += screen_Width /2
    gap_group = [gap_1,gap_2]#编程组

    while True:
        
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_SPACE:#监听空格键
                player_bool = True
                player_speed = -7
                player_rot = 45
            pass

        die = Collision(player_y_,Play_count,gap_group[0][0],gap_group[0][1])#判断是否撞击
        if die:
            overgame()#调用游戏结束函数
            return 0
        
        #小鸟掉落速度
        if player_speed < player_max_speed and not player_bool :
            player_speed +=1
        
        #小鸟转圈圈
        if player_rot >= -90 and not player_bool:
            player_rot -= 3
        
        player_bool = False

        top = (top + 1 )%30
        if top % 5 == 0 :
            Play_count = next(play_style_)
            
        player_y_ += player_speed #赋值小鸟速度

        base_x_ = -((-base_x_ + 4) % base_move_max_)

        Screen.blit(image['background'],(0,0))
        
        #管道的移动
        for gap in gap_group:
            gap[0]['x'] -= 4
            gap[1]['x'] -= 4
        #管道的生成
        if 0 <= gap_group[0][0]['x'] <= 4:
            gap_2 = getRandomPipe()
            gap_group.append(gap_2)
        #管道的删除
        if gap_group[0][0]['x'] < -image['pipe'][0].get_width():
            del gap_group[0]
        #管道的绘画
        for gap in gap_group:
            Screen.blit(image['pipe'][0],(gap[0]['x'],gap[0]['y']))
            Screen.blit(image['pipe'][1],(gap[1]['x'],gap[1]['y']))
        
        #积分 部分代码
        if  ( gap_group[0][0]['x'] + (image['pipe'][0].get_width() / 2) ) < player_x_ < ( gap_group[0][0]['x'] + (image['pipe'][0].get_width() / 2 + 5)):
            score += 1
        show_score(score)#调用分数


        Screen.blit(image['base'],(base_x_,base_y))
        Screen.blit(pygame.transform.rotate(image['bird'][Play_count],player_rot),(player_x_,player_y_))
        
        pygame.display.update()
        Fpsclock.tick(Fps)
    pass


def Collision(player_info_y,player_info_style,pipe_up,pipe_low):#碰撞地板
    #读取基本信息
    player_y = player_info_y
    player_x = int( screen_Width * 0.2 )
    player_style = player_info_style
    player_height = image['bird'][player_info_style].get_height()
    player_width = image['bird'][player_info_style].get_width()
    
    #判断是否碰到地面
    if player_y + player_height >= base_y:
        return True
    
    #绘画矩形
    rec_player = pygame.Rect(player_x,player_y,player_width-20,player_height-20)
    rec_pipe_up = pygame.Rect(pipe_up['x'],pipe_up['y'],image['pipe'][0].get_width(),image['pipe'][0].get_height())
    rec_pipe_low = pygame.Rect(pipe_low['x'],pipe_low['y'],image['pipe'][0].get_width(),image['pipe'][0].get_height())

    #矩形交集
    save_rec_up = rec_pipe_up.clip(rec_player)
    save_rec_low = rec_pipe_low.clip(rec_player)

    #简单的判断是否撞击
    if save_rec_low.width == 0 and save_rec_low.height == 0 and save_rec_up.width == 0 and save_rec_up.height == 0:
        return False
    
    #调用撞击函数
    uColl = Collision_pipe(player_x,player_y,player_style,save_rec_up,pipe_up,0)
    lColl = Collision_pipe(player_x,player_y,player_style,save_rec_low,pipe_low,1)

    #根据获取的返回函数判断是否撞击
    if uColl or lColl:
        return True
    return False
    pass


def Collision_pipe(player_x,player_y,player_info_style,save_rec,pipe,i):#与管道撞击
    x1 , y1 = save_rec.x - player_x , save_rec.y - player_y
    x2 , y2 = save_rec.x - pipe['x'] , save_rec.x - pipe['y']#重新构建坐标系

    x1 = int(x1)#以防万一出现float
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)


    for x in range(save_rec.width):#这部根据getmask函数 对比是否撞击
        for y in range(save_rec.height):
            if hit['bird'][player_info_style][x1+x][y1+y] and hit['pipe'][i][x2+x][y2+y]:
                return True
    return False
    pass


def show_score(score):

    score_list = [int(x) for x in list(str(score))] #数字转化为数组方便提取
    number_y = screen_Width * 0.1
    i = 0 #初始化计次函数

    for x in score_list:#计算中间位置
        i += image['number'][x].get_width()
        a = (screen_Width / 2) - (i / 2)
    
    for x in score_list:#绘制数字
        Screen.blit(image['number'][x],(a,number_y))
        a += image['number'][x].get_width()
    if score > 400:
        print('我爱你打狗一ლ(′◉❥◉｀ლ)')
    pass 


def overgame():
    while True:#暂停游戏,直到按下空格键
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_SPACE :
                return 0
    pass


def welcomeMessage():#开始界面,初始化图片位置
    data = {}#返回的数据包


    play_count = 0
    play_style = cycle([0,1,2,0])#设置小鸟不同姿势 此处修改过(0121)
    top_count = 0

    #设置各个图像位置
    #小鸟
    player_x = int( screen_Width * 0.2 )
    player_y = int( (screen_Height-image['bird'][0].get_width() ) / 2 )
    #message 开始图片
    message_x = int( (screen_Width-image['message'].get_width() ) / 2 )
    message_y = int(screen_Height * 0.12 )
    #base 地面
    basex = 0
    #basey 头部定义
    #base 移动最大距离 base宽度有限
    base_move_max = image['base'].get_width()-image['background'].get_width()
    # #欢迎界面的小鸟跳动
    # player_up_down = {'top' : 0, 'dow' : 1}


    while True:#循环监听事件
        for event in pygame.event.get():#监听用户按键

            if event.type == KEYDOWN and event.key == K_SPACE:
                data = {
                    'player_y' : player_y,
                    'player_x' : player_x,
                    'player_style' : play_style,
                    'base_x' : basex,
                    'base_move_max' : base_move_max,
                }
                return data
        
        #判断鸟儿的姿势该用哪一种
        top_count = (top_count + 1 )%30
        if top_count % 5 == 0 :
            play_count = next(play_style)


        #base移动
        basex = -((-basex + 4) % base_move_max)



        #绘画界面
        Screen.blit(image['background'],(0,0))
        Screen.blit(image['base'],(basex,base_y))
        Screen.blit(image['message'],(message_x,message_y))
        Screen.blit(image['bird'][play_count],(player_x,player_y))

        #刷新界面
        pygame.display.update()
        Fpsclock.tick(Fps)


    pass


def getRandomPipe():
    Pipe_y = random.randrange(0,int(base_y * 0.6-Pipe_size))

    Pipe_y += int(base_y * 0.2)
    Pipe_height = image['pipe'][0].get_height()
    Pipe_x = screen_Width + 1
    data = [
        {'x' : Pipe_x, 'y' : Pipe_y - Pipe_height},#上方管道
        {'x' : Pipe_x, 'y' : Pipe_y + Pipe_size},#下方管道
    ]
    
    return data
    pass


def gethitmask(image):
    mask=[]#边界
    for x in range(image.get_width()):
        mask.append([x])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

if __name__ == "__main__":
    main()
    pass