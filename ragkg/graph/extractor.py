"""Entity and relationship extraction from text."""
import re
import json
import openai

EXTRACTION_PROMPT = """Extract entities and relationships from the following text.
Return JSON with format: {"entities": [{"name": "...", "type": "..."}], "relationships": [{"source": "...", "target": "...", "type": "..."}]}

Text: {text}"""

class EntityExtractor:
    def __init__(self, model='gpt-4'):
        self.model = model
        self.client = openai.OpenAI()

    def extract(self, text):
        """Extract entities and relationships using LLM."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(text=text)}],
            temperature=0,
        )
        try:
            content = response.choices[0].message.content
            # try to parse JSON from response
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group())
        except (json.JSONDecodeError, AttributeError):
            pass
        return {"entities": [], "relationships": []}
