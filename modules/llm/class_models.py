from pydantic import BaseModel, Field
from langgraph.graph import MessagesState

class NormativaOutStr(BaseModel):
    normativa: str = Field(None, title="Normativa", description="Descripción de la normativa")
    cumplimiento: str = Field(None, title="Cumplimiento", description="Cumplimiento de la normativa (Igual, Contiene, No)")
    variaciones: str = Field(None, title="Variaciones", description="Variaciones encontradas en la normativa, si aplica")

class State(MessagesState):
    md_content: str = Field(None, title="md_content", description="Contenido en markdown")
    md_content_parts: list[str] = Field(None, title="md_content_parts", description="Contenido en markdown dividido en partes")
    cumplimiento_normativa: list[NormativaOutStr] = Field(None, title="CumplimientoNormativa", description="Cumplimiento de la normativa")
    path_pliego: str = Field(None, title="path_pliego", description="Ruta del pliego de condiciones")
