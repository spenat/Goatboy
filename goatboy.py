#!/usr/bin/python
#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-#
#					    #
#	Goatboy : The jumpin' jackass	    #
#					    #
#		Writen by Mikael	    #
#		hejhej			    #
#					    #
#-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-#
import pygame, sys, os, string, random
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT, RLEACCEL
pygame.init()
window = pygame.display.set_mode(pygame.display.list_modes()[0]) # Fonsterstorlek
pygame.display.set_caption('Goatboy: the hoorned avanger') #Fonstertitel
screen = pygame.display.get_surface() # Skarmyta
back_file_name = os.path.join("data","background.bmp") # bakgrundsfilnamnsokvag
back_surface = pygame.image.load(back_file_name)
pygame.display.flip()
clock = pygame.time.Clock()
background = pygame.Surface(screen.get_size())
background.blit(back_surface,(0,0))
scrollx = 0
scrolly = 0
scoore = 0
scooresurface = pygame.Surface((50,25))

def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print "Cannot load image:", name
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

def loadvisible():
	global allsprites
	allsprites = pygame.sprite.RenderPlain(sum([map.shots,map.blocks,map.enemies,map.doors,[leveleditor,thor]],[])) # Alla sprites som ska ritas

def reset():   # Satt alla varden till utgangsvarden
	global scrollx,scrolly,thor,scoore,map,allsprites
	scrollx,scrolly,thor.dx,thor.ddx,thor.dy,scoore = 0,0,0,0,0,0
	map.reset()
	thor.setposition(300,150)
	background.blit(back_surface,(0,0))
	loadvisible()

class GameObject(pygame.sprite.Sprite):
	x,y = 0,0
	filename = 'door.bmp'
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(self.filename,-1)
	def setposition(self,x,y): # Satt blockets startposition
		self.x, self.y = x,y
	def setimage(self,imagename,colorkey):
		self.filename = imagename
		self.image, self.rect = load_image(imagename,colorkey)


# -- This is Goatboy -- #

