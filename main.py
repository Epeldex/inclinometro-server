import uvicorn

if __name__ == "__main__":
    uvicorn.run("server.api:app", host="192.168.1.78", port=5000, reload=True)
