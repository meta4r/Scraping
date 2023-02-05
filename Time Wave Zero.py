import numpy as np
import matplotlib.pyplot as plt

 # TMK's Time Wave Zero Function

def time_wave_zero(t, omega=1.0, t0=0.0):
    return np.sin(omega * (t - t0))

t = np.linspace(0, 10, 1000)
y = time_wave_zero(t)

plt.plot(t, y)
plt.show()
