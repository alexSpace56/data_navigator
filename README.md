
Data Navigator 🧠🔍

AI-помощник для интеллектуального анализа данных и бизнес-логики ИС ОДС

https://img.shields.io/badge/Python-3.11-blue.svg
https://img.shields.io/badge/Docker-Compose-green.svg
https://img.shields.io/badge/FastAPI-0.104-teal.svg
https://img.shields.io/badge/License-MIT-yellow.svg

📖 О проекте
Data Navigator — это интеллектуальная система на основе ИИ, которая преобразует сложные технические метаданные баз данных в простые и понятные ответы на естественном языке. 
Система предназначена для аналитиков, разработчиков и бизнес-пользователей, работающих с complex enterprise-системами.


🛠️ Технологический стек
Backend
FastAPI — современный ASGI фреймворк

ChromaDB — векторная база данных для RAG

SQLAlchemy — ORM для работы с PostgreSQL

Uvicorn — ASGI-сервер

Frontend
Streamlit — интерактивный веб-интерфейс

Requests — HTTP-клиент для API коммуникации

AI/ML
Ollama — локальный запуск LLM моделей

Mistral — open-source языковая модель

SentenceTransformers — эмбеддинги для семантического поиска

Infrastructure
Docker — контейнеризация приложения

Docker Compose — оркестрация сервисов

PostgreSQL — реляционная база данных

🚀 Быстрый старт
Предварительные требования
Docker 20.10+

Docker Compose 2.0+

4GB+ свободной RAM

5GB+ свободного места на диске

Запуск проекта
Клонирование репозитория

bash
git clone <repository-url>
cd data-navigator
Запуск всех сервисов

bash
docker-compose up --build -d
Загрузка AI-модели (в отдельном терминале)

bash
docker exec -it data_navigator-ollama-1 ollama pull mistral
Проверка работы

bash
# Проверка бэкенда
curl http://localhost:8001/

# Проверка фронтенда
open http://localhost:8501
📊 Доступ к сервисам
После запуска проект будет доступен по следующим адресам:

Сервис	URL	Назначение
Web Interface	http://localhost:8501	Основной пользовательский интерфейс
API Documentation	http://localhost:8001/docs	Swagger UI для API
REST API	http://localhost:8001	Backend API endpoints
Ollama API	http://localhost:11434	LLM management API