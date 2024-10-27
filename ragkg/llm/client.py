"""LLM client for generation."""
import openai

class LLMClient:
    def __init__(self, model='gpt-4'):
        self.model = model
        self.client = openai.OpenAI()

    def generate(self, query, context, max_tokens=1024):
        """Generate answer using retrieved context."""
        context_str = "\n\n".join(context) if isinstance(context, list) else context
        prompt = f"""Answer the question based on the following context. If the context doesn't contain enough information, say so.

Context:
{context_str}

Question: {query}

Answer:"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.1,
        )
        return response.choices[0].message.content
