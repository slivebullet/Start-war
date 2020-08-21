#-------------------------------<引入模块>---------------
import pygame
import random
from os import path
from easygui import *


#-------------------------<定义游戏边框的全局常量>-----------------------
WIDTH=900
HEIGHT=700
supply=1
game_move=True
WIN=1500

#----------------------<定义玩家的类>-----------------------------------
class Player(pygame.sprite.Sprite):

#--------------------------<初始化玩家的性质函数>----------------------
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image= pygame.transform.rotate(player_img,90)
		self.image=pygame.transform.scale(self.image,(60,50))
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()
		self.rect.centerx=WIDTH/2
		self.rect.bottom=HEIGHT
		self.hp=100
		self.lives=2
		self.score=0

#----------------------------<玩家的坐标函数>--------------------
	def update(self):
		keys=pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.rect.x-=10
		if keys[pygame.K_RIGHT]:
			self.rect.x+=10
		if keys[pygame.K_UP]:
			self.rect.y-=5
		if keys[pygame.K_DOWN]:
			self.rect.y+=5

#----------------------<游戏边框的边界设定检测>-------------------
		

		if self.rect.right>WIDTH:
			self.rect.right=WIDTH

		if self.rect.left<0:
			self.rect.left=0

		if self.rect.top<0:
			self.rect.top=0
		
		if self.rect.bottom>HEIGHT:
			self.rect.bottom=HEIGHT

