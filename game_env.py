from Tkinter import *

game=Tk()
game.title('Sink The Ship')
game.geometry("%dx%d+%d+%d" % (1400, 660, 0, 0))
screen1 = Frame(game, width = 600, height = 400, pady = 50, padx = 50)
screen1.pack(side=LEFT)
screen1.grid()
slabel1 = Label(screen1)
screen2 = Frame(game, width = 600, height = 400, pady = 50, padx = 50)
screen1.pack(side=RIGHT)
screen2.grid()
slabel2 = Label(screen2)

def check(i,j):
    x=2
    if x==0:
        x=1

for i in range(10):
    for j in range(10):
        button=Button(screen1, width=6, height=2, command=check(i,j))
        button.grid(row=i,column=j)

for i in range(10):
    for j in range(10):
        button=Button(screen2, width=6, height=2, command=check(i,j))
        button.grid(row=i,column=j)

game.mainloop()
