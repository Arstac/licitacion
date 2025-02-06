from langgraph.graph import StateGraph, START, END

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

from markitdown import MarkItDown
import os

from modules.load_prompts import prompt_extraccion_datos
from .class_models import Mat, MatOutStr, State
import pandas as pd

api_key = os.environ["OPENAI_API_KEY"] 
MAX_TOKENS = 500

config = {
        "configurable": {
            "thread_id": "123" ,
        }
    }


def convert_to_md(state: State):
    md = MarkItDown()
    result = md.convert("Data/ppt.pdf")
    
    print(f"Length: {len(result.text_content)}")

    return {"md_content": result.text_content}

def mats_to_excel(state: State):
    """Converts the structured output of the material extraction process to an Excel file"""

    # Extract the materials data from the state
    materials_data = state["materiales"]

    # Create a DataFrame from the materials data
    df = pd.DataFrame(materials_data)

    # Define the output Excel file path
    output_file = "materials.xlsx"

    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False)

    return {"excel_file_path": output_file}
    

def extraccion_materiales(state: State):
    prompt_extraccion_materiales = prompt_extraccion_materiales = """Eres un ingeniero especializado en análisis de pliegos técnicos. Extrae exhaustivamente TODOS los materiales medibles mencionados incluyendo:
- Descripción completa del material
- Cantidad numérica exacta
- Unidad de medida (m, m², kg, etc.)
- Código de referencia (si existe)
- Sección/documento donde aparece

Sigue estas reglas estrictamente:
1. Incluye solo elementos cuantificables con unidades de medida
2. Si no se especifica cantidad, omitir el elemento
3. Mantener fidelidad absoluta a los valores originales
4. Especificar la ubicación exacta (página, apartado)
5. Usar formato JSON estructurado para cada entrada

Ejemplo de salida:
{{
  "materiales": [
    {{
      "descripcion": "Tubo de acero galvanizado DN 80",
      "cantidad": 120,
      "unidad": "metros",
      "referencia": "ISO 65-DN80",
      "ubicacion": "Capítulo 5, Sección 3.2.1"
    }}
  ]
}}

Pliego técnico:
{pliego}
"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_extraccion_materiales),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
    
    chain = prompt | llm.with_structured_output(MatOutStr)
    
    response = chain.invoke({"messages":state["messages"], "pliego": state["md_content"]})
    
    print(f"Response: {response.model_dump()['materiales']}")
    
    return {"materiales": response.model_dump()["materiales"]}

graph_mats = StateGraph(State)
graph_mats.add_node("convert_to_md", convert_to_md)
graph_mats.add_node("extraccion_materiales", extraccion_materiales)
graph_mats.add_node("mats_to_excel", mats_to_excel)

graph_mats.add_edge(START, "convert_to_md")
graph_mats.add_edge("convert_to_md", "extraccion_materiales")
graph_mats.add_edge("extraccion_materiales", "mats_to_excel")
graph_mats.add_edge("mats_to_excel", END)

app_mats = graph_mats.compile()
