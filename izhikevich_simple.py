import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider
from matplotlib import animation

"""
5.2.4  dns https://www.izhikevich.org/publications/

Model:
dV/dt  = I + V^2 - u
du/dt = a(bV - u)

if v ≥ 1, then
v <- c, u <- u + d

V approximation of membrane potential
u recovery variable slow outward currents
I injected current
a, b recovery dynamics
c reset v value
d update recovery value u

for multiple recovery variables: 
a b d and w become vectors
dV/dt = I + v^2 - sum(u)

Nullclides:
u = V^2 + I
u = b*V
"""


class Sim:
    def __init__(self, a, b, c, d, I):
        self.Vsim = 0
        self.usim = 0
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.I = I

    def updatevar(self, a, b, c, d, I):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.I = I

    def step(self):
        spike = 0
        self.Vsim = self.Vsim + (self.I + self.Vsim ** 2 + self.usim)
        self.usim = self.usim + self.a * (self.b * self.Vsim - self.usim)
        if self.Vsim > 1:
            spike = 1
            self.Vsim = self.c
            self.usim = self.usim + self.d

        return self.Vsim, self.usim, spike


def frames():
    while True:
        yield s.step()


def Vnullcline(V, I):
    return V ** 2 + I


def unullcline(V, b):
    return b * V


def U_vec(X, Y, I):
    return np.full(X.shape, I) + X ** 2 - Y


def V_vec(X, Y, a, b):
    return np.full(X.shape, a) * (np.full(X.shape, b) * X - Y)


v = np.linspace(-0.6, 1.2, 1000)

# Define initial parameters
a = 0.03
b = -0.02
c = -0.5
d = 1
I = 0.0
s = Sim(a, b, c, d, I)
x1 = [0] * 100
y1 = [0] * 100
x2 = np.arange(-20 + 0.03, 0, 0.03)
y2 = [0] * x2.size
i = [-1.5] * x2.size
x = np.arange(-0.6, 1.2, 0.1)
y = np.arange(-0.05, 0.2, 0.01)
X, Y = np.meshgrid(x, y)

# Create the figure and the line that we will manipulate
fig, ((ax1, ax2), axs) = plt.subplots(2, 2)
gs = axs[1].get_gridspec()
for ax in axs[:]:
    ax.remove()
ax3 = fig.add_subplot(gs[1, :])
ax1.plot(v, Vnullcline(v, I), lw=2)
ax1.plot(v, unullcline(v, b), lw=2)
ax1.set_xlabel('V')
ax1.set_ylabel('w')
U, V = U_vec(X, Y, I), V_vec(X, Y, a, b)
ax1.quiver(X, Y, U, V)

# setting limits to the axes
ax1.set_xlim((-0.6, 1.2))
ax1.set_ylim((-0.05, 0.2))
ax2.set_ylim((-0.05, 0.25))
ax2.set_xlim((-0.6, 1.2))
ax3.set_ylim((-2, 2))
# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.35, bottom=0.35)

# Make a vertically oriented slider to control a
axa = fig.add_axes([0.2, 0.25, 0.03, 0.5])
a_slider = Slider(
    ax=axa,
    label="a",
    valmin=0,
    valmax=1,
    valinit=a,
    orientation="vertical"
)

# Make a vertically oriented slider to control b
axb = fig.add_axes([0.1, 0.25, 0.03, 0.5])
b_slider = Slider(
    ax=axb,
    label="b",
    valmin=-0.2,
    valmax=0.2,
    valinit=b,
    orientation="vertical"
)

# Make a horizontal slider to control the current.
axI = fig.add_axes([0.4, 0.1, 0.35, 0.03])
I_slider = Slider(
    ax=axI,
    label='Current I [pA]',
    valmin=0,
    valmax=0.1,
    valinit=I,
)


# Make c horizontal slider to control c.
axc = fig.add_axes([0.4, 0.2, 0.35, 0.03])
c_slider = Slider(
    ax=axc,
    label='c',
    valmin=-1,
    valmax=1,
    valinit=c,
)

# Make d horizontal slider to control d.
axd = fig.add_axes([0.4, 0.15, 0.35, 0.03])
d_slider = Slider(
    ax=axd,
    label='d',
    valmin=-2,
    valmax=2,
    valinit=d,
)

# The function to be called anytime a slider's value changes
def update(val):
    ax1.clear()
    ax1.plot(v, Vnullcline(v, I_slider.val), lw=2)
    ax1.plot(v, unullcline(v, b_slider.val), lw=2)
    U, V = U_vec(X, Y, I_slider.val), V_vec(X, Y, a_slider.val, b_slider.val)
    ax1.quiver(X, Y, U, V)
    ax1.set_xlim((-0.6, 1.2))
    ax1.set_ylim((-0.05, 0.2))
    fig.canvas.draw_idle()
    ax2.set_ylim((-0.05, 0.25))
    ax2.set_xlim((-0.6, 1.2))
    s.updatevar(a_slider.val, b_slider.val, c_slider.val, d_slider.val, I_slider.val)


# register the update function with each slider
a_slider.on_changed(update)
b_slider.on_changed(update)
c_slider.on_changed(update)
d_slider.on_changed(update)
I_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    a_slider.reset()
    b_slider.reset()
    c_slider.reset()
    d_slider.reset()
    I_slider.reset()


def animate(args):
    ax2.clear()
    ax3.clear()
    ax2.set_ylim((-0.05, 0.25))
    ax2.set_xlim((-0.6, 1.2))
    ax3.set_ylim((-2, 2))
    x1.pop(0)
    y1.pop(0)
    y2.pop(0)
    i.pop(0)
    x1.append(args[0])
    y1.append(args[1])
    y2.append(args[0])
    i.append(I_slider.val * 20 - 1.5)
    return ax2.plot(x1, y1, color='g'), ax3.plot(x2, y2, color='b'), ax3.plot(x2, i, color='r'), plt.show()


button.on_clicked(reset)
anim = animation.FuncAnimation(fig, animate, frames=frames, interval=30, save_count=2000)
plt.show()
