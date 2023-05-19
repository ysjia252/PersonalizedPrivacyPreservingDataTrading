import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
from IncompleteInformationModel import IncompleteInformationModel
from CompleteInformationModel import CompleteInformationModel

mpl.rc('font',family='Times New Roman',size=20)
mpl.rc('lines', **{'linewidth':1.5,'markersize':5,'markeredgewidth':3.0})
mpl.rc('axes', linewidth=1.5,labelsize=22)
# mpl.rc('xtick',labelsize=16)
mpl.rc('xtick.major',width=2)
mpl.rc('xtick.minor',width=1.5,visible='True')
# mpl.rc('ytick',labelsize=16)
mpl.rc('ytick.major',width=2)
mpl.rc('ytick.minor',width=1.5,visible='True')
mpl.rc('legend',loc='best', frameon='True', framealpha=1,edgecolor='black', fancybox='False',fontsize=14)
mpl.rc('figure',figsize=(6.4,4.5))
mpl.rc('figure.subplot',left=0.18,right=0.95,bottom=0.16,top=0.95)
mpl.rc('savefig',format='eps')

if __name__=="__main__":
    trading_ic = IncompleteInformationModel()
    trading_c = CompleteInformationModel()

    trading_ic.setParameters(c=None)
    trading_ic.run()
    trading_ic.compute_r()
    trading_ic.compute_u()

    trading_c.list_c = trading_ic.list_c
    trading_c.dict_c = trading_ic.dict_c
    trading_c.personal_c = trading_ic.personal_c
    trading_c.m = trading_ic.m
    trading_c.delta_c = trading_ic.delta_c
    trading_c.Q = trading_ic.Q
    trading_c.run()
    trading_c.compute_r()
    trading_c.compute_u()

    x = np.arange(1, trading_ic.k+1)
    y_ic = trading_ic.u
    y_c = trading_c.u

    bar_width = 0.5
    plt.bar(x-bar_width/2, y_c, width=bar_width, label='Complete Information Model')
    plt.bar(x+bar_width/2, y_ic, width=bar_width, label='Incomplete Information Model', color='r')

    # 设置横坐标刻度间隔
    x_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)

    # plt.margins(0)
    # plt.subplots_adjust(bottom=0.15)
    plt.xlabel("Privacy Group")
    plt.ylabel("Utility of Data Owners")
    # plt.grid()
    plt.legend()

    for a, b in zip(x, y_c):
        plt.text(a-bar_width/2, b + 0.01, '%.0f' % b, ha='center', va='bottom', fontsize=11)
    for a, b in zip(x, y_ic):
        if b != 0:
            plt.text(a+bar_width/2, b + 0.01, '%.3f' % b, ha='center', va='bottom', fontsize=11)
        else:
            plt.text(a+bar_width/2, b + 0.01, '%.0f' % b, ha='center', va='bottom', fontsize=11)

    plt.show()