class Boss(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=boss_img
		self.image=pygame.transform.scale(self.image,(350,210))
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()
		self.rect.centerx=WIDTH/2
		self.rect.top=0
		self.hp=400
		self.vx=2
		self.vy=2


	def update(self):
		self.rect.x+=self.vx
		self.rect.y+=self.vy
		if self.rect.right>WIDTH:
			self.rect.right=WIDTH
			self.vx=-2
		if self.rect.left<0:
			self.rect.left=0
			self.vx=2
		if self.rect.top<0:
			self.rect.top=0
			self.vy=2
		if self.rect.bottom>HEIGHT:
			self.rect.bottom=HEIGHT
			self.vy=-2

					
#-----------------------<定义敌机的类>--------------------------
class Enemy(pygame.sprite.Sprite):

#-------------------------------<同上一样是初始化>----------------
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=enemy_img
		self.image=pygame.transform.scale(self.image,(random.randint(40,70),random.randint(35,90)))
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()
		##----------------------<引入随机数，确保敌机出现的位置>---------------
		self.rect.x=random.randint(0,WIDTH-self.rect.w)

#--------------------------<控制敌人水平和垂直方向的速度变化>---------------
		self.vx=random.randint(-2,2)
		self.vy=random.randint(2,6)


#-------------------------<敌机出现的坐标>----------------------
	def update(self):
		self.rect.y+=self.vy
		self.rect.x+=self.vx


#------------------------<子弹的类>-------------------
class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=bullet_img
		self.image=pygame.transform.scale(self.image,(10,10))
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()

		self.rect.centerx=x
		self.rect.centery=y 


	def update(self):
		self.rect.y-=12

#----------------------<爆炸特效的类>--------------------------
class Explosion(pygame.sprite.Sprite):
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		self.image=explosions_store[0]
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.image.set_colorkey((0,0,0))
		self.number=0
#---------------------<爆炸特效的更新函数>-------------------
	def update(self):
		if self.number<len(explosions_store):
			self.image=explosions_store[self.number]
			self.image=pygame.transform.scale(self.image,(60,60))
			self.image.set_colorkey((0,0,0))
			self.number+=1
		else:
			self.kill()

class Watch(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=killer_img
		self.image=pygame.transform.scale(self.image,(40,60))
		self.rect=self.image.get_rect()
		self.image.set_colorkey((0,0,0))
		self.rect.x=random.randint(0,WIDTH-self.rect.w)
		self.rect.y=0


	def update(self):
		self.rect.y+=2

class Space(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=space_img
		self.image= pygame.transform.rotate(space_img,45)
		self.image=pygame.transform.scale(self.image,(120,140))
		self.rect=self.image.get_rect()
		self.image.set_colorkey((0,0,0))
		self.rect.y=random.randint(0,HEIGHT-self.rect.h)
		self.rect.x=WIDTH
     
		self.v1=3
		self.v2=4


	def update(self):
		self.rect.x-=7
		self.rect.y+=2


def user_display(): 
	pygame.draw.rect(screen,(0,255,0),(WIDTH/2-40,HEIGHT-20,player.hp,15))
	pygame.draw.rect(screen,(255,255,255),(WIDTH/2-40,HEIGHT-20,100,15),2)

	img_rect=player_small_img.get_rect()
	img_rect.x=WIDTH-60
	img_rect.y=HEIGHT-60
	for i in range(player.lives):
		screen.blit(player_small_img,img_rect)
		img_rect.right=img_rect.x-20

def boss_display():
	pygame.draw.rect(screen,(255,255,0),(WIDTH/2-150,10,boss.hp,15))
	pygame.draw.rect(screen,(255,255,255),(WIDTH/2-150,10,400,15),2)

	
#-----------------------------<游戏边框的基本设置>----------------
pygame.mixer.init()
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("MY Dream----MY GAME")
clock=pygame.time.Clock()       #游戏帧数的设置

#---------------------<游戏声音模块的载入>-----------------------------
sound_dir=path.join(path.dirname(__file__),'sound')
shoot_sound=pygame.mixer.Sound(path.join(sound_dir,'Laser_Shoot4.wav'))

explosion_sound=pygame.mixer.Sound(path.join(sound_dir,'Explosion21.wav'))

pygame.mixer.music.load(path.join(sound_dir,'Mark T - PLAYERUNKNOWN’S BATTLEGROUNDS (耳机试听版).wav')) 


#-----------------------<游戏图像的外部导入>----------------------
img_dir=path.join(path.dirname(__file__),'img')

boss_dir=path.join(img_dir,'BOSS.png')
boss_img=pygame.image.load(boss_dir).convert()

killer_dir=path.join(img_dir,'spaceShips_008.png')
killer_img=pygame.image.load(killer_dir).convert()

background_dir=path.join(img_dir,'background.jpg')
background_img=pygame.image.load(background_dir).convert()
background_rect=background_img.get_rect()

space_dir=path.join(img_dir,'enemy_shoots.png')
space_img=pygame.image.load(space_dir).convert()

player_dir=path.join(img_dir,'spaceship001.png')
player_img=pygame.image.load(player_dir).convert()

player_small_img=pygame.transform.scale(player_img,(60,60))
player_small_img.set_colorkey((0,0,0))
player_small_img= pygame.transform.rotate(player_small_img,90)

enemy_dir=path.join(img_dir,'spaceMeteors_001.png')
enemy_img=pygame.image.load(enemy_dir).convert()

bullet_dir=path.join(img_dir,'spaceMissiles_018.png')
bullet_img=pygame.image.load(bullet_dir).convert()

explosions_store=[]
for i in range(9):
	explosions_dir=path.join(img_dir,'regularExplosion0{}.png'.format(i))
	explosions_img=pygame.image.load(explosions_dir).convert()
	explosions_store.append(explosions_img)

#--------------------------------<类的引用>----------------------
player=Player()     
boss=Boss()

#-----------<精灵群组的引用>--------------------------------------
enemys=pygame.sprite.Group()
bullets=pygame.sprite.Group()
explosions=pygame.sprite.Group()
watchs=pygame.sprite.Group()
spaces=pygame.sprite.Group()
#------------------<游戏的主循环>---------------------------------
msgbox("              Welcome to use MY GAME\n           游戏设计者：彭鑫")
game_over=False
pygame.mixer.music.play(loops=-1)
while not game_over:
	clock.tick(60)
	screen.fill((255,255,255))
	supply+=1
	if supply%20==0:
	    enemy=Enemy()
	    enemys.add(enemy)
	if supply%50==0:
		watch=Watch()
		watchs.add(watch)
	if supply%60==0:
		space=Space()
		spaces.add(space)
	event_list=pygame.event.get()
	for event in event_list:
		if event.type==pygame.QUIT:              #确保玩家可以顺利的退出游戏
			game_over=True
		if event.type==pygame.KEYDOWN:           
			if event.key==pygame.K_ESCAPE:       #同上
				game_over=True
			if event.key==pygame.K_SPACE:        #规定空格键发射子弹
				bullet=Bullet(player.rect.centerx,player.rect.centery)
				bullets.add(bullet)
				shoot_sound.play()
			
#-----------------------游戏的显示模块>---------------------------
	screen.blit(background_img,background_rect)
    
	enemys.update()
	enemys.draw(screen)

	if player.score>=WIN:
		boss.update()
		screen.blit(boss.image,(boss.rect.x,boss.rect.y))
		boss_display()

	spaces.update()
	spaces.draw(screen)

	watchs.update()
	watchs.draw(screen)

	player.update()
	bullets.update()

	bullets.draw(screen)
	explosions.update()
	explosions.draw(screen)

	user_display()
	
	screen.blit(player.image,(player.rect.x,player.rect.y))

#---------------------<判断是否相撞>--------------------------------	
	death=pygame.sprite.spritecollide(player,enemys,True)
	if death:
		player.hp-=45
	if player.hp<=0:
		player.lives-=1
		player.hp=100
	if player.lives<0:
		game_over=True
		msgbox("                YOU LOST THE GAME")

	work=pygame.sprite.collide_rect(player,boss)
	if work:
		boss.hp-=0.5
		player.hp-=1

	reserach=pygame.sprite.spritecollide(player,watchs,True)
	if reserach:
		player.hp-=35

	boyfriend=pygame.sprite.spritecollide(player,spaces,True)
	if boyfriend:
		player.hp-=70
 
 #----<判断子弹和障碍物是否相撞模块，相撞则双方都进行删除>-------
	hits=pygame.sprite.groupcollide(bullets,enemys,True,True)
	if hits:
		explosion_sound.play()
		explosion=Explosion(bullet.rect.center) #若击中则在精灵组里面增加一个精灵
		explosions.add(explosion)
		player.score+=50

	test=pygame.sprite.groupcollide(bullets,watchs,True,True)
	if test:
		explosion_sound.play()
		explosion=Explosion(bullet.rect.center)
		explosions.add(explosion)
		player.score+=70

	girlfriend=pygame.sprite.groupcollide(bullets,spaces,True,True)
	if girlfriend:
		explosion_sound.play()
		explosion=Explosion(bullet.rect.center)
		explosions.add(explosion)
		player.score+=100

	school=pygame.sprite.spritecollide(boss,bullets,False)
	if school:
		boss.hp-=0.1
		if boss.hp<=0:
			game_over=True
			msgbox("                YOU WIN THE GAME")



#----------------------------------------<游戏的刷新画面>-----------
	pygame.display.flip()