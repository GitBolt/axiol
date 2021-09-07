import os
from fastapi import FastAPI
from nacl.signing import VerifyKey
from starlette.responses import Response
from fastapi import Request, HTTPException
from nacl.exceptions import BadSignatureError


app = FastAPI()

# Your public key can be found on your application in the Developer Portal
PUBLIC_KEY = os.environ["PUBLIC_KEY"]
EXAMPLE_RESPONSE = {
    "type": 4,
    "data":{
        "content": "Successfully received command",
        "flags": 1
    }
}
       
@app.middleware("http")
async def discord_validation(request: Request, call_next):
    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = await request.body()

    decoded_body = body.decode("utf-8")
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    
    try:
        verify_key.verify(f'{timestamp}{decoded_body}'.encode(),
                          bytes.fromhex(signature))
        return request(call_next)
    except BadSignatureError:
        print
        return HTTPException(
            status_code=401, detail={"error": "Incorrect request"}
        )


@app.get("/")
async def index() -> Response:
    return Response(
        status_code=200, 
        content={"Message": "Welcome to interaction webhook server"}
        )
        
            
@app.post("/interactions")
async def interactions(request: Request) -> Response:
    print(request.json())



