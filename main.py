import pygame
import pygame.draw as draw
import pygame.display as display

import math


# Programme qui représente deux fonctions sinusoidales et, 
# en rouge, leur superposition. 
# La phase de la deuxième fonction peut être altérée par
# les contrôles ci-dessous.
# La superposition réagit, et elle devient rouge 
# lorsque l'interférence est purement constructive ou 
# destructive (plus ou moins). 
# 
# INSTRUCTIONS : 
# 
# 	- CLIC GAUCHE/DROIT: chgmt de phase (ponctuel)
# 	
# 	- FLECHE GAUCHE/DROITE: chgmt de phase (continu)
# 	 	(gardez L_SHIFT pour un mvmt plus rapide)
# 	
# 	- TOUCHE "V": visualisation pics/creux


BG = (51, 51, 85)
FG = (215, 215, 205)
LINE_COLOR = (155, 155, 145)
nFG = (225, 100, 100)
RED = (255, 10, 10)

SIZE = (500, 500)
WIN = display.set_mode(SIZE)

display.set_caption("SinSumSim")

AMPL = SIZE[1] // 12 - 5
PERIOD = 1/32

PRECISION = 0.08

PEAK_VISUALISATION = False

def handleEvents(g1, g2 = None): 

	global PEAK_VISUALISATION

	for event in pygame.event.get():
		 
		if event.type == pygame.QUIT: 
			pygame.quit()
			return True
			
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: 
				g2.update(math.pi/6)
			elif event.button == 3: 
				g2.update(-math.pi/6)

		elif event.type == pygame.KEYDOWN: 
			if event.key == pygame.K_v: 
				PEAK_VISUALISATION = not PEAK_VISUALISATION
				print(PEAK_VISUALISATION)
				g1.update(0)

	KEYS = pygame.key.get_pressed()

	if KEYS[pygame.K_RIGHT]:
		if KEYS[pygame.K_LSHIFT]: 
			g2.update(-math.pi/100)
		else: 
			g2.update(-math.pi/300)
	elif KEYS[pygame.K_LEFT]: 
		if KEYS[pygame.K_LSHIFT]: 
			g2.update(math.pi/100)
		else: 
			g2.update(math.pi/300)

class Graph: 

	def __init__(self, phi, win, base = False): 

		self.phi = phi
		self.win = win
		self.sizes = (self.win.get_width(), self.win.get_height())
		self.base = base
		if PEAK_VISUALISATION:
			if base: 
				self.base = True
				self.max = self.sizes[1]/2 + AMPL
		self.getPoints()

	def f(self, t):
		r = int((self.sizes[1]/2) + AMPL * math.sin(t * PERIOD + self.phi))
		return r

	def update(self, n):

		self.phi += n
		self.getPoints()
		if PEAK_VISUALISATION:
			if self.base: 
				self.base = True
				self.max = self.sizes[1]/2 + AMPL

	def getPoints(self): 
		self.points = []
		self.pointValues = []

		for t in range(self.sizes[0]): 
			self.points.append((t, self.f(t)))

		for p in self.points: 
			self.pointValues.append(p[1] - self.sizes[1])
			
	def show(self):

		for point in self.points:
			draw.circle(self.win, FG, point, 2)
			if PEAK_VISUALISATION: 
				if self.base:
					if int(AMPL * math.cos(point[0] * PERIOD + self.phi)) == 0: 
						draw.line(WIN, LINE_COLOR, (point[0], 0), (point[0], SIZE[1]))


class Sum: 

	def __init__(self, g1, g2, win): 

		self.firstGraph = g1
		self.secondGraph = g2
		self.win = win
		self.x = [t for t in range(self.win.get_width())]

	def show(self):
		
		if self.secondGraph.phi % math.pi < PRECISION or math.pi - self.secondGraph.phi % math.pi < PRECISION:
			color = RED 
		else: 
			color = nFG

		for i in range(len(self.firstGraph.pointValues)):
			x = self.x[i]
			y = ( self.firstGraph.pointValues[i] + self.secondGraph.pointValues[i] ) + 3 * self.win.get_height() // 2
			p = (x, y)
			draw.circle(self.win, color, p, 2) 

topWin = WIN.subsurface(pygame.Rect(0, 0, SIZE[0], SIZE[1]//3))
midWin = WIN.subsurface(pygame.Rect(0, SIZE[1]//3, SIZE[0], SIZE[1]//3))
botWin = WIN.subsurface(pygame.Rect(0, 2*SIZE[1]//3, SIZE[0], SIZE[1]//3))

g1 = Graph(0, topWin, base = True)
g2 = Graph((math.pi), midWin)
s = Sum(g1, g2, botWin)

while True:

		if handleEvents(g1, g2): 
			break

		WIN.fill(BG)

		g1.show()
		g2.show()
		s.show()

		pygame.display.flip()
