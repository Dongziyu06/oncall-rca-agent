from typing import Any
from pydantic import BaseModel, Field

class AlertLabels(BaseModel):
    alertname: str = "UnknownAlert"
    service: str | None = None
    model_config = {"extra": "allow"}

class AlertItem(BaseModel):
    labels: AlertLabels = Field(default_factory=AlertLabels)
    annotations: dict[str, Any] = Field(default_factory=dict)
    startsAt: str | None = None
    model_config = {"extra": "allow"}

class AlertRequest(BaseModel):
    alerts: list[AlertItem] = Field(default_factory=list)
    # convenient natural-language fallback
    description: str | None = None
    # baseline=True → skip all tools & RAG, LLM only sees alert text (Mode A)
    baseline: bool = False
    model_config = {"extra": "allow"}

class AlertResponse(BaseModel):
    task_id: str
    status: str