class Goatboy(GameObject):
	x=300
	y=150
	onGround = True    # Star goatboy pa marken?
	turnedRight = True # Ar goatboy vand at hoger?
	rightDown = False  # Ar hogerknappen nedtryckt?
	leftDown = False   # Ar vansterknappen nedtryckt?
	maxspeed = 10 # maxhastighet
	jumpheight = 20 # Hopphojd
	topscroll = 300
	bottomscroll = 400
	leftscroll = 400
	rightscroll = 600
	shooting = False
	weapon = 1
	dx = 0	# Goatboys momentana hastighet i x-led
	dy = 0	# -"- y-led
	ddx = 0 # Goatboys acceleration i x-led
	boneRect = pygame.Rect(x+30,y+74,22,1)	# Bonerect is his feets that are collition tested againts ground later on
	def __init__(self):			# Initiera goatboy
		pygame.sprite.Sprite.__init__(self) 			# Ladda en sprite
		self.image, self.rect = load_image('goatboy.bmp',-1) 	# Ladda bilden pa goatboy
		screen = pygame.display.get_surface()			# Lagg skarmytan i screen
	def update(self):			#  update() updates goatboy every loop
		global scrollx,scrolly,reset				
		self.x = self.x + self.dx	# Flytta goatboy i hans horisontella hastighet
		if self.dx < self.maxspeed and self.dx > -self.maxspeed: # Om goatboys maxhastiget inte ar mott,
			self.dx = self.dx + self.ddx			 # oka hans hastighet med hans acceleration
		self.y = self.y + self.dy	# Flytta goatboy i hans vertikala hastighet
		if self.dy > 100:		# Om goatboy faller fortare an 100
			reset()			# Reset game
		if self.shooting:
			if random.randint(1,2) == 2:
				shot = Shot()
				shot.limit = self.weapon
				shot.dy = random.randint(-self.weapon,self.weapon)
				if shot.dy < 0:
					shot.ddy = -1
				else:
					shot.ddy = 1
				map.addShot(shot)
			loadvisible()
		# -- This is the frame of goatboys scroll :
		if self.y > self.bottomscroll:
			scrolly = scrolly + (self.bottomscroll - self.y )
			self.y = self.bottomscroll
		elif self.y < self.topscroll:
			scrolly = scrolly - (self.y - self.topscroll)
			self.y = self.topscroll
		if self.x > self.rightscroll:
			scrollx = scrollx + (self.rightscroll - self.x)
			self.x = self.rightscroll
		elif self.x < self.leftscroll:
			scrollx = scrollx - (self.x - self.leftscroll)
			self.x = self.leftscroll
		# If goatboy doesn't stand on the ground, he will fall down
		if not self.onGround:
			self.dy = self.dy + 1
		self.rect.topleft = self.x, self.y # Satt goatboys sprite till hans nya koordinater
		self.boneRect = pygame.Rect(self.x+30,self.y+74,22,1)	# Flytta fotterna efter de nya koordinaterna
	def move_right(self):
		self.ddx=1 # Nar goatboy flyttar at hoger ar hans acceleration positiv
		self.rightDown=True 	# Hogerknappen ar nedtryckt
		if not self.turnedRight:					# Om goatboy inte ar vand at hoger, 
			self.image = pygame.transform.flip(self.image,1,0) 	# vand pa hans bild
			self.turnedRight = True					# och sag att han e vand at hoger
	def move_left(self):
		self.ddx=-1 		# Nar goatboy flyttar at vanster ar hans acceleration negativ
		self.leftDown=True 	# vansterknappen ar nedtryckt
		if self.turnedRight: 	# Om goatboy ar vand at hoger,
			self.image = pygame.transform.flip(self.image,1,0) # vand pa hans bild
			self.turnedRight = False	# goatboy ar inte langre vand at hoger
	def move_up(self):
		if self.onGround: 			# Om goatboy star pa marken,
			self.dy=self.dy-self.jumpheight # Hoppa!
			self.onGround = False 		# Goatboy star inte langre pa marken
	def move_down(self):
		self.dy=self.dy+1
	def stop(self):				      # stop() kallas da man slapper hoger eller vanster.
		if self.rightDown and self.ddx == -1: # Om goatboy ar pa vag at vanster men trycker at hoger,
			self.dx = self.dx / 2	      # halvera goatboys hastighet.
			self.rightDown = False	      # Goatboy slutar trycka
		elif self.leftDown and self.ddx == 1: # Vice versa.
			self.dx = self.dx / 2
			self.leftDown = False
		else:
			self.dx = 0	# Goatboys hastighet ar noll
			self.ddx = 0	# Goatboys acceleration ar noll
			self.rightDown = False # hoger ar inte nedtryckt
			self.leftDown = False  # vanster ar inte nedtryckt
	def get_x(self):
		return self.x
	def changeweapon(self):
		self.weapon=(self.weapon+2)%16
	def get_y(self):
		return self.y

# -- Block-classen -- #

class Block(GameObject):
	x = 0
	y = 0
	rightlimit = 1000000	# Default-varde for blockets hogra vandpunkt da det ar rorligt
	leftlimit = -1000000	# -"- vanstra -"-
	dx = 0
	filename = 'blockgrass.bmp'
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(self.filename,-1) # Ladda default-bild
		self.dx = 0
	def update(self):
		global scrollx,scrolly,scoore
		self.x = self.x + self.dx
		if self.rect.w + self.x > self.rightlimit or self.x < self.leftlimit: # Om blocket ar utanfor vandpunkterna,
			self.dx = -self.dx					      # byt hall.
		#if self.rect.top > 600:			    # Om blocket kommer nedanfor skarmen,
		#	self.y = self.y - self.rect.h - 600 # flytta upp den ovanfor skarmen.
		#	scoore = scoore + 1
		#	print scoore
		self.rect.topleft = self.x + scrollx, self.y + scrolly # Flytta blockets sprite i forhallande till scrollen
	def setdx(self,dx):
		self.dx = dx # Blockets horisontella hastighet
	def setlimits(self,leftlimit,rightlimit): # Satt blockets vandpunkter
		self.leftlimit = leftlimit
		self.rightlimit = rightlimit

# -- Flamenemy-classen -- #

