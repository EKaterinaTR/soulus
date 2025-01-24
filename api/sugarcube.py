import requests

# Задайте URL вашего API SugarCube
BASE_URL = "http://localhost:your_port_here/sugarcube"  # Замените на ваш адрес


# Функция для создания истории
def create_story(story_name):
    url = f"{BASE_URL}/stories"
    data = {
        "name": story_name,
        "description": "Описание вашей истории."
    }

    response = requests.post(url, json=data)

    if response.status_code == 201:
        print("История успешно создана:", response.json())
        return response.json()  # Возвращаем созданную историю
    else:
        print("Ошибка при создании истории:", response.text)
        return None


# Функция для создания сцены
def create_scene(story_id, scene_name):
    url = f"{BASE_URL}/stories/{story_id}/scenes"
    data = {
        "name": scene_name,
        "content": "Содержимое вашей сцены."
    }

    response = requests.post(url, json=data)

    if response.status_code == 201:
        print("Сцена успешно создана:", response.json())
        return response.json()  # Возвращаем созданную сцену
    else:
        print("Ошибка при создании сцены:", response.text)
        return None


# Функция для установки порядка сцен
def set_scene_order(story_id, scene_ids):
    url = f"{BASE_URL}/stories/{story_id}/scenes/order"
    data = {
        "scene_ids": scene_ids
    }

    response = requests.put(url, json=data)

    if response.status_code == 200:
        print("Порядок сцен успешно обновлён.")
    else:
        print("Ошибка при обновлении порядка сцен:", response.text)


# Пример использования
if __name__ == "__main__":
    # Создаём историю
    story = create_story("Моя первая история")

    if story:
        story_id = story['id']

        # Создаём сцены
        scene1 = create_scene(story_id, "Сцена 1")
        scene2 = create_scene(story_id, "Сцена 2")

        if scene1 and scene2:
            # Устанавливаем порядок сцен
            set_scene_order(story_id, [scene1['id'], scene2['id']])
