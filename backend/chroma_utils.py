import chromadb
from sentence_transformers import SentenceTransformer
from database import get_database_schema, get_procedures_and_triggers

# Инициализация модели для эмбеддингов
embedder = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Инициализация ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="database_schema")


def generate_column_description(column_info):
    """Генерирует описание для колонки на основе её метаданных"""
    keywords = {
        'id': 'уникальный идентификатор',
        'name': 'наименование',
        'date': 'дата',
        'type': 'тип',
        'status': 'статус',
        'reason': 'причина',
        'description': 'описание',
        'planned': 'плановый',
        'actual': 'фактический',
        'well': 'скважины',
        'field': 'месторождения',
        'repair': 'ремонта',
        'crew': 'бригады',
        'event': 'события'
    }

    name_parts = column_info['name'].split('_')
    translated_parts = [keywords.get(part, part) for part in name_parts]
    description = " ".join(translated_parts) + "."

    if column_info['primary_key']:
        description += " Первичный ключ таблицы."
    elif not column_info['nullable']:
        description += " Обязательное поле."

    return description.capitalize()


def infer_procedure_purpose(definition):
    """Определяет назначение процедуры по её коду"""
    definition_lower = definition.lower()
    if 'repair' in definition_lower and 'duration' in definition_lower:
        return "Расчет длительности ремонтных работ скважин"
    elif 'status' in definition_lower and 'well' in definition_lower:
        return "Получение текущего статуса скважины и информации о ремонте"
    elif 'update' in definition_lower and 'timestamp' in definition_lower:
        return "Обновление временных меток при изменении данных"
    return "Обработка бизнес-логики работы со скважинами"


def infer_trigger_purpose(definition):
    """Определяет назначение триггера по его коду"""
    definition_lower = definition.lower()
    if 'timestamp' in definition_lower:
        return "Автоматическое обновление времени последнего изменения"
    elif 'status' in definition_lower and 'repair' in definition_lower:
        return "Автоматическое обновление статуса скважины при изменении статуса ремонта"
    return "Автоматическая обработка изменений данных"


def generate_description(db_object):
    """Генерирует описание для объекта БД"""
    if db_object['type'] == 'table':
        return f"Таблица {db_object['name']}. Содержит поля: {', '.join([col['name'] for col in db_object['columns']])}."
    elif db_object['type'] == 'procedure':
        return f"Процедура {db_object['name']}. Назначение: {infer_procedure_purpose(db_object['definition'])}"
    elif db_object['type'] == 'trigger':
        return f"Триггер {db_object['name']}. Назначение: {infer_trigger_purpose(db_object['definition'])}"
    elif db_object['type'] == 'column':
        return generate_column_description(db_object)
    return ""


def index_database():
    """Индексирует схему БД, процедуры и триггеры в ChromaDB"""
    schema = get_database_schema()
    procedures, triggers = get_procedures_and_triggers()

    documents = []
    metadatas = []
    ids = []

    # Индексация таблиц и колонок
    for table in schema:
        table_doc = generate_description({'type': 'table', 'name': table['table_name'], 'columns': table['columns']})
        documents.append(table_doc)
        metadatas.append({'type': 'table', 'name': table['table_name']})
        ids.append(f"table_{table['table_name']}")

        for column in table['columns']:
            col_doc = generate_description({'type': 'column', 'name': column['name'], **column})
            documents.append(col_doc)
            metadatas.append({'type': 'column', 'table_name': table['table_name'], 'name': column['name']})
            ids.append(f"col_{table['table_name']}_{column['name']}")

    # Индексация процедур
    for proc in procedures:
        proc_doc = generate_description({'type': 'procedure', 'name': proc['name'], 'definition': proc['definition']})
        documents.append(proc_doc)
        metadatas.append({'type': 'procedure', 'name': proc['name']})
        ids.append(f"proc_{proc['name']}")

    # Индексация триггеров
    for trigger in triggers:
        trigger_doc = generate_description(
            {'type': 'trigger', 'name': trigger['name'], 'definition': trigger['definition']})
        documents.append(trigger_doc)
        metadatas.append({'type': 'trigger', 'name': trigger['name']})
        ids.append(f"trig_{trigger['name']}")

    # Генерируем эмбеддинги и добавляем в коллекцию
    embeddings = embedder.encode(documents).tolist()
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )

    return len(documents)


def query_database(query, n_results=5):
    """Ищет релевантные таблицы и колонки по запросу"""
    query_embedding = embedder.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    return results