import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider
from matplotlib import animation

"""
5.2.4  dns https://www.izhikevich.org/publications/

Model:
dV/dt  = 0.04 * vp^2 + 5 * v + 140 - u + I
du/dt = a*(b*V - u)

if V ≥ Vpeak, then
V <- c, u <- u + d

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
u = k*(V - Vr)*(V - Vt) + I
u = b*(V - Vr) 
"""


class Sim:
    def __init__(self, Vpeak, a, b, c, d, I):
        self.Vsim = 0
        self.usim = 0
        self.Vpeak = Vpeak
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.I = I

    def updatevar(self, Vpeak, a, b, c, d, I):
        self.Vpeak = Vpeak
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.I = I

    def step(self):
        spike = 0
        self.Vsim = self.Vsim + 0.2*(0.04 * self.Vsim ** 2 + 5 * self.Vsim + 140 - self.usim + self.I)
        self.usim = self.usim + 0.2*(self.a * (self.b * self.Vsim - self.usim))
        if self.Vsim > self.Vpeak:
            spike = 1
            upad = self.usim
            self.Vsim = self.c
            self.usim = self.usim + self.d
            return self.Vpeak, upad, spike  # padding for consistent spikes
        else:
            return self.Vsim, self.usim, spike

    def setvu(self, v, u):
        self.Vsim = v
        self.usim = u


def frames():
    while True:
        yield s.step()


def Vnullcline(V, I):
    return 0.04 * V ** 2 + 5 * V + 140 + I


def unullcline(V, b):
    return b * V


def U_vec(X, Y, I):
    return (np.full(X.shape, 0.04) * X * X + np.full(X.shape, 5) * X)+ np.full(X.shape, 140) - Y + np.full(X.shape, I)


def V_vec(X, Y, a, b):
    return np.full(X.shape, a) * (np.full(X.shape, b) * X - Y)


def normalize(U, V):
    U / (U * U + V * V)
    return U / (U * U + V * V) ** 0.5, V / (U * U + V * V) ** 0.5

# taken from demo izhikevich
par = [[0.02, 0.2, -65, 6, 14],  # tonic spiking
       [0.02, 0.25, -65, 6, 0.5],  # phasic spiking
       [0.02, 0.2, -50, 2, 15],  # tonic bursting
       [0.02, 0.25, -55, 0.05, 0.6],  # phasic bursting
       [0.02, 0.2, -55, 4, 10],  # mixed mode
       [0.01, 0.2, -65, 8, 30],  # spike frequency adaptation
       [0.02, -0.1, -55, 6, 0],  # Class 1
       [0.2, 0.26, -65, 0, 0],  # Class 2
       [0.02, 0.2, -65, 6, 7],  # spike latency
       [0.05, 0.26, -60, 0, 0],  # subthreshold oscillations
       [0.1, 0.26, -60, -1, 0],  # resonator
       [0.02, -0.1, -55, 6, 0],  # integrator
       [0.03, 0.25, -60, 4, 0],  # rebound spike
       [0.03, 0.25, -52, 0, 0],  # rebound burst
       [0.03, 0.25, -60, 4, 0],  # threshold variability
       [1, 1.5, -60, 0, -65],  # bistability
       [1, 0.2, -60, -21, 0],  # DAP
       [0.02, 1, -55, 4, 0],  # accomodation
       [-0.02, -1, -60, 8, 80],  # inhibition-induced spiking
       [-0.026, -1, -45, 0, 80]]  # inhibition-induced bursting

v = np.linspace(-500, 500, 2000)

# Define initial parameters
Vpeak = 30
a = 0.02
b = 0.2
c = -65
d = 6
I = 14
s = Sim(Vpeak, a, b, c, d, I)
x1 = [0] * 100
y1 = [0] * 100
x2 = np.arange(-1000, 0, 1)
y2 = [0] * x2.size
i = [-1.5] * x2.size
x = np.arange(-200, 120, 12)
y = np.arange(-500, 1000, 150)
X, Y = np.meshgrid(x, y)

# Create the figure and the line that we will manipulate
fig, ((ax1, ax2), axs) = plt.subplots(2, 2, figsize=(15, 10))
gs = axs[1].get_gridspec()
for ax in axs[:]:
    ax.remove()
