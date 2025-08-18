from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sentence_transformers import SentenceTransformer
import torch
import os

KB_PATH='agents/responder_agent/knowledge_base/incidents.md'

with open(KB_PATH,'r') as f:
    kb_text=f.read()
    
sections=[sec.strip() for sec in kb_text.split('##') if sec.strip()]

kb_entries=[]
for sec in sections:
    lines=sec.splitlines()
    title=lines[0].strip()
    content='\n'.join(lines[1:]).strip()
    kb_entries.append((title,content))

embedder=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
kb_embedding=[embedder.encode(text) for (_,text) in kb_entries]

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
        query=issue.issue
        query_emb=embedder.encode(query)
        best_idx=-1
        best_score=-999
        for i,emb in enumerate(kb_embedding):
            score=float(torch.nn.functional.cosine_similarity(
                torch.tensor(query_emb),torch.tensor(emb),dim=0))
            if score>best_score:
                best_score=score
                best_idx=i
        retrieved_context=kb_entries[best_idx][1]
        prompt = (
    "You are a senior DevOps engineer.\n"
    f"Knowledge Base:\n{retrieved_context}\n\n"
    f"Problem:\n{query}\n\n"
    "Write a single, practical fix in 1 concise sentence.\n"
    "Fix:"
)

        result = generator(prompt,max_new_tokens=100,do_sample=False,repetition_penalty=1.5,temperature=0.0)[0]['generated_text']

        return {"suggestion": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/')
def root():
    return {'agent':'responder','status':'running'}