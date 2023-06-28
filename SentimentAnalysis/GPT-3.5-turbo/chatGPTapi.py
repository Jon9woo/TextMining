import pandas as pd
from tqdm import tqdm
data = pd.read_csv("../processing_no_label_data.csv", index_col = 0)

data = data['split_sent']
data = data.tolist()

import openai
openai.api_key  = 'input openai key'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2, # this is the degree of randomness of the model's output # temperature, top-p는 모델의 창의성 통제 변인임. 
    )
    return response.choices[0].message["content"]

positive_example = '세원인텔리전스는 매트리스 범위에 국한하지 않고 일상 전 영역에서 수면 건강을 모니터링하는 AI 소프트웨어를 개발해 주목받고 있다'
negative_example = '클라우드를 활용하는 기업들이 늘어나면서 보안 설정과 공백을 노리는 사이버 위협이 늘어날 것이라는 진단이다'

outputList = []

for i in tqdm(range(len(data))):
    news_review = data[i]
    prompt = f"""

    긍정 예시 : '''{positive_example}'''
    부정 예시 : '''{negative_example}'''

    너는 결과값으로 숫자만 출력하는 라벨링 작업을 수행할거야.
    긍정 부정 중립 3가지 중 하나로 해당 문장의 감성을 분류해줘. 
    긍정일 경우 0, 중립일 경우 1, 부정일 경우 2
    여러 문장이 존재할 경우, 여러 문장을 한번에 판단해서 하나의 숫자를 출력해줘.
    don't print text, just print number.
    don't print 긍정, 부정, 중립, just print 0, 1, 2.

    리뷰할 텍스트: '''{news_review}'''
    """

    try :
        response = get_completion(prompt)
        outputList.append(response)
    except:
        outputList.append('error')

import pickle

# 파일 경로와 이름 설정
file_path = '../outputList.pickle'

# 리스트를 pickle 파일로 저장
with open(file_path, 'wb') as file:
    pickle.dump(outputList, file)