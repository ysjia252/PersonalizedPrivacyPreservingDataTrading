from MultipleIncompleteInformationModel import IncompleteInformationModel
from MultipleCompleteInformationModel import CompleteInformationModel

if __name__=="__main__":
    # 运行不完全信息模型
    print("============= IncompleteInformationModel =============")
    trading_ic = IncompleteInformationModel()
    trading_ic.setParameters(c=None)
    trading_ic.run()
    print("c: ", trading_ic.list_c)
    print("m: ", trading_ic.m)
    print("epsilon: ", trading_ic.epsilon)
    print("p: ", trading_ic.p)
    print("original_result: ", trading_ic.pi)
    print("aggregation_result (dir): ", trading_ic.aggregation_pi_dir)
    print("aggregation_result (mle): ", trading_ic.aggregation_pi_mle)

    # 运行完全信息模型
    print("============= CompleteInformationModel =============")
    trading_c = CompleteInformationModel()
    # 为了便于对比，此处令两种场景下基本参数一致，不再执行setParameters函数
    trading_c.list_c = trading_ic.list_c
    trading_c.dict_c = trading_ic.dict_c
    trading_c.personal_c = trading_ic.personal_c
    trading_c.m = trading_ic.m
    trading_c.delta_c = trading_ic.delta_c
    trading_c.Q = trading_ic.Q
    trading_c.run()
    print("epsilon: ", trading_c.epsilon)
    print("p: ", trading_c.p)
    print("original_result: ", trading_c.pi)
    print("aggregation_result (dir): ", trading_c.aggregation_pi_dir)
    print("aggregation_result (mle): ", trading_c.aggregation_pi_mle)