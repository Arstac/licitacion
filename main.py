from dotenv import load_dotenv

import gradio as gr
import pandas as pd
import os

from modules import app_info, app_mats, app_price

doc = "lic_2"

load_dotenv()


# #Prueba de funcionamiento de PDF a información
# response_data = app.invoke({"messages": "Extrae la info, porfavor", "doc": doc})

# print(response_data["DataInfo"])


# #Prueba de funcionamiento de PDF a información
# response_mats = app_mats.invoke({"messages": "Extrae la info, porfavor", "doc": doc})

# print(response_mats["materiales"])

# response_price = app_price.invoke({"messages": "Extrae la info, porfavor", "doc": doc})

# print(response_price["mat_prices"])

def extraer_info(file):
    print(f"extrayendo info de file: {file}")
    response_data = app_info.invoke({"messages": "Extrae la info, porfavor", "doc": file})
    df = pd.DataFrame(response_data["DataInfo"])
    output_path = "output.csv"
    df.to_csv(output_path, index=False)
    return output_path, df

def extraer_materiales(file):
    response_mats = app_mats.invoke({"messages": "Extrae la info, porfavor", "doc": file})
    df = pd.DataFrame(response_mats["materiales"])
    output_path = "materiales.csv"
    df.to_csv(output_path, index=False)
    return output_path, df

def buscar_precios():
    response_price = app_price.invoke({"messages": "Extrae la info, porfavor", "doc": doc})
    df = pd.DataFrame(response_price["mat_prices"])
    output_path = "precios.csv"
    df.to_csv(output_path, index=False)
    return output_path

with gr.Blocks() as app:
    gr.Markdown("## Procesador de PDFs para Licitaciones")
    
    with gr.Row():
        file1 = gr.File(label="Anuncio Lic 1 (PDF)")
        file2 = gr.File(label="Lic 1 (PDF)")
    
    extract_info_btn = gr.Button("Extraer Info")
    extract_materials_btn = gr.Button("Extraer Materiales")
    output_csv = gr.File(label="Output CSV")
    output_table = gr.Dataframe()
    materials_csv = gr.File(label="Materiales CSV")
    materials_table = gr.Dataframe()
    
    extract_info_btn.click(extraer_info, inputs=[file1], outputs=[output_csv, output_table])
    extract_materials_btn.click(extraer_materiales, inputs=[file2], outputs=[materials_csv, materials_table])
    
    buscar_btn = gr.Button("Buscar Precios")
    prices_csv = gr.File(label="Precios CSV")
    
    buscar_btn.click(buscar_precios, inputs=[], outputs=prices_csv)

app.launch()
