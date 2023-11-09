from fastapi import FastAPI, Response, Request, HTTPException

app = FastAPI()

@app.post("/submit")
async def submit(request: Request):
    content_type = request.headers['Content-Type']
    if content_type == 'application/xml':
        body = await request.body()
        return Response(content=body, media_type="application/xml")
    else:
        raise HTTPException(status_code=400, detail=f'Content type {content_type} not supported')