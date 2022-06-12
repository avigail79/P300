import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

x = np.linspace(0,2,100)
x0 = 0.5 # resting tendon length

def active_force_length(x, x0):
    w = 0.185
    alpha = np.exp(-((x/x0-1)**2)/w)
    return alpha

alpha = active_force_length(x, x0)

def passive_force(x, x0):
    k = 5
    eps = 0.6

    f_p = (np.exp((k * (x/x0-1)) / eps) -1) / (np.exp(k) -1)
    return f_p


g = 1  # gama
a = 1  # alpha
F = np.linspace(0, 1.399, 300)


def force_velocity_calc(f, g, a, x0):
    F_max = 1.4
    A_f = 0.25
    V_mx = 10  # aproximate V_max form the article

    # b calculation
    if f < g * a:
        b = g * a + f / A_f
    else:
        b = ((2 + (2 / A_f)) * (g * a * F_max - f)) / (F_max - 1)
    return x0 * (0.25 + 0.75 * g) * V_mx * ((f - g * a) / b)


def force_velocity(F, g, a, x0):
    F_max = 1.4
    A_f = 0.25
    V_mx = 10  # aproximate V_max form the article

    xdot = []
    for f in F:
        xd = force_velocity_calc(f, g, a, x0)
        xdot.append(xd)
    return np.array(xdot)


Y = np.linspace(0.5, 0.55, 100)
y0 = 0.5


def tendon_strain_calc(y, y0):
    F_toe = 0.33
    k_toe = 3
    e_0 = 0.04
    eps_toe = 0.609 * e_0
    k_lin = 1.712 * ((e_0) ** -1)

    y_til = (y - y0) / y0

    if y_til < eps_toe:
        f_t = (F_toe / (np.exp(k_toe) - 1)) * (np.exp(k_toe * y_til / eps_toe) - 1)
    elif y_til > eps_toe:
        f_t = k_lin * (y_til - eps_toe) + F_toe
    else:
        f_t = 1

    return f_t


def tendon_strain(Y, y0):
    F_t = []
    for y in Y:
        F_t.append(tendon_strain_calc(y, y0))
    return F_t

t = np.linspace(0,1,100)
stim_duration = [0.1, 0.6]

tau_act = 0.015  # ms
tau_deact = 0.05  # ms

STIM = lambda t, stim_duration: (t > stim_duration[0]) * 1 * (t <= stim_duration[1])
TAU = lambda stim, g: 0.015 * (0.5 + 1.5 * g) if stim > g else 0.05 / (0.5 + 1.5 * g)


def activation_dynamic_calc(g, t, stim_duration):
    stim = STIM(t, stim_duration)
    tau = TAU(stim, g)
    dgdt = (stim - g) / tau
    return dgdt


def activation_dynamic(t, stim_duration):
    stim = STIM(t, stim_duration)
    g0 = 0
    muscle_active_g = odeint(activation_dynamic_calc, g0, t, args=(stim_duration, ))
    return [muscle_active_g, stim]


def hill_type_model(t, stim_duration, x0=0.5, y0=0.5, theta=0, L_mt=1):
    x = np.zeros(len(t))
    x[0] = x0  # muscle length
    y = np.zeros(len(t))
    y[0] = y0  # tendon length
    # g = np.zeros(len(t))  # gamma
    g0 = 0.0001

    f_t = np.zeros(len(t))
    f_t[0] = tendon_strain_calc(y[0], y0)

    g = odeint(activation_dynamic_calc, g0, t, args=(stim_duration,))

    for i in range(1, len(t)):
        a = active_force_length(x[i-1], x0)  # calc the active force
        f_pe = passive_force(x[i-1], x0)  # calc the passive force
        f_mf = f_t[i-1] / np.cos(theta) - f_pe  # calc the muscle fiber length

        dxdt = force_velocity_calc(f_mf, g[i-1], a, x0)

        x[i] = x[i-1] + dxdt/x0  # update the muscle length
        y[i] = L_mt - x[i]  # update the tendon length
        f_t[i] = tendon_strain_calc(y[i], y0)  # use the tendon length to calc the tendon force

        # L_mt = y[i] + x[i]

    Stim = STIM(t, stim_duration)

    plt.plot(t, Stim)
    plt.plot(t, g)
    plt.plot(t, x)
    plt.plot(t, y)
    plt.plot(t, f_t)
    plt.title('Hill type model')
    plt.legend(["STIM", "Activation dynamics (gamma)", "Muscle Fiber Length", "Tendon Length", "Tendon Force"])
    plt.ylim([0, 2])
    plt.show()

    return



if __name__ == "__main__":

    t = np.linspace(0, 1, 100)
    stim_duration = [[0.1, 0.6], [0.1, 0.105], [0.1, 1]]

    # for s in stim_duration:
    hill_type_model(t, stim_duration[0])


