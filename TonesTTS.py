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
    while True:
        try:
            status = await fy.is_tts_job_ready(job_token)
            print(f"📊 Статус задачи: {status['state']['status']}")

            if status["state"]["status"] == "complete_success":
                break
            elif status["state"]["status"] == "complete_failure":
                print("❌ Сервер вернул ошибку при генерации речи.")
                return

            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Ошибка проверки статуса: {e}")
            return

    # Скачиваем аудиофайл
    print("\n📥 Загрузка готового аудиофайла...")
    try:
        audio_content = await fy.retreive_audio_file(job_token)
        output_file = "output.wav"

        with open(output_file, "wb") as f:
            f.write(audio_content)

        print(f"✅ Аудио успешно сохранено как: {output_file}")
    except Exception as e:
        print(f"❌ Ошибка загрузки аудио: {e}")


# Запуск
if __name__ == "__main__":
    asyncio.run(main())