class Flamenemy(GameObject):
	x = 0
	y = 0
	kind = 0
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('flamenemy.bmp',-1) # Ladda default-bild
		self.dx,self.dy = random.randint(-10,10),random.randint(-5,5)
		self.ddx,self.ddy = 1,-1
	def update(self):
		global scrollx,scrolly,scoore
		self.x = self.x + self.dx
		self.dx = self.dx + self.ddx
		self.y = self.y + self.dy
		self.dy = self.dy + self.ddy
		if self.dx > 20 or self.dx < -20: # Om blocket ar utanfor vandpunkterna,
			self.ddx = -self.ddx
			self.image = pygame.transform.flip(self.image,1,0)			      # byt hall.
		if self.dy > 10 or self.dy < -10: # Om blocket ar utanfor vandpunkterna,
			self.ddy = -self.ddy	
		#if self.rect.top > 600:			    # Om blocket kommer nedanfor skarmen,
		#	self.y = self.y - self.rect.h - 600 # flytta upp den ovanfor skarmen.
		#	scoore = scoore + 1
		#	print scoore
		self.rect.topleft = self.x + scrollx, self.y + scrolly # Flytta blockets sprite i forhallande till scrollen
	def reset(self):
		self.dx,self.dy,self.ddx,self.ddy = random.randint(-10,10),random.randint(-5,5), 1,-1 #random.randint(-1,1),random.randint(-1,1)
	def die(self):
		global scoore
		scoore = scoore + 1
		map.enemies.remove(self)

# -- Flameboy -- # 

class Flameboy(GameObject):
	kind = 1
	filename = 'flameboy.bmp'
	onGround = False
	range = 400
	life = 20
	limit = random.randint(4,7)
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(self.filename,-1) 
		self.dx,self.ddx,self.dy,self.ddy = 1,-1,1,0
	def update(self):
		global scrollx, scrolly
		self.x = self.x + self.dx
		self.y = self.y + self.dy
		self.dx = self.dx + self.ddx
		if not self.onGround:
			self.dy = self.dy + 1
		if self.dx > self.limit or self.dx < -self.limit:
			self.ddx=-self.ddx
			self.limit = random.randint(4,7)
			if self.onGround:
				self.dy = -random.randint(5,15)
				if self.x + scrollx < thor.x + self.range and self.x + scrollx > thor.x - self.range and self.y + scrolly < thor.y + self.range and self.y + scrolly > thor.y - self.range:
					enemy = Flamenemy()
					enemy.setposition(self.x - 100,self.y)
					map.addEnemy(enemy)
					loadvisible()
		if self.dy > 100:
			print "flameboy fell down"
			map.enemies.remove(self)
			loadvisible()
		if self.rect.collidelist(map.blocks) != -1:
			if self.dy > 0:
				self.dy,self.ddy = 0,0
				self.onGround = True
		else:
			self.onGround = False
		self.rect.topleft = self.x + scrollx, self.y + scrolly
	def reset(self):
		self.dx,self.dy,self.ddx,self.ddy = 1,-1,1,0
		self.onGround = False
	def die(self):
		global scoore
		self.life = self.life - 1
		if self.life < 1:
			scoore = scoore + 1
			map.enemies.remove(self)
			loadvisible()
		else:
			self.dy = -10

# -- Map-classen -- # 

