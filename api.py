from fastapi import FastAPI
from agent import PaymentMethodAgent
from memory import update_memory

app = FastAPI()
agent = PaymentMethodAgent()

@app.post("/recommend")
def recommend(context: dict):
    return agent.recommend(context)

@app.post("/feedback")
def feedback(method: str, success: bool):
    update_memory(method, success)
    return {"status": "memory updated"}
