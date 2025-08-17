from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

app = FastAPI()

MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"   
)

generator = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer
)

class Issue(BaseModel):
    issue: str

@app.post("/suggest_fix")
def suggest_fix(issue: Issue):
    try:
        prompt = (
            "You are a DevOps assistant.\n"
            "A build has failed due to memory limits.\n"
            "Given the issue described below, provide one practical fix or improvement.\n\n"
            f"Issue: {issue.issue}\n\n"
            "Fix:"
        )

        result = generator(prompt, max_new_tokens=200)[0]["generated_text"]
        return {"suggestion": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
