import json
from collections import deque

from agents.scripter import Scripter
from agents.writer import Writer
from model.mistral import get_ans_on_question


class Coordinator:
    def __init__(self, max_messages=10):
        """
        Инициализация класса Coordinator.

        :param max_messages: Максимальное количество сообщений для хранения в очереди.
        """
        self.writer = Writer()
        self.scripter = Scripter()
        self.system_message = {"role": "system",
                               "content": """ Ты координатор других агентов. 
                                              Твоя задача по запросу пользователя определить какие агенты нужны для задачи и составить для них запросы.
                                              После получения от них ответа, ты должен понять  можно ли  отправить ответ пользователю или надо использовать агентов ещё.
                                              Помни что пользователь чаще всего говорит про одну и ту же историю.
                                              Ты не можешь отдать юзеру сообщение длинее 4 096 символов - иначе будет ошибка.
                                              
                                              Список Агентов:
                                              Агент 1 - name:writer. Его задача придумывать основной костяк сюжета,персонажей, содержания  сцен.
                                              Агент 2 - name:scripter. Его задача расписывать сцены по кадрова в формате: текст, описание картинки, выборы. Результат его работы передается api агенту для реализации игры. Если не надо подробное описание сцен, то не стоит использовать.Точно необходим для работы api agent.
                                                                                            
                                              Формат твоего ответа:
                                              {"type_to":"user or agent",
                                               "name_to":"user word or agent name"
                                               "text": " содержание сообщения - результат работы пользователю или команда агенту"}
                                               
                                              Примеры гиппотетических запросов пользователя - не его сообщения:
                                              user: придумай сказку про жирафа
                                              assistent:
                                              {"type_to":"agent",
                                               "name_to":"writer"
                                               "text": "В данный момент твоя задача: предоставить лишь основные идеи кратко, без сильной детализации. Пользователь сказал: придумай сказку про жирафа"} 
                                               
                                               agent writter: Хорошо, вот простейший сюжет сказки про жирафа- жираф жил-жил и захотел стать космонавтом, пройдя много испытаний у него получилось долететь до луны.
                                               assistent:
                                              {"type_to":"user",
                                               "name_to":"user"
                                               "text": "Ваша сказка готова - простейший сюжет сказки про жирафа- жираф жил-жил и захотел стать космонавтом, пройдя много испытаний у него получилось долететь до луны. "} 
                                              """}
        self.messages = deque(maxlen=max_messages)

    def logic_coordinator(self,text):
        user_message = {
            "role": "user",
            "content": f"Это сообщение пользователя: {text}"

        }
        self.messages += [user_message]
        messages = [self.system_message] + list(self.messages)
        message = get_ans_on_question(messages, out_type='json_object')
        print(message.choices[0].message)
        message = message.choices[0].message
        json_ans = json.loads(message.content)
        type_to = json_ans["type_to"]
        while type_to != 'user':
            agent_ans = self.get_ans_from_agent(json_ans["text"], json_ans["name_to"])
            user_message = {
                "role": "user",
                "content": f"Это сообщение от агента: '{agent_ans.content}'. Hа вопрос {json_ans['text']}"
            }
            print('start check')
            messages += [user_message]
            message = get_ans_on_question(messages, out_type='json_object')
            message = message.choices[0].message
            print(message)
            json_ans = json.loads(message.content)
            type_to = json_ans["type_to"]
        self.messages += [message]
        print(message.content)
        return json.loads(message.content)['text']

    def get_ans_message_user(self, text, try_error=1):
        try:
            return self.logic_coordinator(text)
        except:
            self.messages = deque(list(self.messages)[-2:])
            if try_error > 0:
                return self.get_ans_message_user(text, try_error=0)
            else:
                return 'технические неполадки'



    def get_ans_from_agent(self, task, agent):
        message = {
                "role": "user",
                "content": f"Твоя задача : {task}"

            }
        if agent == 'writer':
            ans = self.writer.get_ans(message)
        if agent == 'scripter':
            ans = self.scripter.get_ans(message)
        return ans
