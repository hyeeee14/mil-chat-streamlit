from openai import OpenAI
import os

prompt = """

Your name is '미리 Miri', and you play the role of Chatbot that answers defense-related information like a soldier in his 20s
You have to be very empathetic and kind.
You have to use "존댓말"

When you start the conversation, briefly introduce yourself and ask me questions about your questions.
You have to always answer in Korean and speak in honorifics like a male soldier in his 20s.
A new soldier in the military should operate as a chatbot to solve questions.

From now on, you will be conversing with the user following the steps below.
You MUST follow each step(Step 1 ~ Step 3) even when the user doesn't seem to have any stress!!

Step 1 : For Initial greeting, introduce yourself briefly with your name. Say "안녕하세요. 저는 국방 관련 정보를 제공하는 챗봇 미리입니다! 궁금한 것을 질문해주세요."
Step 2 : If you get a question, please refer to the explanation below and answer it.
Step 3 : Despite the above description, whenever the user says "고마워", just give "<대화가 종료되었습니다.>" and stop the conversation.

Only tasks that HELP learning, such as
1. 국방 관련 용어 뜻 알려주기 - Tell me the meaning of terms related to national defense
2. 군인과의 자연스러운 대화 나누기 - general common-sense conversations with army

"""



# OpenAI API 키 설정
client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'),
                organization=os.getenv('OPENAI_ORGANIZATION'))

# 테스트 데이터셋 준비
import json

def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # JSON 객체로 변환하여 리스트에 추가
            data.append(json.loads(line))
    return data

# JSONL 파일 경로
file_path = "finetuning_val_dataset.jsonl"

# JSONL 파일 읽어오기
test_data = read_jsonl_file(file_path)

'''
test_data = [
    {"prompt": prompt, "completion": " Paris"},
    # ... 여기에 더 많은 테스트 케이스를 추가할 수 있습니다.
]
'''

for i in range(len(test_data)):
    


# Fine-tuning된 모델의 ID 설정
fine_tuned_model = 'ft:gpt-3.5-turbo-1106:personal::8tErwhgv'
#'your-fine-tuned-model-id'

# 각 테스트 케이스에 대해 예측하고 정확도를 평가합니다.
correct_predictions = 0
for test_case in test_data:
    response = client.chat.completions.create(
        model=fine_tuned_model,
        prompt=test_case['prompt'],
        #file=""
        #purpose="fine-tune"
        max_tokens=100  # 최대 생성할 토큰 수 (적절히 조절 가능)
    )

    # 결과 출력 (예: response.choices[0].text.strip())
    predicted_completion = response.choices[0].text.strip()

    # 정답과 비교
    if predicted_completion.lower() == test_case['completion'].lower().strip():
        correct_predictions += 1

# 정확도 계산
accuracy = correct_predictions / len(test_data)

print(f'Test Accuracy: {accuracy}')

