from pydantic import BaseModel, Field
from langgraph.graph import MessagesState

class OutStr(BaseModel):
    titulo: str = Field(None, title="Titulo", description="Titulo del proyecto")
    importe_total: str = Field(None, title="Importe total", description="Importe total")
    plazo_ejecucion: str = Field(None, title="Plazo de ejecución", description="Plazo de ejecución")

class Mat(BaseModel):
    descripcion: str = Field(None, title="Material", description="Material")
    cantidad: str = Field(None, title="Cantidad", description="Cantidad")
    unidad: str = Field(None, title="Unidad", description="Unidad")
    # precio_unitario: float = Field(None, title="Precio unitario", description="Precio unitario")
    # importe: float = Field(None, title="Importe", description="Importe")
    ubicaion: str = Field(None, title="Ubicación", description="Ubicación dento del documento")
    referencia: str = Field(None, title="Referencia", description="Codigo de referencia del material")
    
class MatOutStr(BaseModel):
    materiales: list[Mat] = Field(None, title="Materiales", description="Materiales")
    
    
class State(MessagesState):
    DataInfo: OutStr = Field(None, title="DataInfo", description="Información de los datos")
    md_content: str = Field(None, title="md_content", description="Contenido en markdown")
    md_content_parts: list[str] = Field(None, title="md_content_parts", description="Contenido en markdown dividido en partes")
    materiales: list[Mat] = Field(None, title="Materiales", description="Materiales")

