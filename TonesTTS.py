import asyncio
from fakeyou import AsyncFakeYou


async def main():
    # Создаем экземпляр AsyncFakeYou
    fy = AsyncFakeYou()

    # Получаем список голосов
    voices = await fy.list_voices()

    # Выводим все доступные названия голосов
    print("Доступные голоса:")
    for i, title in enumerate(voices.title):
        print(f"{i}: {title}")

    # Выбор голоса по номеру
    choice = int(input("Введите номер голоса для использования: "))
    selected_title = voices.title[choice]
    selected_token = voices.modelTokens[choice]

    print(f"Выбран голос: {selected_title} (Token: {selected_token})")

    # Ввод текста для озвучивания
    text = input("Введите текст для преобразования в речь: ")

    # Генерация аудио
    result = await fy.rapid_tts(selected_token, text)

    # Сохраняем файл
    output_file = "output.wav"
    with open(output_file, "wb") as f:
        f.write(result.content)

    print(f"Аудио успешно сохранено как: {output_file}")


# Запуск
if __name__ == "__main__":
    asyncio.run(main())