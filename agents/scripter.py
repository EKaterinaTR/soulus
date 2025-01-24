from collections import deque

from model.mistral import get_ans_on_question


class Scripter:
    def __init__(self, max_messages=5):
        """
        Инициализация класса

        :param max_messages: Максимальное количество сообщений для хранения в очереди.
        """
        self.name = 'scripter'
        self.description = ''
        self.system_message = {"role": "system",
                               "content": """   Ты управляешь сценами/набросками сцен
                                                Ты можешь придумывать их, изменять, убирать из повествования.
                                                Сцена это  id, текст, описание картинки и выборы:
                                                ID - уникальный идентификатор сцены.
                                                Текст - описывающий что происходит, реплики героев, события. Его не должно быть много. Если его много стоит задуматься над тем чтобы разбить сцену на 2.
                                                Описание картинки - то что по идеи должен увидит пользователь в сцене - это должен быть статичный момент.
                                                Выборы - то что может выбрать игрок в визуальной новелле, при их выборе открывается другая сцена. У выбора есть id(сцена куда ведет выбор), и есть текст, что должен сделать герой чтобы перейти к сцене.
                                                
                                                Пример ответа и формат, придерживайся его:
                                                
                                                ###Сцена(id=1)
                                                Ты сладко спал, но неожидано прозвенел будилник, ты открыл глаза и увидел,:
                                                *****
                                                Телефон крупным планом, время 6:40. Размыто по краям. 
                                                *****
                                                
                                                ['спать дальше',id=2]
                                                ['встать',id=3]
                                                
                                                ###Сцена(id=2)
                                                Ты закрыл глаза но сон никак не приходит:
                                                *****
                                                Все черное 
                                                *****
                                                
                                                ['спать дальше',id=2]
                                                ['всё таки встать',id=4]

                                              """}
        self.messages = deque(maxlen=max_messages)

    def get_ans(self, task_message):
        self.messages += [task_message]
        messages = [self.system_message] + list(self.messages)
        print(self.name, messages)
        print(len(messages))
        print('---------------')
        message = get_ans_on_question(messages)
        message = message.choices[0].message
        print(self.name, message)
        self.messages.append(message)
        return message