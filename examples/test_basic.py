from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

import os

from dotenv import load_dotenv

# 加载环境变量（如果使用 .env 文件）
load_dotenv()

# 定义测试用例
test_case = LLMTestCase(
    input="什么是深度学习？",
    actual_output="深度学习是机器学习的一个子领域，基于人工神经网络...",
    expected_output="深度学习是机器学习的分支，使用多层神经网络来学习数据的层次化表示。",
    context=["深度学习是机器学习的一个子集，灵感来自人脑的神经网络结构。"]
)


# 定义评估指标
faithfulness = FaithfulnessMetric()
relevancy = AnswerRelevancyMetric()



# 运行测试
if __name__ == "__main__":
    assert_test(
        test_case=test_case,
        metrics=[faithfulness, relevancy]
    )
