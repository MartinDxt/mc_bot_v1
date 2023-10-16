import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider
from matplotlib import animation

"""
4.2.6 dns https://www.izhikevich.org/publications/
Model:
dV/dt = V*(a − V)*(V − 1) − w + I
dw/dt = b*V − c*w
V approximation of membrane potential
w recovery variable slow outward currents
I injected current
a shape of the cubic parabola V(a − V)*(V − 1)
b and c kinetics recovery variable
Constraints:
b > 0
c ≥ 0

for multiple recovery variables: 
b c and w become vectors
dV/dt = V*(a − V)*(V − 1) − sum(w) + I

Nullclines:
w = V (a − V )(V − 1) + I
w = b/c V

Linearized stability w/ I=0:
tr(L) = −a − c < 0 
det(L) = ac + b > 0
"""

# class that contains the sim neuron
class Sim:
    def __init__(self, a, b, c, I):
        self.Vsim = 0
        self.wsim = 0
        self.a = a
        self.b = b
        self.c = c
        self.I = I

    def updatevar(self, a, b, c, I):
        self.a = a
        self.b = b
        self.c = c
        self.I = I

    def step(self):
        self.Vsim = self.Vsim+(self.Vsim*(self.a -self.Vsim)*(self.Vsim - 1) - self.wsim + self.I)
        self.wsim = self.wsim+(self.b*self.Vsim - self.c*self.wsim)
        return self.Vsim, self.wsim


def frames():
    while True:
        yield s.step()


def Vnullcline(V, a, I):
    return V * (a - V) * (V - 1) + I


def wnullcline(V, b, c):
    return V * (b / c)


def U_vec(X, Y, a, I):
    return X * (np.full(X.shape, a) - X) * (X - np.ones(X.shape)) - Y + np.full(X.shape, I)


def V_vec(X, Y, b, c):
    return np.full(X.shape, b) * X - np.full(X.shape, c) * Y


v = np.linspace(-0.6, 1.2, 1000)

# Define initial parameters
b = 0.01
c = 0.02
a = 0.1
I = 0.0
s = Sim(a, b, c, I)
x1 = [0]*100
y1 = [0]*100
x = np.arange(-0.6, 1.2, 0.1)
y = np.arange(-0.05, 0.2, 0.01)
X, Y = np.meshgrid(x, y)

# Create the figure and the line that we will manipulate
fig1, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(v, Vnullcline(v, a, I), lw=2)
ax1.plot(v, wnullcline(v, b, c), lw=2)
ax1.set_xlabel('V')
ax1.set_ylabel('w')
vec_field = ax1.quiver(X, Y, U_vec(X, Y, a, I), V_vec(X, Y, b, c))
ax1.set_xlim((-0.6, 1.2))
ax1.set_ylim((-0.05, 0.2))
# adjust the main plot to make room for the sliders
fig1.subplots_adjust(left=0.35, bottom=0.35)
# Make a horizontal slider to control the current.
axI = fig1.add_axes([0.4, 0.1, 0.35, 0.03])
I_slider = Slider(
    ax=axI,
    label='Current I [pA]',
    valmin=0,
    valmax=0.3,
    valinit=I,
)

# Make a horizontal slider to control a.
axa = fig1.add_axes([0.4, 0.2, 0.35, 0.03])
a_slider = Slider(
    ax=axa,
    label='a',
    valmin=-1,
    valmax=1,
    valinit=I,
)

# Make a vertically oriented slider to control b
axb = fig1.add_axes([0.1, 0.25, 0.03, 0.5])
b_slider = Slider(
    ax=axb,
    label="b",
    valmin=0,
    valmax=0.1,
    valinit=b,
    orientation="vertical"
)

# Make a vertically oriented slider to control c
axc = fig1.add_axes([0.2, 0.25, 0.03, 0.5])
c_slider = Slider(
    ax=axc,
    label="c",
    valmin=0.0001,
    valmax=0.1,
    valinit=b,
    orientation="vertical"
)


# The function to be called anytime a slider's value changes
def update(val):

    ax1.clear()
    ax1.plot(v, Vnullcline(v, a_slider.val, I_slider.val), lw=2)
    ax1.plot(v, wnullcline(v, b_slider.val, c_slider.val), lw=2)
    ax1.quiver(X, Y, U_vec(X, Y, a_slider.val, I_slider.val), V_vec(X, Y, b_slider.val, c_slider.val))
    ax1.set_xlim((-0.6, 1.2))
    ax1.set_ylim((-0.05, 0.2))
    fig1.canvas.draw_idle()
    ax2.set_ylim((-0.45, 0.45))
    ax2.set_xlim((-0.6, 1.2))
    s.updatevar(a_slider.val, b_slider.val, c_slider.val, I_slider.val)


# register the update function with each slider
a_slider.on_changed(update)
b_slider.on_changed(update)
c_slider.on_changed(update)
I_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig1.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    a_slider.reset()
    b_slider.reset()
    c_slider.reset()
    I_slider.reset()


def animate(args):
    ax2.clear()
    ax2.set_ylim((-0.45, 0.45))
    ax2.set_xlim((-0.6, 1.2))
    x1.pop(0)
    y1.pop(0)
    x1.append(args[0])
    y1.append(args[1])
    return ax2.plot(x1, y1, color='g'), plt.show()

button.on_clicked(reset)
anim = animation.FuncAnimation(fig1, animate, frames=frames, interval=30, save_count=2000)
plt.show()
