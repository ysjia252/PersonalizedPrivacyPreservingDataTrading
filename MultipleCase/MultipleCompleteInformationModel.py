from scipy import optimize
from MultipleDataTradingApproach import DataTradingApproach

class CompleteInformationModel(DataTradingApproach):
    # 重写约束条件
    def con(self):
        e = 1e-5
        cons = [{'type': 'eq', 'fun': lambda x: sum(self.m[i] * self.list_c[i] * x[i] for i in range(0, self.k)) - self.B},
                {'type': 'ineq', 'fun': lambda x: x - e},
                {'type': 'ineq', 'fun': lambda x: [x[i] - x[i + 1] - 0.01 for i in range(0, self.k - 1)]}]
        return cons

    # 计算报酬
    def compute_r(self):
        for i in range(0, self.k):
            self.r.append(self.list_c[i] * self.epsilon[i])
        # print("r: ", self.r)

    # 计算效用
    def compute_u(self):
        for i in range(0, self.k):
            self.u.append(self.r[i] - self.list_c[i] * self.epsilon[i])
        # print("u: ", self.u)

    # 测试激励相容性
    def testIC(self):
        for i in range(0, self.n):
            print("%d: %d(%d)" %(i+1, self.personal_c[i], self.dict_c[self.personal_c[i]]+1))
            for j in range(0, self.k):
                print(self.r[j] - self.personal_c[i] * self.epsilon[j])
