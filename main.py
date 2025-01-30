import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END,MessagesState
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from markitdown import MarkItDown

load_dotenv()


api_key = os.environ["OPENAI_API_KEY"] 

class OutStr(BaseModel):
    titulo: str = Field(None, title="Titulo", description="Titulo del proyecto")
    importe_total: str = Field(None, title="Importe total", description="Importe total")
    plazo_ejecucion: str = Field(None, title="Plazo de ejecución", description="Plazo de ejecución")


class State(MessagesState):
    DataInfo: OutStr = Field(None, title="DataInfo", description="Información de los datos")
    md_content: str = Field(None, title="md_content", description="Contenido en markdown")

config = {
        "configurable": {
            "thread_id": "123" ,
        }
    }



def get_current_step(state: State):
    # Lógica para obtener el paso actual
    return state["current_step"]

def convert_to_md(state: State):
    md = MarkItDown()
    result = md.convert("Data/EjemploLicitacion.pdf")

    return {"md_content": result.text_content}


def extraccion_datos(state: State):
    system="""Eres un experto en extracción de información de datos. Tu función es ayudar a los usuarios a analizar y extraer información de sus datos.
    Debes extraer la siguiente informacion:
    - Titulo
    - Importe total
    - Plazo ejecución
    
    Documento en formato markdown:
    {md_content}
    
    """
    
    #print(state["data_info"])
    
  
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
    
    chain = prompt | llm.with_structured_output(OutStr)
    
    response = chain.invoke({"messages":state["messages"], "md_content": state["md_content"]})
    
    print(f"Response: {response.model_dump()}")
    
    return {"DataInfo": response}

graph = StateGraph(State)
graph.add_node("convert_to_md", convert_to_md)
graph.add_node("extraccion_datos", extraccion_datos)

graph.add_edge(START, "convert_to_md")
graph.add_edge("convert_to_md", "extraccion_datos")
graph.add_edge("extraccion_datos", END)

app = graph.compile()

response = app.invoke({"messages": "Extrae la info, porfavor"})

print(response["DataInfo"])
