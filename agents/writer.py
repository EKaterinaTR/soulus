from collections import deque

from model.mistral import get_ans_on_question


class Writer:
    def __init__(self, max_messages=5):
        """
        Инициализация класса Coordinator.

        :param max_messages: Максимальное количество сообщений для хранения в очереди.
        """
        self.name = 'writer'
        self.description = 'Задача - придумывать основной костяк сюжета,персонажей, содержания  сцен.'
        self.system_message = {"role": "system",
                               "content": """ Ты креативный писатель. 
                                                Твоя задача придумать и дорабатыввать сюжет для визуальной новеллы под предпочтении пользователя.
                                                Также ты должен мочь отвечать уже по предуманому тобой.
                                                Чаще всего пользователь не отказывается от истории - если есть правки или уточнения они относятся к предыдущим сообщениям. Если не сказано обратное. 
                                                
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

