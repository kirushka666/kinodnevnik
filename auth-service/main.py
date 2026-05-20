from fastapi import FastAPI
import hashlib

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Auth Service работает!"}

@app.get("/api/hash/{text}")
def get_hash(text: str):
    # Простое хэширование через SHA-256
    hashed = hashlib.sha256(text.encode()).hexdigest()
    return {"text": text, "hash": hashed}

@app.get("/api/about")
def about():
    return {"project": "КиноДневник", "author": "sedukhin"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)