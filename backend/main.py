from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chroma_utils import index_database, query_database
from llm_utils import llm_processor

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


class QueryRequest(BaseModel):
    question: str


@app.post("/api/query")
async def process_query(request: QueryRequest):
    try:
        print(f"📥 Получен запрос: {request.question}")

        # Ищем в векторной БД
        results = query_database(request.question)

        if not results or not results['documents'] or not results['documents'][0]:
            print("❌ Ничего не найдено в векторной БД")
            return {
                "answer": "По вашему запросу ничего не найдено в базе данных.",
                "context": []
            }

        print(f"✅ Найдено {len(results['documents'][0])} результатов")

        # Форматируем контекст
        context = []
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            context.append({
                "description": doc,
                "type": metadata.get('type', 'object'),
                "name": metadata.get('name', ''),
                "table_name": metadata.get('table_name', '')
            })

        # Получаем ответ от LLM
        answer = llm_processor.generate_response(request.question, context)

        print(f"📤 Ответ готов: {answer[:100]}...")

        return {
            "answer": answer,
            "context": context
        }

    except Exception as e:
        print(f"❌ Ошибка в process_query: {e}")
        return {
            "answer": "Произошла ошибка при обработке запроса. Попробуйте еще раз.",
            "error": str(e)
        }


@app.post("/api/index")
async def reindex():
    try:
        count = index_database()
        return {"message": f"Проиндексировано {count} таблиц"}
    except Exception as e:
        raise HTTPException(500, str(e))