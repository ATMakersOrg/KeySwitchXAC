from mode import Mode

#This global section sets how to change modes
#By default you hold down switches 1&2 for 2 seconds to switchmodes

modeSwitches=(5,) #which switches do you hold down to change modes
modeDelay=2.0 #And how many seconds does it wait when they're down

repeatDelay=.2

#For a single switch user, you might choose
#modeswitches=1
#modedelay=3.0
modes = {}


#It sends button press for buttons 1-4 and lights up blue
modes[0] = Mode("ButtonPress", "#0000ff")
modes[0].buttonPress(1, 1)              #Button X1(L-USB)/View(R-USB)
modes[0].buttonPress(2, 2)              #Button X2(L-USB)/Menu(R-USB)
modes[0].buttonPress(3, 3)              #Button LS(L-USB)/RS(R-USB)
modes[0].buttonPress(4, 4)              #Button LB(L-USB)/RB(R-USB)

#Dpad Mode and lights up red
modes[1] = Mode("Dpad", "#FF0000")
modes[1].dpadMove(1, 0, 1)
modes[1].dpadMove(2, 0, -1)
modes[1].dpadMove(3, -1, 0)
modes[1].dpadMove(4, 1, 0)

#Extra buttons Mode and lights up green
modes[2] = Mode("ButtonExtra", "#00FF00")
modes[2].buttonPress(1, 5)              #Button A(L-USB)/X(R-USB)
modes[2].buttonPress(2, 6)              #Button B(L-USB)/Y(R-USB)
modes[2].buttonPress(3, [7,8])          #Button Menu and View (L-USB)
modes[2].buttonPress(4, 8)              #Button Menu(L-USB)