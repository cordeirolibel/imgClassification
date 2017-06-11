#>>>>>>>>			Interface				   <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - may of 2017		   #
#-------------------------------------------------------#

from commons import *
import Tkinter as tk #for keyboard read
import threading

#---------------------------------------------
#------Auxiliary
#---------------------------------------------

N_BOXS = 6

class Item:
	qtd = 0
	box = -1

	def add(self):
		self.qtd += 1


def name2symbol(name):

	cut = name.split()[1]

	if cut == 'cube':
		return  '[ ] Cube'
	elif cut == 'sphere':
		return  '( ) Sphere'
	elif cut == 'L':
		return  'L'
	elif cut == 'plus':
		return  '+ Plus'
	elif cut == 'rect':
		return  '[===] Rect'
	elif cut == 'coin':
		return  '(#) Coin'
	return name+'?'

#---------------------------------------------
#------App
#---------------------------------------------

class App(threading.Thread):
	squares = []
	box_free = 0
	take = False

	items = {'red cube':Item(), \
			 'red sphere':Item(), \
			 'red L':Item(), \
			 'red plus':Item(), \
			 'red rect':Item(), \
			 'red coin':Item(), \
			 'blue cube':Item(), \
			 'blue sphere':Item(), \
			 'blue L':Item(), \
			 'blue plus':Item(), \
			 'blue rect':Item(), \
			 'blue coin':Item()}

	def __init__(self):
		threading.Thread.__init__(self)
		self.start()

	#---------------------------------------------
	#------Interruptions Functions
	#---------------------------------------------
	def on_closing(self):
		self.root.quit() 
		os._exit(1)

	def keys(self,event):
		if event.char is 'k':
			self.root.quit() 
			os._exit(1)

	def takeObj(self):
		self.take = True

	def clear(self):

		self.box_free = 0

		#clear boxs
		k = 1
		for square in self.squares:
			square.config(text = 'Empty '+str(k), bg="gray")
			k+=1

		#clear itens
		for key in self.items:
			self.items[key].qtd = 0
			self.items[key].box = -1

	def run(self):
		#---------------------------------------------
		#------Screen Config
		#---------------------------------------------
		self.root = tk.Tk()
		self.root.geometry("220x340")
		self.root.title('3S Config')

		#---------------------------------------------
		#------Interruptions Config
		#---------------------------------------------

		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.bind('<Key>', self.keys)
		tk.Button(self.root, text='Take',width = 20, height = 3, command=self.takeObj).place(x=20, y=220)
		tk.Button(self.root, text='Clear',width = 20, height = 2, command=self.clear).place(x=20, y=280)

		#---------------------------------------------
		#------Draw Squares
		#---------------------------------------------
		for i in range(N_BOXS):
			self.squares.append(tk.Label(self.root, text="Empty", bg="gray", fg="white", width = 10, height = 4))

		self.squares[0].place(x=20, y=10)
		self.squares[1].place(x=120, y=10)
		self.squares[2].place(x=20, y=80)
		self.squares[3].place(x=120, y=80)
		self.squares[4].place(x=20, y=150)
		self.squares[5].place(x=120, y=150)
		self.root.mainloop()

	#return the position of the object 'name'
	def whichBox(self,name):

		item = self.items[name]

		#if don't have a box
		if item.box is -1:
			item.box = self.box_free
			self.box_free = (self.box_free+1)%N_BOXS

		item.add()

		#draw
		self.updateText()

		return item.box

	def updateText(self):

		#save texts
		texts = ['']*N_BOXS
		for key in self.items:
			#empty
			if self.items[key].box is -1:
				continue
			
			#string
			string = name2symbol(key) + '\n' 
			string += str(self.items[key].qtd) + '  '
			if key[0] == 'r': #red
				string += 'Red'
			else:
				string += 'Blue'
				
			#if not first
			if not texts[self.items[key].box] == '':
				string = '\n'+string

			texts[self.items[key].box] += string

		#draw texts
		for square, text in zip(self.squares,texts):
			square.config(text = text)
#---------------------------------------------
#------Main - Test
#---------------------------------------------

#app = App()
