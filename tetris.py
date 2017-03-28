#!/usr/bin/env python2
import random, time, pygame, sys
from pygame.locals import *
from random import randrange as rand

Size =20
Columns =32
tuples =30
maxfps =30
colors=[(0,0,0),(60,60,0),(0,60,60),(60,0,60),(100,200,100),(35,35,35),(100,50,70),(150,200,200),(10,20,30)]
k=0
GAME_dikhawats = [ 
		[[1, 1, 1], 
			[0, 1, 0]],

		[[0, 2, 2], 
			[2, 2, 0]],

		[[3, 3, 0], 
			[0, 3, 3]],

		[[4, 0, 0], 
			[4, 4, 4]],

		[[0, 0, 5], 
			[5, 5, 5]],

		[[6, 6, 6, 6]],

		[[7, 7], 
			[7, 7]] 
		]
global new_s
global nAREA
def CHECCK_COL(AREA, dikhawat, off_x,off_y):
	#off_x, off_y = offset
	for cy, RO_W in enumerate(dikhawat):
		for cx, cell in enumerate(RO_W):
			try:
				if cell and AREA[ cy + off_y ][ cx + off_x ]:
					return True
			except IndexError:
				return True
	return False

def join_matrixes(Matrices1,Matrices2,a,b):
	off_x=a
	off_y = b
	for y,RO_W in enumerate(Matrices2):
		for x,val in enumerate(RO_W):
			Matrices1[y+off_y-1][x+off_x] += val
	return Matrices1
a=0
class Block(object):
	global nAREA
	def __init__(self,dikhawat,AREA,RO_W,a):
		self.dikhawat=dikhawat
		self.AREA=AREA
		self.RO_W=RO_W
		#self.Matrices1=Matrices1
		#self.Matrices2=Matrices2
		#self.Matrices2_off=Matrices2_off
		if a==1:
			self.rotate_clockwise()
		elif a==2:
			self.remove_RO_W()
	def rotate_clockwise(self):
		global new_s
		new_s=[ [ self.dikhawat[y][x]
				for y in xrange(len(self.dikhawat)) ]
			for x in xrange(len(self.dikhawat[0]) - 1, -1, -1) ]


	def remove_RO_W(self):
		global nAREA
		del self.AREA[self.RO_W]
		#return [[0 for i in xrange(Columns)]] + self.AREA
		nAREA = [[0 for i in xrange(Columns)]] + self.AREA
		
	

