import pyautogui
import time
from matplotlib import pyplot as plt
from matplotlib import animation


def frames():
    while True:
        yield pyautogui.position()


fig = plt.figure()

x = []
y = []
def animate(args):
    x.append(args[0])
    y.append(-args[1])
    return plt.plot(x, y, color='g')


anim = animation.FuncAnimation(fig, animate, frames=frames, interval=60)
plt.show()



