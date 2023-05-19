# PersonalizedPrivacyPreservingDataTrading
## BinaryCase（二值问题）/MultipleCase（多值问题）
1. DataTradingApproach.py中包括了参数设置、用户模拟数据生成、随机响应机制、求解优化问题、聚合算法等函数，其余模型都继承自该类
2. CompleteInformationModel.py, IncompleteInformationModel.py分别对应完全信息和不完全信息场景下的模型
3. ExperimentPPL.py, ExperimentIR.py, ExperimentIC.py分别验证了文中的单调性、个体理性、激励相容性
4. RunModel.py在保证参数一致的条件下分别在完全信息和不完全信息场景下运行了数据交易过程
