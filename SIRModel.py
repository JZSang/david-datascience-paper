import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class SIRModel(object):

    def __init__(self, N, days):
        self.N = N
        self.I0, self.R0 = 1, 0
        self.S0 = N - self.I0 - self.R0
        self.t = np.linspace(0, days-1, days)
        self.beta, self.gamma = 0.2, 1./10
        self.S, self.I, self.R = None, None, None
        self.changed = True

    def _deriv(self, y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    def integrate(self):
        self.changed = False
        y0 = self.S0, self.I0, self.R0
        ret = odeint(self._deriv, y0, self.t, args=(
            self.N, self.beta, self.gamma))
        self.S, self.I, self.R = ret.T

    def set_contact_rate(self, beta):
        self.beta = beta

    def set_mean_recovery_rate(self, gamma):
        self.gamma = gamma


sir = SIRModel(1000, 15)
print(sir.t)
