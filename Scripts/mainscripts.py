import bge
import var
import GameObjects
from random import random as rnd

arah = [[0,1], [0, -1], [-1, 0], [1, 0]]
#       atas    bawah    kiri     kanan
#		  0		  1		   2		3

def acakNomorPuzzle():
	l = []
	n = 0
	for i in range(var.diameter):
		temp = []
		for j in range(var.diameter):
			temp.append(n)
			n+=1
		l.append(temp)
		
	i = 0
	lastUsed = [0, 0]
	pos = [0, 0]
	while i < var.acakLevel:
		tempL = []
		tempL = arah.copy()
		x, y = pos
		if x == 0:
			tempL.remove(arah[2])
		if x == var.diameter - 1:
			tempL.remove(arah[3])
		if y == 0:
			tempL.remove(arah[1])
		if y == var.diameter - 1:
			tempL.remove(arah[0])
		belakang = [-lastUsed[0], -lastUsed[1]]
		if belakang in tempL:
			tempL.remove(belakang)
		terpilih = tempL[int(rnd() * len(tempL))]
		sebelumnyaN = l[pos[0]][pos[1]]
		sebelumnya = pos.copy()
		pos = [terpilih[0] + pos[0], terpilih[1] + pos[1]]
		l[sebelumnya[0]][sebelumnya[1]] = l[pos[0]][pos[1]]
		l[pos[0]][pos[1]] = sebelumnyaN
		lastUsed = terpilih
		i+=1
	
	return l


def registerBlock(cont):
	own = cont.owner
	idx = own['index']
	this = GameObjects.KX_Block(own)
	this.index = idx
	var.blockList[this.index] = this

def initialize(cont):
	own = cont.owner
	ac = acakNomorPuzzle()
	'''
	l = []
	for i in ac:
		for j in i:
			l.append(j)
	n = 0
	'''
	
	#lb = var.blockList.copy()
	
	#ac = [[0,1,2], [3,4,5], [6,7,8]]
	print(ac)
	y = 0
	for i in ac:
		x = 0
		for j in ac[y]:
			var.blockList[j].position.x = -x
			var.blockList[j].position.y = y
			var.puzzle.append(j)
			x+=1
		y+=1
		
	del var.blockList[0]["block"]
	var.status = "ready"

# ------------------------------------- Player Controller -------------------------------------
def MoveBlock(cont):
	own = cont.owner
	mover = cont.sensors['mover']
	click = cont.sensors['click']
	if mover.positive and click.positive:
		if 'index' in mover.hitObject:
			'''
			'''
			if mover.hitObject['moveable'] == True:
				temp = mover.hitObject.position.copy()
				mover.hitObject.position = var.blockList[0].position
				var.blockList[0].position = temp
				
				d1 = var.puzzle.index(mover.hitObject.index)
				d2 = var.puzzle.index(var.blockList[0].index)
				#skg kase baku tukar dong pe nilai
				var.puzzle[d1] = var.blockList[0].index
				var.puzzle[d2] = mover.hitObject.index
	own['puzzle'] = str(var.puzzle)
	if var.puzzle == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
		for i in var.blockList[0].children:
			i.visible = True
		bge.logic.addScene("HUD")
		own.scene.suspend()
# ---------------------------------------------------------------------------------------------

def setBahasa(cont):
	own = cont.owner
	aktif = True
	for sen in cont.sensors:
		if sen.positive == False:
			aktif = False
			
	if aktif:
		var.bahasa = own['bahasa']
		own.scene.replace("inGame")

def translate(cont):
	own = cont.owner
	if var.bahasa == 1:
		own.text = var.terjemahan[own['identifikasi']]
	