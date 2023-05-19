from scipy import optimize
import numpy as np
import math
import random
from collections import Counter


class DataTradingApproach:

    def __init__(self):
        self.n = 1000  # 参与用户数
        self.B = 8000  # 预算
        self.pi = 0.2  # 真实聚合结果
        self.k = 10  # 种类数
        self.list_c = []  # 隐私偏好
        self.dict_c = dict()  # 用字典存储c和下标
        self.personal_c = []  # 经过随机分配后每个用户的隐私偏好
        self.original_x = []  # 每个用户的原始答案
        self.perturbed_x = []  # 每个用户的扰动答案
        self.aggregation_pi_dir = 0  # 直接计数法得到的聚合结果
        self.aggregation_pi_mle = 0  # 基于分组加权的最大似然估计法得到的聚合结果
        self.m = []  # 每个组别的人数
        self.epsilon = []  # 隐私保护水平
        self.p = []  # 随机扰动概率
        self.r = []  # 报酬
        self.u = []  # 效用
        self.dict_cp = dict()  # 用于绑定c和p
        self.delta_c = [0]  # delta_ci=c_i-c_(i-1)
        self.Q = []  # 最终约束条件中的Q

    # ------------------------------------ 设置参数 ------------------------------------
    def setParameters(self, c):
        # 随机生成隐私偏好，并从小到大排序
        if c == None:
            self.list_c = []
            for i in range(self.k):
                self.list_c.append(np.random.uniform(5, 15))
        else:
            self.list_c = random.sample(c, self.k)
        self.list_c.sort()
        # print(self.list_c)

        # 记录每个隐私偏好c的下标
        for i in range(0, self.k):
            self.dict_c[self.list_c[i]] = i

        # 将用户随机分配到k个组中（等概率）
        self.personal_c = np.random.choice(self.list_c, self.n)
        cnt = Counter(self.personal_c)
        # 由于Counter()统计结果会直接去掉人数为0的组，此时会直接导致下面m数组元素的缺失，所以暂时用while循环保证每个组一定有人
        while len(cnt) != self.k:
            self.personal_c = np.random.choice(self.list_c, self.n)
            cnt = Counter(self.personal_c)

        # 统计每个组别的人数
        self.m = [value for key, value in sorted(cnt.items())]

        for i in range(1, self.k):
            self.delta_c.append(self.list_c[i] - self.list_c[i - 1])
        for i in range(0, self.k):
            if i == 0:
                self.Q.append(self.m[i] * self.list_c[i])
            else:
                self.Q.append(self.m[i] * self.list_c[i] + self.delta_c[i] * sum(self.m[0:i]))

    # ------------------------------------ 随机生成初始答案 ------------------------------------
    def setOriginal_x(self):
        # 根据pi随机初始化每个用户的原始答案{+1,-1}
        self.original_x = [1] * round(self.n * self.pi) + [-1] * int(self.n - round(self.n * self.pi))
        random.shuffle(self.original_x)

    # ------------------------------------ 目标函数 ------------------------------------
    def func(self):
        fun = lambda x: sum(self.m[i] * ((math.exp(x[i]) + 1) / (math.exp(x[i]) - 1)) ** 2 for i in range(0, self.k))
        return fun

    # ------------------------------------ 约束条件 ------------------------------------
    def con(self):
        e = 1e-10
        cons = [{'type': 'eq', 'fun': lambda x: sum(self.Q[i] * x[i] for i in range(0, self.k)) - self.B},
                {'type': 'ineq', 'fun': lambda x: x - e},
                {'type': 'ineq', 'fun': lambda x: [x[i] - x[i + 1] - 0.01 for i in range(0, self.k - 1)]}]
        return cons

    # ------------------------------------ 求解优化问题 ------------------------------------
    def resolve(self):
        cons = self.con()
        x0 = [1.0] * self.k
        res = optimize.minimize(self.func(), x0, method='SLSQP', constraints=cons)
        xx = 1.0
        while res.success == False:
            xx = xx + 0.5
            x0 = [xx] * self.k
            res = optimize.minimize(self.func(), x0, method='SLSQP', constraints=cons)
        return res

    # ------------------------------------ 计算随机扰动概率 ------------------------------------
    def compute_p(self):
        for i in range(0, self.k):
            self.p.append(math.exp(self.epsilon[i]) / (math.exp(self.epsilon[i]) + 1))
            self.dict_cp.update({self.list_c[i]: self.p[i]})

    # ------------------------------------ 随机响应算法 ------------------------------------
    def random_response(self, ori_ans, p):
        pr = random.random()
        if pr <= p:
            return ori_ans
        else:
            return -ori_ans

    # ------------------------------------ 用户执行随机响应 ------------------------------------
    def execute_random_response(self):
        for i in range(0, self.n):
            self.perturbed_x.append(1) if self.random_response(self.original_x[i], self.dict_cp[self.personal_c[i]]) == 1 else self.perturbed_x.append(-1)

    # ------------------------------------ 聚合算法1:直接统计 ------------------------------------
    def aggregate_1(self):
        perturbed_pi = self.perturbed_x.count(1) / self.n
        return perturbed_pi

    # ------------------------------------ 聚合算法2:采用自定义聚合统计算法 ------------------------------------
    def aggregate_2(self):
        nk = [0] * self.k
        for i in range(0, self.n):
            if self.perturbed_x[i] == 1:
                nk[self.dict_c[self.personal_c[i]]] = nk[self.dict_c[self.personal_c[i]]] + 1
        aggregated_res = 0
        for i in range(0, self.k):
            aggregated_res = aggregated_res + ((nk[i] + self.m[i] * (self.p[i] - 1)) / (2 * self.p[i] - 1))
        aggregated_res = aggregated_res / self.n
        return aggregated_res

    # ------------------------------------ 运行数据交易过程 ------------------------------------
    def run(self):
        # 为了保证对比实验中同一轮次各模型的参数一致，在执行run函数前单独执行setParameters函数
        # self.setParameters(c=None)
        self.setOriginal_x()
        res = self.resolve()
        self.epsilon = res.x
        self.compute_p()
        self.execute_random_response()
        self.aggregation_pi_dir = self.aggregate_1()
        self.aggregation_pi_mle = self.aggregate_2()