###############################################################################################
# API Key 입력 #
###############################################################################################
# importing SKLLMConfig to configure OpenAI API (key and Name)
from skllm.config import SKLLMConfig

# Set your OpenAI API key
SKLLMConfig.set_openai_key("input openai api key")

# Set your OpenAI organization (optional)
SKLLMConfig.set_openai_org("input openai organization")
###############################################################################################




###############################################################################################
# Data 불러오기 #
###############################################################################################
import pandas as pd
from tqdm import tqdm
data = pd.read_csv("../textrank_results_0605.csv", index_col = 0)
#start index
a = 0 
#end index
b = len(data)
data = data[a:b]
data2 = data['summarization']
###############################################################################################



###############################################################################################
# 3 shot 만들기 (1,1,1) #
###############################################################################################
X, y = ['블룸버그통신 등 외신에 따르면 라스 모래비 테슬라 차량 엔지니어링 부사장은 1일 미 텍사스주 테슬라 기가팩토리에서 열린 투자자의 날 행사에서 차세대 모델의 조립비용이 현재 테슬라 모델 중 가장 저렴한 모델3 스포츠유틸리티차 모델Y와 비교했을 때 절반 수준이 될 것으로 기대한다고 밝혔다',
     '챗위안은 또 중국 경제의 문제에 대한 질문에 투자 부족 주택 거품 환경 오염 기업 운영 효율성 감소 등을 지적하며 중국 경제의 전망은 낙관할 여지가 없다 는 식으로 답변했다',
     '한국갤럽이 지난 7 9일 전국 만 18세 이상 남녀 1천2명을 대상으로 조사한 결과 윤 대통령의 직무 수행 긍정 평가는 32 부정 평가는 59 로 각각 집계됐다'],['positive','negative','neutral']
###############################################################################################



###############################################################################################
# model fitting #
###############################################################################################
from skllm import ZeroShotGPTClassifier

clf = ZeroShotGPTClassifier(openai_model="gpt-3.5-turbo")
clf.fit(X,y)
###############################################################################################





###############################################################################################
# predicting the labels #
###############################################################################################
labels = clf.predict(data2)
###############################################################################################





###############################################################################################
# saving the results #
###############################################################################################
data['label'] = labels
data.to_csv("../outputSentiment.csv")
###############################################################################################