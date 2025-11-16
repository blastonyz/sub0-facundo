import json
import os
import re
from pathlib import Path
from typing import Any

from google import genai
from loguru import logger
from src.settings.gemini import GeminiSettings


class AIService:
    """Service wrapper that evaluates projects using an LLM (OpenAI).

    The primary flow is:
    - Read the system prompt from `src/prompts/evaluation.md`.
    - Build a user message containing the project data.
    - Call OpenAI ChatCompletion (model: gpt-3.5-turbo by default) and
      ask for a JSON response with `ai_score`, `decision` and `rationale`.

    If the OpenAI call fails or returns unparsable output, falls back to the
    simple local heuristic used previously.
    """

    PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "evaluation.md"
    MODEL = os.getenv("GENERATIVE_MODEL", "gemini-2.5-flash")

    @staticmethod
    def _read_prompt() -> str:
        return AIService.PROMPT_PATH.read_text(encoding="utf-8")

    @staticmethod
    def _extract_json(text: str) -> dict | None:
        # First, try to remove markdown code block wrapper if present
        if text.strip().startswith("```json") and text.strip().endswith("```"):
            text = text.strip()[len("```json"):-len("```")].strip()

        # Try to find the first JSON object in text
        try:
            return json.loads(text)
        except Exception:
            # Try to extract a JSON substring
            m = re.search(r"(\{\s*\"ai_score\"[\s\S]*\})", text)
            if m:
                try:
                    return json.loads(m.group(1))
                except Exception:
                    return None
            return None


    @staticmethod
    def evaluate_project(project: Any) -> dict:
        """Evaluate a project by calling OpenAI and returning a dict.

        Input: `project` is expected to be a `src.models.project.Project` instance
        (SQLModel/ Pydantic-compatible) or any object with `.name`, `.description`,
        `.budget`, and `.milestones` attributes.

        Returns a dict with keys: ai_score (float), decision (str), rationale (str).
        """

        # Build prompt and messages
        system_prompt = AIService._read_prompt()

        # Build a compact project representation for the model
        proj = {}
        proj["project_title"] = getattr(project, "name", "")
        proj["project_description"] = getattr(project, "description", "") or ""
        proj["budget_usd"] = float(getattr(project, "budget", 0) or 0)

        milestones = []
        for m in getattr(project, "milestones", []) or []:
            # Milestone may be a SQLModel with name/description/amount
            if isinstance(m, dict):
                title = m.get("name") or m.get("title") or str(m)
                desc = m.get("description", "")
                milestones.append(f"{title}: {desc}")
            else:
                title = getattr(m, "name", None) or getattr(m, "title", None)
                desc = getattr(m, "description", None)
                if title and desc:
                    milestones.append(f"{title}: {desc}")
                elif title:
                    milestones.append(str(title))
                else:
                    # Fallback to string representation
                    milestones.append(str(m))

        proj["milestones"] = milestones

        user_message = (
            "Please evaluate the following project and return ONLY a JSON object with keys:"
            " ai_score (number), decision (approve|borderline|reject), rationale (short).\n\n"
            "Example response: {\"ai_score\": 85, \"decision\": \"approve\", \"rationale\": \"The project meets all criteria.\"}"
            f"Project data:\n{json.dumps(proj, ensure_ascii=False, indent=2)}"
            f"{system_prompt}"
        )

        client = genai.Client(api_key=GeminiSettings.API_KEY.get_secret_value())
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=user_message
        )
        response_json = AIService._extract_json(response.text)
        return response_json