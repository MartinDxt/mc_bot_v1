import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider
from matplotlib import animation

"""
5.2.4  dns https://www.izhikevich.org/publications/

Model:
dV/dt  = (k*(V - Vr)*(V - Vt) - u + I)/C
du/dt = a*(b*(V - Vr) - u)

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
u = k*(V - Vr)*(V - Vt) + I
u = b*(V - Vr) 
"""


class Sim:
    def __init__(self, Vr, Vt, Vpeak, a, b, c, d, k, I, C):
        self.Vsim = 0
        self.usim = 0
        self.Vr = Vr
        self.Vt = Vt
        self.Vpeak = Vpeak
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.k = k
        self.I = I
        self.C = C

    def updatevar(self, Vr, Vt, Vpeak, a, b, c, d, k, I, C):
        self.Vr = Vr
        self.Vt = Vt
        self.Vpeak = Vpeak
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.k = k
        self.I = I
        self.C = C

    def step(self):
        spike = 0
        self.Vsim = self.Vsim + (self.k * (self.Vsim - self.Vr) * (self.Vsim - self.Vt) - self.usim + self.I)/self.C
        self.usim = self.usim + self.a * (self.b * (self.Vsim - self.Vr) - self.usim)
        if self.Vsim > self.Vpeak:
            spike = 1
            upad = self.usim
            self.Vsim = self.c
            self.usim = self.usim + self.d
            return self.Vpeak, upad, spike  # padding for consistent spikes
        else:
            return self.Vsim, self.usim, spike


def frames():
    while True:
        yield s.step()


def Vnullcline(V, Vr, Vt, k, I):
    return k * (V - Vr) * (V - Vt) + I


def unullcline(V, Vr, b):
    return b * (V - Vr)


v = np.linspace(-500, 500, 2000)

# Define initial parameters
Vr = -60
Vt = -40
Vpeak = 35
a = 0.03
b = -2
c = -50
d = 100
k = 0.7
I = 0.0
C = 100
s = Sim(Vr, Vt, Vpeak, a, b, c, d, k, I, C)
x1 = [0] * 100
y1 = [0] * 100
x2 = np.arange(-1000, 0, 1)
y2 = [0] * x2.size
i = [-1.5] * x2.size

# Create the figure and the line that we will manipulate
fig, ((ax1, ax2), axs) = plt.subplots(2, 2, figsize=(15, 10))
gs = axs[1].get_gridspec()
for ax in axs[:]:
    ax.remove()
ax3 = fig.add_subplot(gs[1, :])
ax1.plot(v, Vnullcline(v, Vr, Vt, k, I), lw=2)
ax1.plot(v, unullcline(v, Vr, b), lw=2)
ax1.set_xlabel('V')
ax1.set_ylabel('w')
# setting limits to the axes
ax1.set_xlim((-70, 35))
ax1.set_ylim((-50, 60))
ax2.set_xlim((-70, 35))
ax2.set_ylim((-50, 60))
ax3.set_ylim((-2, 2))

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
    valmax=10,
    valinit=b,
    orientation="vertical"
)

# Make a vertically oriented slider to control k
axk = fig.add_axes([0.15, 0.35, 0.03, 0.5])
k_slider = Slider(
    ax=axk,
    label="k",
    valmin=0,
    valmax=2,
    valinit=k,
    orientation="vertical"
)

