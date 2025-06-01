
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from typing import List
from auth import get_current_user
from crud import delete_students_by_ids, get_all_students
from load_csv import load_data_from_csv

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/")
def read_root():
    return {"message": "Student API with CSV import, deletion, and caching"}

@app.post("/import_csv/")
async def import_csv(path: str, background_tasks: BackgroundTasks, user: dict = Depends(get_current_user)):
    background_tasks.add_task(load_data_from_csv, path)
    return {"message": f"CSV import from {path} started in background."}

@app.post("/delete_records/")
async def delete_records(ids: List[int], background_tasks: BackgroundTasks, user: dict = Depends(get_current_user)):
    background_tasks.add_task(delete_students_by_ids, ids)
    return {"message": f"Deletion of records {ids} started in background."}

@app.get("/students")
@cache(expire=60)
async def get_students(user: dict = Depends(get_current_user)):
    return await get_all_students()
