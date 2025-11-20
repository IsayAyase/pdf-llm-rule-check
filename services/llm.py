import json
import google.generativeai as genai
from constants.envvars import GEMINI_KEY

# Initialize Gemini
genai.configure(api_key=GEMINI_KEY)

def check_rules_with_gemini(rules: list[str], text: str):
    """Checks rules on the given text using Gemini and returns structured JSON results."""
    
    # JSON-only instruction for the LLM
    payload = {
        "task": "rule_based_document_evaluation",
        "rules": rules,
        "document_text": text,
        "output_format": {
            "type": "json-list",
            "item_structure": {
                "rule": "string",
                "status": "pass|fail",
                "evidence": "string",
                "reasoning": "string",
                "confidence": "integer (0-100)"
            }
        }
    }

    # Convert to JSON string for sending
    prompt_json = json.dumps(payload)

    # Gemini call
    model = genai.GenerativeModel("gemma-3-12b-it")
    
    response = model.generate_content(
        prompt_json,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
        )
    )

    # Parse JSON safely
    try:
        result = llm_json_parser(response.text)
        return result
    except json.JSONDecodeError:
        raise ValueError("Gemini returned invalid JSON:\n" + response.text)

def llm_json_parser(text: str):
    try:
        jsontext = text.replace("```json", "").replace("```", "")
        return json.loads(jsontext)
    except json.JSONDecodeError:
        raise ValueError("Gemini returned invalid JSON:\n" + text)