from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()
openai = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))


async def get_response(request: Request):
    # Extract query parameters
    text = request.query_params.get("text")
    summary = request.query_params.get("summary")

    if not text:
        raise HTTPException(status_code=400, detail="No input provided")

    # Call OpenAI GPT-4o
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"You are a chatbot that answers questions based on provided context and the context is {summary}"
            },
            {
                "role": "user",
                "content": f"Answer: {text}"
            },
        ]
    )

    response_message = completion.choices[0].message.content
    return JSONResponse(content={"message": response_message})
