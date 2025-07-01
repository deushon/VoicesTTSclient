import asyncio
from fakeyou import AsyncFakeYou


async def main():
    # Инициализируем клиент
    fy = AsyncFakeYou()

    # Авторизация
    try:
        login = await fy.login("mihandr1@mail.ru", "199621368m")
        print(f"✅ Успешно вошли как: {login.username}")
    except Exception as e:
        print(f"❌ Ошибка авторизации: {e}")
        return

    # Получаем список всех голосов
    try:
        voices = await fy.list_voices()
        print(f"📚 Загружено {len(voices.title)} голосов")
    except Exception as e:
        print(f"❌ Не удалось получить список голосов: {e}")
        return

    # Поиск голоса по части названия
    search_term = input("🔎 Введите название голоса (или часть): ").lower()
    matching_indices = [
        i for i, title in enumerate(voices.title) if search_term in title.lower()
    ]

    if not matching_indices:
        print("❌ Голос не найден")
        return

    index = matching_indices[0]
    selected_title = voices.title[index]
    selected_token = voices.modelTokens[index]

    print(f"\n🎯 Выбран голос: {selected_title} (Token: {selected_token})")

    # Ввод текста для озвучивания
    text = input("📝 Введите текст для преобразования в речь: ")

    # Создание задачи TTS
    print("\n🔊 Создаю задачу генерации речи...")
    try:
        job_token = await fy.make_tts_job(text=text, ttsModelToken=selected_token)
        print(f"📨 Получен Job Token: {job_token}")
    except Exception as e:
        print(f"❌ Ошибка при создании задачи: {e}")
        return

    # Проверяем статус задачи
    print("\n⏳ Ожидание завершения генерации...")


    try:
        wav  = await fy.tts_poll(job_token)
        audio_content = wav.content
            # Скачиваем аудиофайл
        print("\n📥 Загрузка готового аудиофайла...")
        output_file = "output.wav"

        with open(output_file, "wb") as f:
            f.write(audio_content)

        print(f"✅ Аудио успешно сохранено как: {output_file}")
    except Exception as e:
        print(f"❌ Ошибка загрузки аудио: {e}")


# Запуск
if __name__ == "__main__":
    asyncio.run(main())