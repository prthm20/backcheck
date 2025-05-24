from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import openai
import os
client = openai.OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
async def extract_skills(request: Request):
    try:
        
        summary = request.query_params.get("summary")
        
        if not summary:
            return JSONResponse(content={"message": "No summary provided"}, status_code=400)

        structured_prompt = f"Extract skills and group them for chart display based on this summary: {summary}"
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a skill extractor for charting. Format the response as JSON."},
                {"role": "user", "content": structured_prompt}
            ]
        )

        json_data = response.choices[0].message.content
        print("backend =", json_data)

        return JSONResponse(content={"data": json_data})
    
    except Exception as e:
        print("Server Error:", e)
        return JSONResponse(content={"message": "Server Error"}, status_code=500)