#Block.Block()
class Gameplay(Block):
	#global new_s
	def __init__(self):
		pygame.init()
		pygame.key.set_repeat(250,25)
		self.HEIGHT=Size*tuples
		self.WIDTH=Size*(Columns+10)
		self.ROWLIMIT=Size*Columns
		self.default_font =  pygame.font.Font(
			pygame.font.get_default_font(), 12)
		self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in xrange(Columns)] for y in xrange(tuples)]
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
	#	pygame.event.set_blocked(pygame.MOUSEMOTION) # We do not need
		                                             # mouse movement
		                                             # events, so we
		                                             # block them.
		self.next_Designs = GAME_dikhawats[rand(len(GAME_dikhawats))]
		self.gameover=False
		self.Paused=False
		self.game()
		
	def new_AREA(self):
		AREA = [ [ 0 for x in xrange(Columns) ]
				for y in xrange(tuples) ]
		AREA += [[ 1 for x in xrange(Columns)]]
		return AREA

	def game(self):
		self.AREA=self.new_AREA()
		self.new_Designs()
		self.level=1
		self.score=0
		self.lines=0
		pygame.time.set_timer(pygame.USEREVENT+1, 1000)
	def new_Designs(self):
		self.Designs = self.next_Designs[:]
		self.next_Designs = GAME_dikhawats[rand(len(GAME_dikhawats))]
		self.Designs_x = int(Columns / 2 - len(self.Designs[0])/2)
		self.Designs_y = 0
		
		if CHECCK_COL(self.AREA,
		                   self.Designs,
		                   self.Designs_x, self.Designs_y):
			self.gameover = True


	def MESSAGE(self, msg, topleft):
		x,y = topleft
		for line in msg.splitlines():
			self.screen.blit(
				self.default_font.render(
					line,
					False,
					(255,255,255),
					(0,0,0)),
				(x,y))
			y+=14
	def center_msg(self, msg):
		for i, line in enumerate(msg.splitlines()):
			msg_image =  self.default_font.render(line, False,
				(255,255,255), (0,0,0))
		
			msgim_center_x, msgim_center_y = msg_image.get_size()
			msgim_center_x //= 2
			msgim_center_y //= 2
		
			self.screen.blit(msg_image, (
			  self.WIDTH // 2-msgim_center_x,
			  self.HEIGHT // 2-msgim_center_y+i*22))
	
	def draw_matrix(self, matrix, offset):
		off_x, off_y  = offset
		for y, RO_W in enumerate(matrix):
			for x, val in enumerate(RO_W):
				if val:
					pygame.draw.rect(
						self.screen,
						colors[val],
						pygame.Rect(
							(off_x+x) *
							  Size,
							(off_y+y) *
							  Size, 
							Size,
							Size),0)
	
	def addlines(self, n):
		linescores = 100
		self.lines += n
		self.score += linescores * self.level
		if self.lines >= self.level*6:
			self.level += 1
			newdelay = 1000-50*(self.level-1)
			newdelay = 100 if newdelay < 100 else newdelay
			pygame.time.set_timer(pygame.USEREVENT+1, newdelay)
	
	def move(self, delta_x):
		if not self.gameover and not self.paused:
			new_x = self.Designs_x + delta_x
			if new_x < 0:
				new_x = 0
			if new_x > Columns - len(self.Designs[0]):
				new_x = Columns - len(self.Designs[0])
			if not CHECCK_COL(self.AREA,
			                       self.Designs,
			                       new_x, self.Designs_y):
				self.Designs_x = new_x
	def quit(self):
		self.center_msg("Exiting...")
		pygame.display.update()
		sys.exit()
	
	def drop(self, manual):
		global nAREA
		if not self.gameover and not self.paused:
			#self.score += 1 if manual else 0
			self.Designs_y += 1
			if CHECCK_COL(self.AREA,self.Designs,self.Designs_x, self.Designs_y):
				#	Bl=Block.__init__(self,self.Designs,self.AREA,k,self.AREA,self.Designs,(sel.Designs_x,self.Designs_y))
				self.AREA = join_matrixes(
						self.AREA,
						 self.Designs,
						 self.Designs_x, self.Designs_y)
				#self.AREA=Bl.join_matrixes()
				#self.AREA=
				self.score += 10
				self.new_Designs()
				cleared_tuples = 0
				while True:
					for i, RO_W in enumerate(self.AREA[:-1]):
						if 0 not in RO_W:
							Bl=Block.__init__(self,self.Designs,self.AREA,i,2)
							self.AREA = nAREA
							#self.AREA = remove_RO_W(
							# self.AREA, i)
							cleared_tuples += 1
							self.score += 100
							break
					else:
						break
				self.addlines(cleared_tuples)
				return True
		return False
	
	def InstantDr(self):
		if not self.gameover and not self.paused:
			while(not self.drop(True)):
				pass
	
	def rotate_Designs(self):
		global new_s
		if not self.gameover and not self.paused:
			Bl=Block.__init__(self,self.Designs,self.AREA,0,1)
		#	new_s = rotate_clockwise(self.Designs)
	#		new_s = Bl.rotate_clockwise(self)
			if not CHECCK_COL(self.AREA,
			                       new_s,
			                       self.Designs_x, self.Designs_y):
				self.Designs = new_s
	
	def toggle_pause(self):
		self.paused = not self.paused
	
	def start_game(self):
		if self.gameover:
			self.game()
			self.gameover = False
	
	def run(self):
		keys = {
			'ESCAPE':	self.quit,
			'LEFT':		lambda:self.move(-1),
			'RIGHT':	lambda:self.move(+1),
			'DOWN':		lambda:self.drop(True),
			'UP':		self.rotate_Designs,
			'p':		self.toggle_pause,
			'SPACE':	self.start_game,
			'RETURN':	self.InstantDr
		}
		
		self.gameover = False
		self.paused = False
		
		dont_burn_my_cpu = pygame.time.Clock()
		while 1:
			self.screen.fill((0,0,0))
			if self.gameover:
				self.center_msg("""Game Over!\nYour score: %d
Press space to continue""" % self.score)
			else:
				if self.paused:
					self.center_msg("Paused")
				else:
					pygame.draw.line(self.screen,
						(255,255,255),
						(self.ROWLIMIT+1, 0),
						(self.ROWLIMIT+1, self.HEIGHT-1))
					self.MESSAGE("Next:", (
						self.ROWLIMIT+Size,
						2))
					self.MESSAGE("Score: %d\n\nLevel: %d\
\nLines: %d" % (self.score, self.level, self.lines),
						(self.ROWLIMIT+Size, Size*5))
					self.draw_matrix(self.bground_grid, (0,0))
					self.draw_matrix(self.AREA, (0,0))
					self.draw_matrix(self.Designs,
						(self.Designs_x, self.Designs_y))
					self.draw_matrix(self.next_Designs,
						(Columns+1,2))
			pygame.display.update()
			
			for event in pygame.event.get():
				if event.type == pygame.USEREVENT+1:
					self.drop(False)
				elif event.type == pygame.QUIT:
					self.quit()
				elif event.type == pygame.KEYDOWN:
					for key in keys:
						if event.key == eval("pygame.K_"
						+key):
							keys[key]()
					
			dont_burn_my_cpu.tick(maxfps)


if  __name__ == '__main__':
	app=Gameplay()
	app.run()
