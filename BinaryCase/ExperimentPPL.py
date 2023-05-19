import matplotlib as mpl
import matplotlib.pyplot as plt
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
    trading_c.list_c = trading_ic.list_c
    trading_c.dict_c = trading_ic.dict_c
    trading_c.personal_c = trading_ic.personal_c
    trading_c.m = trading_ic.m
    trading_c.delta_c = trading_ic.delta_c
    trading_c.Q = trading_ic.Q
    trading_ic.run()
    trading_c.run()

    x = range(1, trading_ic.k+1)
    y_ic = trading_ic.epsilon
    y_c = trading_c.epsilon

    plt.plot(x, y_c, label='Complete Information Model', color='b', marker='v')
    plt.plot(x, y_ic, label='Incomplete Information Model', color='r', marker='^')

    plt.ylim(min(y_ic) - 0.01, max(y_c) + 0.01)  # 设置纵坐标范围

    plt.margins(0)
    # plt.subplots_adjust(bottom=0.15)
    plt.xlabel("Privacy Group")
    plt.ylabel("PPL %c" %chr(949))
    # plt.grid()  # 添加网格
    plt.legend()
    plt.show()