import os
import time
from mistralai import Mistral, ResponseFormat

model = "mistral-large-latest"

def get_ans_on_question(messages: list, out_type: ResponseFormat = 'text'):
    m_api_key = os.getenv('m_api_key')
    time.sleep(5)
    mc_client = Mistral(api_key=m_api_key)
    chat_response = mc_client.chat.complete(
        model=model,
        messages=messages,
        response_format={"type": out_type }
    )
    return chat_response
