
Навигатор Данных 🧠🔍

ИИ-помощник для интеллектуального анализа данных и бизнес-логики ИС ОДС


![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-green.svg)
![FastApi](https://img.shields.io/badge/FastAPI-0.104-teal.svg)
![Mit](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 О проекте
Навигатор Данных — это интеллектуальная система на основе ИИ, которая преобразует сложные технические метаданные баз данных в простые и понятные ответы на естественном языке. 
Система предназначена для аналитиков, разработчиков и бизнес-пользователей, работающих с enterprise-системами.


## 🛠️ Технологический стек
Backend
- FastAPI — современный ASGI фреймворк
- ChromaDB — векторная база данных для RAG
- SQLAlchemy — ORM для работы с PostgreSQL
- Uvicorn — ASGI-сервер

Frontend
- Streamlit — интерактивный веб-интерфейс
- Requests — HTTP-клиент для API коммуникации

AI/ML
- Ollama — локальный запуск LLM моделей
- Mistral — open-source языковая модель
- SentenceTransformers — эмбеддинги для семантического поиска

Infrastructure
- Docker — контейнеризация приложения
- Docker Compose — оркестрация сервисов
- PostgreSQL — реляционная база данных

## 🚀 Быстрый старт
- Предварительные требования
- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ свободной RAM
- 5GB+ свободного места на диске


## Запуск проекта
Клонирование репозитория
```bash
git clone <repository-url>
cd data-navigator
```

Запуск всех сервисов
```bash
docker-compose up --build -d
```

Загрузка AI-модели (в отдельном терминале)

```bash
docker exec -it data_navigator-ollama-1 ollama pull mistral
```

Проверка работы
```bash
# Проверка бэкенда
curl http://localhost:8001/

# Проверка фронтенда
open http://localhost:8501
```
## 📊 Доступ к сервисам
После запуска проект будет доступен по следующим адресам:


| Сервис | URL | Назначение |
| ------ | --- | ---------- |
| Web Interface |	http://localhost:8501 |	Основной пользовательский интерфейс |
| API Documentation	| http://localhost:8001/docs	| Swagger UI для API |
| REST API	| http://localhost:8001	| Backend API endpoints |
| Ollama API	| http://localhost:11434	| LLM management API |


## 🎯 Примеры использования
Базовые запросы
```python
# Поиск таблиц
"Какие таблицы есть в базе данных?"

# Анализ структуры  
"Расскажи о таблице well_repair"

# Поиск связей
"Как связаны таблицы well и well_repair?"
```

Бизнес-логика
```python
# Понимание процессов
"Что происходит при изменении статуса скважины?"

# Анализ воздействия
"Какие отчеты используют таблицу well?"
```

## 🏗️ Структура проекта

```text
data-navigator/
├── docker-compose.yml          # Docker компоновка
├── backend/
│   ├── main.py                # FastAPI приложение
│   ├── database.py            # Работа с PostgreSQL
│   ├── chroma_utils.py        # Векторная база данных
│   ├── llm_utils.py           # Интеграция с LLM
│   └── requirements.txt       # Python зависимости
├── frontend/
│   ├── app.py                 # Streamlit интерфейс
│   └── requirements.txt       # Frontend зависимости
└── database/
    └── init.sql               # Инициализация БД
```

##

Навигатор Данных — умный помощник для ваших данных! 🚀