# Make a vertically oriented slider to control C
axC = fig.add_axes([0.2, 0.35, 0.03, 0.5])
C_slider = Slider(
    ax=axC,
    label="C",
    valmin=0,
    valmax=200,
    valinit=C,
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

# Make a horizontal slider to control Vr.
axVr = fig.add_axes([0.05, 0.1, 0.35, 0.03])
Vr_slider = Slider(
    ax=axVr,
    label='Vr',
    valmin=-100,
    valmax=100,
    valinit=Vr,
)

# Make a horizontal slider to control Vt.
axVt = fig.add_axes([0.05, 0.2, 0.35, 0.03])
Vt_slider = Slider(
    ax=axVt,
    label='Vt',
    valmin=-100,
    valmax=100,
    valinit=Vt,
)

# Make a horizontal slider to control Vpeak.
axVpeak = fig.add_axes([0.05, 0.15, 0.35, 0.03])
Vpeak_slider = Slider(
    ax=axVpeak,
    label='Vpeak',
    valmin=-100,
    valmax=100,
    valinit=Vpeak,
)



# The function to be called anytime a slider's value changes
def update(val):
    ax1.clear()
    ax1.plot(v, Vnullcline(v, Vr_slider.val, Vt_slider.val, k_slider.val, I_slider.val), lw=2)
    ax1.plot(v, unullcline(v, Vr_slider.val, b_slider.val), lw=2)
    fig.canvas.draw_idle()
    s.updatevar(Vr_slider.val, Vt_slider.val, Vpeak_slider.val, a_slider.val, b_slider.val, c_slider.val, d_slider.val, k_slider.val, I_slider.val, C_slider.val)


# register the update function with each slider
Vr_slider.on_changed(update)
Vt_slider.on_changed(update)
Vpeak_slider.on_changed(update)
a_slider.on_changed(update)
b_slider.on_changed(update)
c_slider.on_changed(update)
d_slider.on_changed(update)
k_slider.on_changed(update)
I_slider.on_changed(update)
C_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
rs_ib = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button_ib = Button(rs_ib, 'Intrinsically bursting', hovercolor='0.975')
rs_ax = fig.add_axes([0.1, 0.025, 0.1, 0.04])
button_rs = Button(rs_ax, 'Regular spiking', hovercolor='0.975')
rs_ch = fig.add_axes([0.3, 0.025, 0.1, 0.04])
button_ch = Button(rs_ch, 'chattering', hovercolor='0.975')


def regular_spiking(event):
    Vr_slider.reset()
    Vt_slider.reset()
    Vpeak_slider.reset()
    a_slider.reset()
    b_slider.reset()
    c_slider.reset()
    d_slider.reset()
    k_slider.reset()
    I_slider.reset()
    C_slider.reset()

def intrinsically_bursting(event):
    Vr_slider.set_val(-75)
    Vt_slider.set_val(-45)
    Vpeak_slider.set_val(50)
    a_slider.set_val(0.01)
    b_slider.set_val(5)
    c_slider.set_val(-56)
    d_slider.set_val(130)
    k_slider.set_val(1.2)
    C_slider.set_val(150)

def chattering(event):
    Vr_slider.set_val(-60)
    Vt_slider.set_val(-40)
    Vpeak_slider.set_val(25)
    a_slider.set_val(0.03)
    b_slider.set_val(5)
    c_slider.set_val(-40)
    d_slider.set_val(150)
    k_slider.set_val(1.5)
    C_slider.set_val(50)
"""
dV/dt  = (k*(V - Vr)*(V - Vt) - u + I)/C
du/dt = a*(b*(V - Vr) - u)
"""

def animate(args):
    ax2.clear()
    ax3.clear()
    ax1.set_ylim((-500, 1000))
    ax1.set_xlim((-300, 300))
    ax2.set_ylim((-500, 1000))
    ax2.set_xlim((-300, 300))
    """
    ax2.set_xlim((-Vpeak_slider.val*2, Vpeak_slider.val))
    ax2.set_ylim((-75, 100))
    ax3.set_ylim((-Vpeak_slider.val, Vpeak_slider.val))"""
    x1.pop(0)
    y1.pop(0)
    y2.pop(0)
    i.pop(0)
    x1.append(args[0])
    y1.append(args[1])
    y2.append(args[0])
    i.append(I_slider.val/10)
    return ax2.plot(x1, y1, color='g'), ax3.plot(x2, y2, color='b'), ax3.plot(x2, i, color='r'), plt.show()


button_rs.on_clicked(regular_spiking)
button_ib.on_clicked(intrinsically_bursting)
button_ch.on_clicked(chattering)
anim = animation.FuncAnimation(fig, animate, frames=frames, interval=30, save_count=2000)
plt.show()