class Map():
	blocks = []
	enemies = []
	doors = []
	shots = []
	initenemies = []
	initblocks = []
	initdoors = []
	def addBlock(self, block):
		self.blocks.append(block)
		self.initblocks.append([block.x,block.y,block.leftlimit,block.rightlimit,block.dx])
	def addEnemy(self, enemy):
		self.enemies.append(enemy)
		self.initenemies.append([enemy.x,enemy.y,enemy.kind])
	def addDoor(self,door):
		self.doors.append(door)
		self.initdoors.append([door.x,door.y,door.mapname])
	def addShot(self,shot):
		self.shots.append(shot)
	def update(self):
		for block in self.blocks:
			block.update()
		for enemy in self.enemies:
			enemy.update()
		for door in self.doors:
			door.update()
		for shot in self.shots:
			shot.update()
		if pygame.font:
			font = pygame.font.Font(None, 36)
			text = font.render(str(scoore), 1, (255, 5, 5))
			textpos = text.get_rect()
			textpos.centerx = background.get_rect().centerx
			background.blit(scooresurface,textpos)
			background.blit(text, textpos)
	def reset(self):
		for index,block in enumerate(self.blocks):
			block.setposition(self.initblocks[index][0],self.initblocks[index][1])
			block.setlimits(self.initblocks[index][2],self.initblocks[index][3])
			block.setdx(self.initblocks[index][4])
		for index,enemy in enumerate(self.enemies):
			enemy.setposition(self.initenemies[index][0],self.initenemies[index][1])
			enemy.reset()
		for index,door in enumerate(self.doors):	
			door.setposition(int(self.initdoors[index][0]),int(self.initdoors[index][1]))
			#door.mapname = initdoors[index][2]
		self.shots = []
	def savemap(self,filename):
		f = open(filename,'w')
		for index,block in enumerate(self.blocks):
			f.write(string.join(["block",str(self.initblocks[index][0]),str(self.initblocks[index][1]),str(self.initblocks[index][2]),str(self.initblocks[index][3]),str(self.initblocks[index][4]),block.filename], ':'))
			f.write('\n')
		for index in enumerate(self.enemies):
			f.write(string.join(["flamenemy",str(self.initenemies[index][0]),str(self.initenemies[index][1]),str(self.initenemies[index][2])], ':'))
			f.write('\n')
		for index in enumerate(self.doors):
			f.write(string.join(["door",str(self.initdoors[index][0]),str(self.initdoors[index][1]),self.initdoors[index][2]], ':'))
			f.write('\n')
	def loadmap(self,filename):
		self.blocks = []
		self.enemies = []
		self.doors = []
		self.initblocks = []
		self.initenemies = []
		self.initdoors = []
		f = open(os.path.join('data',filename),'r')
		for line in f:
			entity  = string.split(line,':')
			if entity[0] == 'block':
				block = Block()
				block.setposition(int(entity[1]),int(entity[2]))
				block.setlimits(int(entity[3]),int(entity[4]))
				block.setdx(int(entity[5]))
				if string.strip(entity[6]) == 'blockgrass.bmp':
					block.setimage(string.strip(entity[6]),-1)
				else:
					block.setimage(string.strip(entity[6]),None)
				self.addBlock(block)
			elif entity[0] == 'flamenemy':
				if len(entity) > 3:
					if int(entity[3]) == 0:
						enemy = Flamenemy()
					elif int(entity[3]) == 1:
						enemy  = Flameboy()
				else:
					enemy = Flamenemy()
				enemy.setposition(int(entity[1]),int(entity[2]))
				self.addEnemy(enemy)
			elif entity[0] == 'door':
				door = Door()
				door.setposition(int(entity[1]),int(entity[2]))
				door.mapname = string.strip(entity[3])
				self.addDoor(door)

# -- Leveleditor -- #

class LevelEditor(GameObject):
	entity = 0
	images = ['blockgrass.bmp','block.bmp','flamenemy.bmp','door.bmp','flameboy.bmp']
	filename = images[0]
	def createGO(self):
		if self.entity == 0:
			block = Block()
			block.setposition(self.x - scrollx,self.y - scrolly)
			map.addBlock(block)	
		elif self.entity == 1:
			block = Block()
			block.setposition(self.x - scrollx,self.y - scrolly)
			block.setimage(self.images[self.entity],None)
			map.addBlock(block)
		elif self.entity == 2:
			enemy = Flamenemy()
			enemy.setposition(self.x - scrollx,self.y - scrolly)
			map.addEnemy(enemy)
		elif self.entity == 3:
			door = Door()
			door.setposition(self.x - scrollx,self.y - scrolly)
			map.addDoor(door)
		elif self.entity == 4:
			flameboy = Flameboy()
			flameboy.setposition(self.x - scrollx,self.y - scrolly)
			map.addEnemy(flameboy)
		loadvisible()
	def changeGO(self):
		self.entity = (self.entity + 1)%5
		if self.entity == 0 or self.entity == 2 or self.entity == 3 or self.entity == 4: # For bilderna som vill ha en transparentcolor
			self.setimage(self.images[self.entity],-1)
		else: 							     # For bilderna som inte vill
			self.setimage(self.images[self.entity],None)
	def update(self):
		self.rect.topleft = self.x,self.y

# -- Door class -- # 

class Door(GameObject):
	numofmaps = 18
	filename = 'door.bmp'
	mapname = 'map' + str(numofmaps) + '.map'
	def update(self):
		self.rect.topleft = self.x + scrollx, self.y + scrolly
	def open(self):
		global map,mapname
		map = Map()
		map.loadmap(self.mapname)
		mapname = self.mapname
		reset()
		loadvisible()

