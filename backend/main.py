from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chroma_utils import index_database, query_database
import json

app = FastAPI(title="Data Navigator API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return {"message": "Data Navigator API"}


@app.post("/api/query")
async def process_query(request: QueryRequest):
    try:
        # Ищем релевантные объекты в векторной БД
        results = query_database(request.question)

        # Формируем ответ
        response = {
            "answer": f"По вашему запросу '{request.question}' найдена следующая информация:",
            "results": []
        }

        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            if metadata['type'] == 'table':
                response['results'].append({
                    "type": "table",
                    "table_name": metadata['table_name'],
                    "description": doc
                })
            elif metadata['type'] == 'column':
                response['results'].append({
                    "type": "column",
                    "table_name": metadata['table_name'],
                    "column_name": metadata['column_name'],
                    "description": doc
                })
            elif metadata['type'] == 'procedure':
                response['results'].append({
                    "type": "procedure",
                    "name": metadata['name'],
                    "description": doc
                })
            elif metadata['type'] == 'trigger':
                response['results'].append({
                    "type": "trigger",
                    "name": metadata['name'],
                    "description": doc
                })

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/index")
async def reindex_database():
    try:
        count = index_database()
        return {"message": f"База данных проиндексирована. Добавлено {count} объектов."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)