import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.server.main:server",
        host="0.0.0.0",
        port=8000,
        reload=True,
        use_colors=True
    )