#1. 라이브러리 가져오고 api key를 환경 변수에서 가져오기
# UI 추가하기
# -0) 라이브러리 추가하기 : streamlit
# -1) model 선택하기 : st.sidebar / st.selectbox
# -2) prompt 작성하기 : st.text_area
# -3) 이미지 업로드하기 : st.file_uploader
# -4) 업로드한 이미지 보여주기 : st.image
# -5) 분류 실행하기 : st.button /st.spinner
# -6) 결과 출력하기 : st.write / st.code

#1. 라이브러리 가져오고 api key를 환경 변수에서 가져오기
import os
from PIL import Image
import google.genai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# 1. 클라이언트 생성 (API 키 설정)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

#2.모델이 이미지 분류 요청 함수 정의하기
# client 객체의 models.generate_content 사용
def classify_image(prompt, image, model_name):
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=[prompt, image]
    )
    return response.text
    
    
#3. 프롬프트 선언하고 이미지 분류 실행하기
# gemini에게 보낼 프롬프트 정의
prompt = """
영상을 보고 다음 보기 내용이 포함되면 1, 포함되지 않으면 0으로 분류해줘.
보기 = [건축물, 바다, 산]
JSON format으로 키는 'building', 'sea', 'mountain'으로 하고 각각 건축물, 바다, 산에 대응되도록 출력해줘.
자연 이외의 건축물이 조금이라도 존재하면 'building'을 1로, 물이 조금이라도 존재하면 'sea'을 1로, 산이 조금이라도 보이면 'mountain'을 1로 설정해줘.
markdown format은 포함하지 말아줘.
"""

#1. 라이브러리 가져오고 api key를 환경 변수에서 가져오기
# UI 추가하기
# -0) 라이브러리 추가하기 : streamlit
# -1) model 선택하기 : st.sidebar / st.selectbox
# -2) prompt 작성하기 : st.text_area
# -3) 이미지 업로드하기 : st.file_uploader
# -4) 업로드한 이미지 보여주기 : st.image
# -5) 분류 실행하기 : st.button /st.spinner
# -6) 결과 출력하기 : st.write / st.code



st.set_page_config(
    page_title="image Classification- OpenAI",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title('이미지 분류기- gemini')
# -1) model 선택하기 : st.sidebar / st.selectbox
with st.sidebar:
    model = st.selectbox('모델 선택', 
                         options=['gemini-2.0-flash', 'gemini-2.0-flash-mini'],
                         index=0)
# -2) prompt 작성하기 : st.text_area
prompt = st.text_area('프롬프트 입력', value=prompt, height=200)
# -3) 이미지 업로드하기
uploaded_file = st.file_uploader('이미지 업로드', type=['png', 'jpg', 'jpeg'])

# -4) 업로드한 이미지 보여주기
if uploaded_file:
    img = Image.open(uploaded_file)
    # 최신 버전에서는 use_container_width=True를 권장합니다.
    st.image(img, caption='업로드한 이미지', use_container_width=True)

    # -5) 분류 실행하기 (이 줄의 시작 위치가 img = Image.open... 과 수직으로 딱 맞아야 합니다)
    if st.button('분류 실행'): 
        with st.spinner('분류 중...'):
            # 상단에서 선택한 model 변수를 사용합니다.
            response = classify_image(prompt, img, model)
            
            # -6) 결과 출력하기
            st.subheader('분류 결과')
            st.code(response)