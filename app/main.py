import csv
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.concurrency import asynccontextmanager
import uvicorn

from app.db import create_tabel, get_connect

ml_model = {}

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    ml_model["connect_db"] = get_connect()
    ml_model["create_table"] = create_tabel()

    yield

    ml_model.clear()


app = FastAPI(lifespan= lifespan)

@app.post("/upload")
def upload_csv(file: UploadFile = File(...)):
    content = file.file.read()
    decoded = content.decode("utf-8")

    reader = csv.reader(io.StringIO(decoded))
    rows = [row for row in reader]

    return {
        "message": "CSV load",
        "rows_count": len(rows),
        "data": rows,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)