from pydantic import BaseModel


class EvaluateResponse(BaseModel):
    ai_score: float
    decision: str  # "approve" | "reject" | "borderline"
    rationale: str
