import asyncio
from fakeyou import AsyncFakeYou


async def main():
    fy = AsyncFakeYou()

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
    tts_job = await fy.make_tts_job(selected_token, text)

    # Ожидание завершения задачи
    while not await fy.is_tts_job_ready(tts_job.job_token):
        await asyncio.sleep(1)

    print("Генерация завершена.")

    # Получение и сохранение аудиофайла
    result = await fy.retreive_audio_file(tts_job.job_token)
    output_file = "output.wav"

    with open(output_file, "wb") as f:
        f.write(result.content)

    print(f"Аудио успешно сохранено как: {output_file}")


# Запуск асинхронного кода
if __name__ == "__main__":
    asyncio.run(main())