ax3 = fig.add_subplot(gs[1, :])
ax1.plot(v, Vnullcline(v, I), lw=2)
ax1.plot(v, unullcline(v, b), lw=2)
ax1.set_xlabel('V')
ax1.set_ylabel('u')
U, V = U_vec(X, Y, I), V_vec(X, Y, a, b)
U, V = normalize(U, V)
ax1.quiver(X, Y, U, V)
# setting limits to the axes
ax1.set_ylim((-500, 1000))
ax1.set_xlim((-200, Vpeak * 1.2))
ax2.set_ylim((-500, 1000))
ax2.set_xlim((-200, Vpeak * 1.2))

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.35, bottom=0.35)

# Make a vertically oriented slider to control a
axa = fig.add_axes([0.05, 0.35, 0.03, 0.5])
a_slider = Slider(
    ax=axa,
    label="a",
    valmin=0,
    valmax=0.2,
    valinit=a,
    orientation="vertical"
)

# Make a vertically oriented slider to control b
axb = fig.add_axes([0.1, 0.35, 0.03, 0.5])
b_slider = Slider(
    ax=axb,
    label="b",
    valmin=-10,
    valmax=40,
    valinit=b,
    orientation="vertical"
)

# Make a horizontal slider to control the current.
axI = fig.add_axes([0.5, 0.1, 0.35, 0.03])
I_slider = Slider(
    ax=axI,
    label='I',
    valmin=-1000,
    valmax=1000,
    valinit=I,
)

# Make a horizontal slider to control c.
axc = fig.add_axes([0.5, 0.2, 0.35, 0.03])
c_slider = Slider(
    ax=axc,
    label='c',
    valmin=-100,
    valmax=100,
    valinit=c,
)

# Make a horizontal slider to control d.
axd = fig.add_axes([0.5, 0.15, 0.35, 0.03])
d_slider = Slider(
    ax=axd,
    label='d',
    valmin=-100,
    valmax=200,
    valinit=d,
)

# Make a horizontal slider to control Vpeak.
axVpeak = fig.add_axes([0.05, 0.2, 0.35, 0.03])
Vpeak_slider = Slider(
    ax=axVpeak,
    label='Vpeak',
    valmin=-100,
    valmax=100,
    valinit=Vpeak,
)

# Make "select" horizontal slider to control model type.
axselect = fig.add_axes([0.4, 0.25, 0.35, 0.03])
select_slider = Slider(
    ax=axselect,
    label='select type',
    valmin=0,
    valmax=20,
    valstep=1,
    valinit=0,
)


# The function to be called anytime a slider's value changes
def update(val):
    ax1.clear()
    ax1.plot(v, Vnullcline(v, I_slider.val), lw=2)
    ax1.plot(v, unullcline(v, b_slider.val), lw=2)
    U, V = U_vec(X, Y, I_slider.val), V_vec(X, Y,
                                            a_slider.val,
                                            b_slider.val)
    ax1.quiver(X, Y, U, V)
    ax2.clear()
    ax2.plot(v, Vnullcline(v, I_slider.val), lw=2)
    ax2.plot(v, unullcline(v, b_slider.val), lw=2)
    fig.canvas.draw_idle()
    s.updatevar(Vpeak_slider.val, a_slider.val, b_slider.val, c_slider.val, d_slider.val, I_slider.val)


def update_mode(val):
    n = int(select_slider.val)
    if n != 0:
        n = n - 1
        a_slider.set_val(par[n][0])
        b_slider.set_val(par[n][1])
        c_slider.set_val(par[n][2])
        d_slider.set_val(par[n][3])
        I_slider.set_val(par[n][4])
        Vpeak_slider.set_val(30)


# register the update function with each slider

Vpeak_slider.on_changed(update)
a_slider.on_changed(update)
b_slider.on_changed(update)
c_slider.on_changed(update)
d_slider.on_changed(update)
I_slider.on_changed(update)
select_slider.on_changed(update_mode)


def animate(args):
    ax2.clear()
    ax3.clear()
    ax1.set_ylim((-500, 1000))
    ax1.set_xlim((-200, Vpeak_slider.val * 1.2))
    ax2.set_ylim((-500, 1000))
    ax2.set_xlim((-200, Vpeak_slider.val * 1.2))
    x1.pop(0)
    y1.pop(0)
    y2.pop(0)
    i.pop(0)
    x1.append(args[0])
    y1.append(args[1])
    y2.append(args[0])
    i.append(I_slider.val / 10)
    return (ax2.plot(x1, y1, color='g'), ax3.plot(x2, y2, color='b'), ax3.plot(x2, i, color='r'),
            ax2.plot(v, Vnullcline(v, I_slider.val), lw=2), ax2.plot(v, unullcline(v, b_slider.val), lw=2), plt.show())


anim = animation.FuncAnimation(fig, animate, frames=frames, interval=30, save_count=2000)
plt.show()
