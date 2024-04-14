from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("config.yaml", 'r') as f:
  config = load(f, Loader=Loader)

# OpenAI
openai_assistant_id = config["openai"]["assistant_id"]
openai_api_key = config["openai"]["api_key"]

# Google
g_client_id = config["google"]["client_id"]
g_client_secret = config["google"]["client_secret"]


if __name__ == "__main__":
  print("You should not be seeing this message. If this message somehow appears, please contact contact@adamxu.net")
  print("DEBUG CONFIG YAML CONVERTED TO JSON BELOW:")
  print(config)