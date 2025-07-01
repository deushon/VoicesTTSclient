import asyncio
from fakeyou import AsyncFakeYou


async def main():
    fy = AsyncFakeYou()
    # Call the login method with email and password and await the result
    login = await fy.login("mihandr1@mail.ru", "199621368m")

    # Print the username of the logged-in user
    print("Logged in as:", login.username)
    # Получаем список всех голосов
    voices = await fy.list_voices()

    # Поиск голоса по названию
    search_term = input("Введите название голоса (или часть названия): ").lower()
    matching_indices = [
        i for i, title in enumerate(voices.title) if search_term in title.lower()
    ]

    if not matching_indices:
        print("Голос не найден.")
        return

    # Выбираем первый совпадающий голос
    index = matching_indices[0]
    selected_title = voices.title[index]
    selected_token = voices.modelTokens[index]

    print(f"Выбран голос: {selected_title} (Token: {selected_token})")

    # Ввод текста для озвучивания
    text = input("Введите текст для преобразования в речь: ")

    # Создание TTS задачи
    print("Создаём TTS-задачу...")
    tts_job = await fy.make_tts_job(selected_token, text)

    if tts_job is None:
        print("Ошибка: Не удалось создать TTS-задачу. Возможно, указан неверный токен.")
        return

    print("Ожидание завершения генерации...")

    # Ожидание завершения задачи
    while not tts_job.is_ready():
        await asyncio.sleep(1)

    print("Генерация завершена.")

    # Получение и сохранение аудиофайла
    audio_content = await tts_job.audio_content()
    output_file = "output.wav"

    with open(output_file, "wb") as f:
        f.write(audio_content)

    print(f"Аудио успешно сохранено как: {output_file}")


# Запуск
if __name__ == "__main__":
    asyncio.run(main())