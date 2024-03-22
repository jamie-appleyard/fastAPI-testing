import uvicorn

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)

#some logic here to seed a test database if env var TEST = True
#some logic here to seed a dev database if env var TEST = False
    