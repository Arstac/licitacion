from langgraph.graph import StateGraph, START, END

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from markitdown import MarkItDown
import os

from modules.load_prompts import prompt_extraccion_datos
from .class_models import OutStr, State

api_key = os.environ["OPENAI_API_KEY"] 


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
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_extraccion_datos),
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
