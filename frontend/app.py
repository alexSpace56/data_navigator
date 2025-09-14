import streamlit as st
import requests
import os
import json
from datetime import datetime

API_URL = os.getenv("RAG_API_URL", "http://rag_api:8000")

st.set_page_config(page_title="Data Navigator", layout="wide")
st.title("🔍 Навигатор Данных")
st.markdown("### ИИ-помощник для работы с данными ИС ОДС")

# Инициализация сессии
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Привет! Я ваш ИИ-помощник по данным ИС ОДС. Спросите меня о таблицах, полях или бизнес-логике.",
        "timestamp": datetime.now().isoformat(),
        "id": "welcome_message"
    })

if "deleted_messages" not in st.session_state:
    st.session_state.deleted_messages = []


# Функции для управления историей
def add_message(role, content, message_id=None):
    """Добавляет сообщение в историю"""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "id": message_id or f"msg_{datetime.now().timestamp()}"
    }
    st.session_state.messages.append(message)
    return message


def delete_message(message_id):
    """Удаляет сообщение по ID"""
    st.session_state.messages = [
        msg for msg in st.session_state.messages
        if msg["id"] != message_id
    ]
    st.session_state.deleted_messages.append(message_id)
    st.rerun()


def clear_chat():
    """Очищает всю историю чата"""
    st.session_state.messages = [
        msg for msg in st.session_state.messages
        if msg["id"] == "welcome_message"
    ]
    st.session_state.deleted_messages = []
    st.rerun()


# Сайдбар с управлением
with st.sidebar:
    st.header("⚙️ Управление чатом")

    # Кнопка очистки истории
    if st.button("🗑️ Очистить историю", use_container_width=True):
        clear_chat()
        st.success("История очищена!")

    # Статистика
    st.metric("Сообщений", len(st.session_state.messages))
    st.metric("Удалено", len(st.session_state.deleted_messages))

    st.divider()
    st.header("ℹ️ О системе")
    st.markdown("""
    **Навигатор данных** помогает:
    - Находить таблицы и поля в БД
    - Понимать бизнес-логику

    Просто спросите на естественном языке!
    """)

    if st.button("🔄 Переиндексировать базу данных", use_container_width=True):
        with st.spinner("Индексация..."):
            try:
                response = requests.post(f"{API_URL}/api/index")
                if response.status_code == 200:
                    st.success("База данных переиндексирована!")
                else:
                    st.error("Ошибка при индексации")
            except:
                st.error("Не удалось подключиться к API")

# Основной интерфейс чата
chat_container = st.container()

with chat_container:
    # Показ истории сообщений с кнопками удаления
    for message in st.session_state.messages:
        # Пропускаем удаленные сообщения
        if message["id"] in st.session_state.deleted_messages:
            continue

        col1, col2 = st.columns([0.9, 0.1])

        with col1:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                # Показываем контекст если есть (для ответов ассистента)
                if message["role"] == "assistant" and "context" in message:
                    with st.expander("📊 Источники информации"):
                        for item in message.get("context", []):
                            st.write(f"**{item.get('type', 'object')}**: {item.get('description', '')}")

        with col2:
            # Кнопка удаления только для не-приветственных сообщений
            if message["id"] != "welcome_message":
                if st.button("❌", key=f"delete_{message['id']}"):
                    delete_message(message["id"])

# Поле ввода внизу
input_container = st.container()
with input_container:
    if prompt := st.chat_input("Задайте вопрос о данных..."):
        # Добавляем вопрос пользователя
        user_message = add_message("user", prompt)

        # Отправка запроса к API
        with st.spinner("🤔 Думаю..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/query",
                    json={"question": prompt},
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()

                    # Формируем ответ ассистента
                    assistant_content = data["answer"]

                    # Добавляем ответ ассистента
                    assistant_message = add_message("assistant", assistant_content)

                    # Сохраняем контекст для показа в expander
                    if "context" in data:
                        assistant_message["context"] = data["context"]

                else:
                    error_msg = "Ошибка при обработке запроса"
                    add_message("assistant", error_msg)

            except Exception as e:
                error_msg = f"Ошибка соединения с API: {str(e)}"
                add_message("assistant", error_msg)

        # Обновляем интерфейс
        st.rerun()

# Стили для улучшения внешнего вида
st.markdown("""
<style>
    .stButton button {
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stExpander {
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)