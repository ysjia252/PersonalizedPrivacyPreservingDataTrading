import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from IncompleteInformationModel import IncompleteInformationModel

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
    trading_ic.setParameters(c=None)
    trading_ic.run()
    trading_ic.compute_r()
    trading_ic.compute_u()

    x = range(1, trading_ic.k+1)
    y = trading_ic.testIC()

    # k=10 取3,5,7组
    plt.plot(x, y[2], label='Type-3', color='r', marker='v', linestyle='-')
    plt.plot(x, y[4], label='Type-5', color='b', marker='^', linestyle='--')
    plt.plot(x, y[6], label='Type-7', color='g', marker='s', linestyle='-.')
    plt.vlines(x=3, ymin=min(y[6]) - 0.5, ymax=y[2][2], lw=1, colors='r', linestyles=':')
    plt.vlines(x=5, ymin=min(y[6]) - 0.5, ymax=y[4][4], lw=1, colors='b', linestyles=':')
    plt.vlines(x=7, ymin=min(y[6]) - 0.5, ymax=y[6][6], lw=1, colors='g', linestyles=':')

    plt.ylim(min(y[6]) - 0.5, max(y[2]) + 0.5)

    # 设置横坐标刻度间隔
    x_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)

    plt.margins(0)
    # plt.subplots_adjust(bottom=0.15)
    plt.xlabel("Type of Contracts")
    plt.ylabel("Utility of Data Owners")
    # plt.grid()  # 添加网格
    plt.legend()
    plt.show()