import streamlit as st
import requests
import json

# Настройки
RAG_API_URL = st.secrets.get("RAG_API_URL", "http://localhost:8001")

st.set_page_config(page_title="Data Navigator", page_icon="🔍", layout="wide")

st.title("🔍 Data Navigator")
st.markdown("### AI-помощник для поиска данных в ИС ОДС")

# Инициализация сессии
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant",
                                      "content": "Привет! Я ваш помощник по данным ИС ОДС. Спросите меня о таблицах, полях или бизнес-логике."})

# Показ истории сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода
if prompt := st.chat_input("Задайте вопрос о данных..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Отправка запроса к API
    with st.chat_message("assistant"):
        with st.spinner("Ищу информацию..."):
            try:
                response = requests.post(
                    f"{RAG_API_URL}/api/query",
                    json={"question": prompt},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()

                    # Показываем ответ
                    st.markdown(data["answer"])

                    for result in data["results"]:
                        with st.expander(
                                f"**{result['type'].capitalize()}**: {result.get('table_name', '')}.{result.get('column_name', '')}"):
                            st.markdown(result['description'])

                else:
                    st.error("Ошибка при обработке запроса")

            except Exception as e:
                st.error(f"Ошибка соединения с API: {str(e)}")

# Sidebar с информацией
with st.sidebar:
    st.header("ℹ️ О системе")
    st.markdown("""
    **Data Navigator** помогает:
    - Находить таблицы и поля в БД
    - Понимать бизнес-логику

    Просто спросите на естественном языке!
    """)

    if st.button("🔄 Переиндексировать базу данных"):
        with st.spinner("Индексация..."):
            try:
                response = requests.post(f"{RAG_API_URL}/api/index")
                if response.status_code == 200:
                    st.success("База данных переиндексирована!")
                else:
                    st.error("Ошибка при индексации")
            except:
                st.error("Не удалось подключиться к API")