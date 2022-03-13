import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import numpy as np
import random
from scipy.signal import convolve


# generate the burst points in the given time period
def burst_fun(resolut, nums_bin, periods):
    """
        Arguments:
        resolut: each bin_size
        nums_bin: the total number of bins emerge in each brust
        periods: the total number of periods (1 min per period)

        Return:
        total_bins: the total bins' value during all periods' time scale
        """
    # initialization (10ms)
    sin_period = 60000  # the single period conversion (1 min = 60,000ms)
    te = int(sin_period / resolut)  # single period respect to the given resolution

    # initialize the value of each bin
    total_bins = np.zeros((te * periods))

    # create the burst process (<250ms) = 25 bins
    for i in range(periods):
        # random index for the chosen time to burst
        t0_index, t1_index = np.random.randint(0 + te * i, te + te * i, size=2)
        # the difference between 2 brust's time duration should be greater than 250 ms (total bins duration) 25 bins
        while abs(t1_index - t0_index) <= nums_bin:
            t0_index, t1_index = np.random.randint(0 + te * i, te + te * i, size=2)

        # resetting the value of bins when they burst (burst bin value = 1)
        total_bins[t0_index:t0_index + nums_bin] = 1
        total_bins[t1_index:t1_index + nums_bin] = 1

    return total_bins


# Spike Train simulation
class Generate_Spike:
    def __init__(self, resolut, nums_bin, periods, r_0, alpha):
        """
        Arguments:
        resolut: resolution of the signal (each bin size 10ms)
        nums_bin: the total number of bins emerge in each brust
        periods: the total number of periods (1 min per period)
        r_0: base firing rate (HZ) conversion to current unit ms
        alpha: burstness of neuron

        Return:
        firate: the firing rate for all the spike
        S_t: spike generation
        """
        self.resolut = resolut
        self.nums_bin = nums_bin
        self.periods = periods
        self.r_0 = r_0
        self.alpha = alpha

    def firate_fun(self):
        # convert r0 to the current resolution
        r_0 = self.r_0 * self.resolut
        firate = r_0 + self.alpha * burst_fun(self.resolut, self.nums_bin, self.periods)
        return firate

    def Spike_train(self):
        # generate random variables from poisson distribution when its mu = firate_fun
        mu = self.firate_fun()
        S_t = np.random.poisson(mu)  # poisson.rvs(mu)
        return S_t


# plot spikes
class plot_window:
    def __init__(self, x, y, width):
        """
        Arguments：
        :param x: x data for the window plot
        :param y: y data for the window plot
        :param width: the bar plot width
        """
        self.x = x
        self.y = y
        self.width = width

    def set_window(self, title, x_label, y_label, bool_param=False):
        # create the window
        window = pg.plot()

        # setting the window
        window.setTitle(title, color='008080', size='12pt')
        window.setBackground('w')
        window.showGrid(x=bool_param, y=bool_param)
        window.setGeometry(200, 200, 1200, 1000)
        window.setLabel("left", y_label, size='8pt')
        window.setLabel("bottom", x_label, size='8pt')

        # bar plot
        bar_plot = pg.BarGraphItem(x=self.x, height=self.y, width=self.width, brush='r')
        # add bar plot in the window
        window.addItem(bar_plot)
        # export and save the plot
        exporter = pg.exporters.ImageExporter(window.scene())
        exporter.export("spike_simulation.png")
        QtGui.QApplication.instance().exec_()


# The realistic kernel function (differences between exponential decay kernel functions)
def kernel_fun(t, tau1, m):
    """
    Arguments:
    :param t: total time scale
    :param tau1: time constant coefficient
    :param m: adjusting factor
    :return:
    k_t: kernel value
    """
    # initialize the kernel to the fluorescence rise time
    tau2 = tau1 / m
    k_t = np.exp(-t / tau1) - np.exp(-t / tau2)
    return k_t


# create the calcium trace
class cal_trace:
    def __init__(self, train_spike, t, tau1, m):
        """
        Arguments:
        :param train_spike: spike_train simulation
        :param t: total time scale
        :param tau1: time constant coefficient
        :param m: adjusting factor
        """
        self.train_spike = train_spike
        self.t = t
        self.tau1 = tau1
        self.m = m

# generate the random amplitude coefficient from 0 to 0.02
    def amp(self):
        beta = round(random.random() * 0.02, 4)
        while beta == 0:
            beta = round(random.random() * 0.02, 4)
        return beta

# generate the random noise
    def noise_fun(self):
        noise = np.random.normal(0, 1, len(self.t))
        beta = self.amp()
        noise = beta * noise
        return noise

# generate the final calcium traces
    def total_trace(self):
        # generate kernel function
        kernel = kernel_fun(self.t, self.tau1, self.m)
        # convolve kernel and spike
        conv = convolve(self.train_spike, kernel, 'same')
        # generate calcium trace (kernel&spike convolution and noise)
        return conv + self.noise_fun()


