from app.config import settings
from app.ai.base import AIProvider
from app.ai.gemini_provider import GeminiProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.fallback_provider import FallbackProvider


class AIRouter:
    @staticmethod
    def get_provider(provider_name: str = "") -> AIProvider:
        chosen = (provider_name or settings.AI_PROVIDER).lower()
        if chosen == "gemini" and settings.GEMINI_API_KEY:
            return GeminiProvider(api_key=settings.GEMINI_API_KEY)
        elif chosen == "openai" and settings.OPENAI_API_KEY:
            return OpenAIProvider(api_key=settings.OPENAI_API_KEY)
        else:
            return FallbackProvider()


ai_service = AIRouter.get_provider()
