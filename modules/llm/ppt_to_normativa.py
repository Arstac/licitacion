from langgraph.graph import StateGraph, START, END

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from markitdown import MarkItDown

#from modules.load_prompts import prompt_cumplimiento_normativa
from .class_models import State, NormativaOutStr
from .load_llm_models import llm

# config = {
#         "configurable": {
#             "thread_id": "123" ,
#         }
#     }


prompt_cumplimiento_normativa = """Eres un analizador encargado de buscar si una normativa se encuentra en un documento.
Responde con:
- Igual: Si la normativa se encuentra en el documento de forma exacta.
- Contiene: Si la normativa se encuentra en el documento pero con variaciones. En caso de contener la normativa, especifica las variaciones encontradas.
- No: Si la normativa no se encuentra en el documento.

La normativa a buscar es la siguiente:
{normativa}

El contenido del documento es el siguiente:
{documento}
"""
def get_current_step(state: State):
    # Lógica para obtener el paso actual
    return state["current_step"]

def convert_to_md(state: State):
    md = MarkItDown()
    result = md.convert(f"{state['doc']}")

    return {"md_content": result.text_content}

import pandas as pd
def evaluar_cumplimiento_normativa(state: State):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_cumplimiento_normativa),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    
    chain = prompt | llm.with_structured_output(NormativaOutStr)
    # Read Data/normativa.csv
    df_normativa = pd.read_csv("Data/normativa.csv", sep=",")

    #     ID_instruccion,descripcion,obligatoria
    # INSTR-001,Uso obligatorio de materiales certificados para la construcción,si
    # INSTR-002,Aplicación de medidas de seguridad en obra,si
    cumplimiento_normativa = []
    # Por cada descripcion de la normaitva:
    for normativa in df_normativa["descripcion"]:
        response = chain.invoke({"messages":state["messages"], "documento": state["md_content"], "normativa": normativa})
        cumplimiento_normativa.append([normativa, response.model_dump()["cumplimiento"], response.model_dump()["variaciones"]])
        
    
    return {"cumplimiento_normativa": cumplimiento_normativa}

graph = StateGraph(State)
graph.add_node("convert_to_md", convert_to_md)
graph.add_node("evaluar_cumplimiento_normativa", evaluar_cumplimiento_normativa)

graph.add_edge(START, "convert_to_md")
graph.add_edge("convert_to_md", "evaluar_cumplimiento_normativa")
graph.add_edge("evaluar_cumplimiento_normativa", END)

app_normativa = graph.compile()