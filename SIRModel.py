import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class SIRModel(object):

    def __init__(self, N, days, I0=1, R0=0, contact_rate=0.2, mean_recovery_rate=1./10):
        self.N = N
        self.I0, self.R0 = I0, R0
        self.S0 = N - self.I0 - self.R0
        self.t = np.linspace(0, days-1, days)
        self.beta, self.gamma = contact_rate, mean_recovery_rate
        self.S, self.I, self.R = None, None, None
        self.changed = True

    def _deriv(self, y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    def integrate(self):
        y0 = self.S0, self.I0, self.R0
        ret = odeint(self._deriv, y0, self.t, args=(
            self.N, self.beta, self.gamma))
        self.S, self.I, self.R = ret.T

    def set_contact_rate(self, beta):
        self.beta = beta

    def set_mean_recovery_rate(self, gamma):
        self.gamma = gamma


sir = SIRModel(1000, 15, R0=1)

print(sir.t)
