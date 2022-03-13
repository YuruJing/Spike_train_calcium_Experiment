from utilis import *
import pyqtgraph.exporters
import numpy as np
import matplotlib.pyplot as plt

# get the total time scale (20 mins)=60000ms
resolut = 10
te = 60000
resolut_scale = int(te/resolut)
p = 20
total_time_scale = np.arange(resolut_scale*p)

# plt spike train simulation
r_c = 0.5/1000
generate_spike = Generate_Spike(10, 25, 20, int(r_c), 0.2)
spike = generate_spike.Spike_train()
burst_plot = plot_window(x=total_time_scale, y=spike, width=1)
burst_plot.set_window(title="Spike train simulation in 20 mins", x_label="Time scale/10ms", y_label="The number of spike")

# plt kernel function with different m coefficient for tau2
labels = []
for i in range(4, 11):
    plt.plot(total_time_scale[:1000], kernel_fun(total_time_scale[:1000], 75, i))
    labels.append(r'm = % s' % i)

plt.legend(labels)
plt.title("kernel function (tau1 = 75 /10ms)")
plt.xlabel("Time scale/10ms")
plt.savefig("kernel_diff_m.png")
plt.show()

# plt kernel function with different time constant, tau1
label2 = []
tau_collect = [75, 125, 200]
for j in tau_collect:
    plt.plot(total_time_scale[:1000], kernel_fun(total_time_scale[:1000], j, 4))
    label2.append(r'tau1 = % s' % j)

plt.legend(label2)
plt.title("kernel function with different tau1 (m=4)")
plt.xlabel("Time scale/10ms")
plt.savefig("kernel_diff_tau.png")
plt.show()
