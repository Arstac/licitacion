from .load_config import load_config
 
config = load_config()

print(config)
path_normativa = config["prompts"]["path_prompt_cumplimiento_normativa"]

with open(path_normativa, "r") as file:
    prompt_cumplimiento_normativa = file.read()