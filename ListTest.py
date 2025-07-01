import requests
import time

# === API URLs ===
FAKEYOU_TTS_JOB_URL = "https://api.fakeyou.com/tts/job "
FAKEYOU_JOB_STATUS_URL = "https://api.fakeyou.com/tts/job/ "

# === Публичный токен голоса Donald Trump ===
MODEL_TOKEN = "TM:92f9yjxj11mz"  # Токен голоса Trump'a


def create_tts_job(model_token, text):
    """Создаёт TTS задачу и возвращает job_token"""
    payload = {
        "model_token": model_token,
        "intext": text
    }
    response = requests.post(FAKEYOU_TTS_JOB_URL, json=payload)
    response.raise_for_status()
    return response.json()['job_token']


def wait_for_job(job_token):
    """Ожидает завершения задачи"""
    while True:
        response = requests.get(f"{FAKEYOU_JOB_STATUS_URL}{job_token}")
        response.raise_for_status()
        data = response.json()

        status = data['state']['status']
        if status == "complete_success":
            return True
        elif status == "complete_failure":
            return False
        time.sleep(2)


def download_audio(job_token, output_file="output.wav"):
    """Скачивает готовое аудио и сохраняет в файл"""
    audio_url = f"https://api.fakeyou.com/tts/job/ {job_token}/audio"
    response = requests.get(audio_url, stream=True)
    response.raise_for_status()

    with open(output_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    print(f"✅ Аудио сохранено как {output_file}")


def main():
    text = input("Введите текст для озвучивания: ")

    print("🔊 Создаём задачу генерации речи...")
    job_token = create_tts_job(MODEL_TOKEN, text)
    print(f"Задача создана. Job Token: {job_token}")

    print("⏳ Ожидаем завершения генерации...")
    success = wait_for_job(job_token)

    if not success:
        print("❌ Не удалось сгенерировать аудио.")
        return

    print("📥 Загружаем готовое аудио...")
    download_audio(job_token)


if __name__ == "__main__":
    main()