# -- Shot classen .. d e ett skott -- #

class Shot(GameObject):
	filenames = ['shot.bmp','oldshot.bmp']
	images = []
	imagenr = 0
	range = 400
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		for filename in enumerate(self.filenames):
			image, self.rect = load_image(filename,-1)
			self.images.append(image)
		self.image = self.images[0]
		self.x,self.y = thor.x - scrollx,thor.y + 30 - scrolly
		self.dy,self.ddy = random.randint(-6,6),random.randint(-1,1)
		if thor.turnedRight:
			self.dx = 15
			self.x  = self.x + 40
		else:
			self.dx = -15
	def update(self):
		self.x = self.x + self.dx
		self.y = self.y + self.dy
		self.dy = self.dy + self.ddy
		self.imagenr = (self.imagenr + 1)%len(self.filenames)
		self.image = self.images[self.imagenr]	
		if self.dy > self.limit or self.dy < -self.limit:
			
			self.ddy=-self.ddy
		self.rect.topleft = self.x + scrollx,self.y + scrolly
		if self.x + scrollx > thor.x + self.range  or self.x + scrollx < thor.x - self.range:
			map.shots.remove(self) # ta bort skottet fran listan i kartan o hopppas garbagecollectorn fixar biffen
			loadvisible()
		elif self.rect.collidelist(map.enemies) != -1:
			map.shots.remove(self)
			map.enemies[self.rect.collidelist(map.enemies)].die()
			loadvisible()
		
# -- Alla objekt och deras utgangsvarden :

leveleditor = LevelEditor()
thor = Goatboy() # skapa ett goatboy-objekt =)
map = Map()	 # skapa ett map-objekt
mapname = "map2.map"
map.loadmap(mapname) # ladda banan fran fil
loadvisible()

# -- Input - hanteraren :

def input(events):
	global thor
	for event in events:
		if event.type == QUIT:
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == 275 or event.key == 100: 		# Tryck hoger lr d
				thor.move_right()
			elif event.key == 276 or event.key == 97:		# Tryck vanster lr a
				thor.move_left()
			elif event.key == 274:					# Tryck ner
				thor.move_down()
			elif event.key == 273 or event.key == 119:		# Tryck upp lr w
				thor.move_up()
			elif event.key == 120:
				thor.changeweapon()
			elif event.key == 27:		# Tryck escape
				sys.exit()
			elif event.key == 112:		# Tryck p for save current map
				map.savemap(os.path.join('data',mapname))
			elif event.key == 32 or event.key == 102:		# Tryck space for SKJUT!
				thor.shooting = True
			else:
				print event
		elif event.type == KEYUP:
			if event.key == 275 or event.key == 276 or event.key == 100 or event.key == 97: # Lyft hoger eller vanster
				thor.stop()
			elif event.key == 32 or event.key == 102:
				thor.shooting = False
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 1: 		# Tryck vanster musknapp for skapa valt objekt
				leveleditor.createGO()
			elif event.button == 3:		# Tryck hoger  mosknapp for vaxla objekt
				leveleditor.changeGO()
		elif event.type == MOUSEMOTION:
				leveleditor.setposition(event.pos[0],event.pos[1]) # muspekaren flyttar leveleditorn
		else:
			print event

# -- The Main Loop -- #

while True:
	clock.tick(60) 					# Delay
	screen.blit(background,(0,0)) 			# Rita bakgrunden
	if thor.boneRect.collidelist(map.blocks) != -1: # Testa goatboys ben mot alla block
		if thor.dy > 0: 			# Om man nuddar ett block pa vagen ner,
			thor.dy = 0 			# faller man inte langre nedat
			thor.onGround = True 		# och har fotterna pa fast mark.
	else:
		thor.onGround = False # nuddar man inget block, star man inte pa marken
	if thor.rect.collidelist(map.enemies) != -1:
		reset()
	elif thor.rect.collidelist(map.doors) != -1:
		map.doors[thor.rect.collidelist(map.doors)].open() # Oppna dorren
		reset()
	thor.update()
	leveleditor.update()
	map.update()
	if pygame.event.peek(): # Titta om det finns en event i event-kon
		input(pygame.event.get()) # Om det finns skicka event till input()
	allsprites.draw(screen) # Rita alla sprites
	pygame.display.flip()   # vand fram dubbelbufferten
