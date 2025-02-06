from .load_config import load_config
 
config = load_config()

print(config)
path_extraccion_datos = config["prompts"]["path_prompt_extraccion_datos"]

with open(path_extraccion_datos, "r") as file:
    prompt_extraccion_datos = file.read()