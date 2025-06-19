import os
import json
from dotenv import load_dotenv
import httpx
from loguru import logger

# Загрузка переменных окружения
load_dotenv()

MODEL_URI = os.getenv("MODEL_URI")
YANDEXGPT_API_KEY = os.getenv("YANDEXGPT_API_KEY")
YANDEXGPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

class YandexGPTApiService:
    def __init__(self):
        self.model_uri = MODEL_URI
        self.api_key = YANDEXGPT_API_KEY
        self.session_context = {}  # Хранение контекста для каждой сессии
        self.file_path = 'misc/prompt.json'
        self.maxTokens = 2000
        self.shiftTokens = self.maxTokens * 0.1

    def read_context_from_json(self, file_path: str):
        """
        Чтение контекста из JSON-файла.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                context = json.load(f)
                return context
        except FileNotFoundError:
            logger.error(f"Файл {file_path} не найден.")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON файла {file_path}: {e}")
            return {}

    async def get_response(self, session_id: str, prompt: str):
        """
        Асинхронный запрос к Yandex GPT API с учетом контекста.
        """
        url = YANDEXGPT_URL

        # Обновляем контекст для текущей сессии
        if session_id not in self.session_context:
            self.session_context[session_id] = self.read_context_from_json(self.file_path)
        self.session_context[session_id].append({"role": "user", "text": prompt})

        payload = {
            "modelUri": self.model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": 0.8,
                "maxTokens": self.maxTokens
            },
            "messages": self.session_context[session_id]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }

        logger.debug(f"Отправка запроса к YandexGPT с телом: {payload}")

        # Асинхронный запрос
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()

                # Извлекаем ответ и добавляем его в контекст
                gpt_response = result.get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "")
                self.session_context[session_id].append({"role": "assistant", "text": gpt_response})

                # Проверка на переполнение контекста
                if len(self.session_context[session_id]) > self.maxTokens:
                    self.session_context[session_id] = self.read_context_from_json(self.file_path).extend(self.session_context[session_id][-self.shiftTokens:])

                # logger.info(f"Ответ от YandexGPT: {gpt_response[0]}")
                return gpt_response
            except httpx.RequestError as e:
                logger.error(f"Ошибка при запросе к YandexGPT API: {e}")
                return "Ошибка при обращении к сервису YandexGPT."
            except Exception as e:
                logger.exception(f"Неизвестная ошибка при запросе к YandexGPT API: {e}")
                return "Неизвестная ошибка при обращении к сервису YandexGPT."

    async def process_request(self, session_id: str, user_request: str):
        """
        Обработка запроса пользователя с учетом идентификатора сессии.
        """
        logger.info(f"Получен запрос от пользователя: {user_request.text}")
        response = await self.get_response(session_id, user_request.text)
        return {"status": "success", "response": response}

