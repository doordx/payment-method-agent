import os, json, re
from groq import Groq
from dotenv import load_dotenv

from config import GROQ_API_KEY, MODEL_NAME
from tools import get_global_success_rates, get_user_history
from rules import apply_rules
from memory import load_memory
from debate_agents import upi_agent, card_agent, wallet_agent

load_dotenv()

def extract_json_from_response(content: str) -> dict:
    """Extract JSON from LLM response, handling markdown code blocks and other formatting."""
    try:
        # First, try to parse directly
        return json.loads(content)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON object in the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        # If all else fails, raise an error with the content
        raise ValueError(f"Could not extract valid JSON from response: {content}")

class PaymentMethodAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.system_prompt = """
You are a Payment Method Success Recommendation Agent.

You follow this process:
1. Use provided tools and rules.
2. Reason step-by-step.
3. Recommend a primary and fallback payment method.
4. Output STRICT JSON only.

Never recommend a method not allowed by rules.
"""

    def recommend(self, context: dict) -> dict:
        allowed = apply_rules(context)
        memory = load_memory()
        success_rates = get_global_success_rates()

        debates = {
            "upi": upi_agent(context),
            "card": card_agent(context),
            "wallet": wallet_agent(context)
        }

        prompt = f"""
Allowed methods: {allowed}

Global success rates:
{json.dumps(success_rates, indent=2)}

Agent memory:
{json.dumps(memory, indent=2)}

Debate arguments:
{json.dumps(debates, indent=2)}

Transaction:
{json.dumps(context, indent=2)}

Return STRICT JSON:
{{
  "primary_method": "...",
  "fallback_method": "...",
  "confidence": 0.xx,
  "explanation": "..."
}}
"""

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return extract_json_from_response(content)
