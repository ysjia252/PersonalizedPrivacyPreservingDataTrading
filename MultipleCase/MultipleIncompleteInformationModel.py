from MultipleDataTradingApproach import DataTradingApproach

class IncompleteInformationModel(DataTradingApproach):
    # 计算报酬
    def compute_r(self):
        for i in range(0, self.k):
            self.r.append(self.list_c[i] * self.epsilon[i])
            if i != self.k - 1:
                for j in range(i + 1, self.k):
                    self.r[i] = self.r[i] + self.delta_c[j] * self.epsilon[j]
        # print("r: ", self.r)

    # 计算效用
    def compute_u(self):
        for i in range(0, self.k):
            self.u.append(self.r[i] - self.list_c[i] * self.epsilon[i])
        # print("u: ", self.u)

    # 测试激励相容性
    def testIC(self):
        ic = [[] for i in range(self.k)]
        for i in range(0, self.k):
            # print("=====", i, "=====")
            for j in range(0, self.k):
                utility = self.r[j] - self.list_c[i] * self.epsilon[j]
                ic[i].append(utility)
                # print(utility)
        return ic
