import vertexai
from vertexai.preview.language_models import CodeChatModel
import yaml

class ConfigurationLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_yaml_file()

    def load_yaml_file(self):
        with open(self.file_path, 'r') as file:
            try:
                yaml_data = yaml.safe_load(file)
                return yaml_data
            except yaml.YAMLError as e:
                print(f"Error loading YAML file: {e}")

    def get_value(self, key):
        if key in self.data:
            return self.data[key]
        else:
            print(f"Key '{key}' not found in YAML file.")
            return None


class ChatModel:

    def __init__(self, project_id, model_id,location):
        self.project_id = project_id
        self.model_id = model_id
        self.location = location

    def initialize(self):
        """Initialize the chat model."""
        client = vertexai.init(project =self.project_id, location=self.location)
        chat_model = CodeChatModel.from_pretrained(self.model_id)
        return chat_model

    def send_message(self, message, **parameters):
        chat = self.initialize().start_chat()
        response = chat.send_message(message, **parameters)
        return response.text