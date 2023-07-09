import re


known_tokens = {
    "code-bison": 4,
}

class Model:
    always_available = False
    use_repo_map = False
    send_undo_reply = False

    prompt_price = None
    completion_price = None

    def __init__(self, name):
        self.name = name

        tokens = None

        match = re.search(r"-([0-9]+)k", name)
        if match:
            tokens = int(match.group(1))
        else:
            for m, t in known_tokens.items():
                if name.startswith(m):
                    tokens = t

        if tokens is None:
            raise ValueError(f"Unknown context window size for model: {name}")

        self.max_context_tokens = tokens * 1024

        if self.is_code_bison():
            self.edit_format = "diff"
            self.use_repo_map = True
            self.send_undo_reply = True

 
            self.prompt_price = 0.03
            self.completion_price = 0.06
            self.always_available = True
    

            return

        raise ValueError(f"Unsupported model: {name}")

    def is_code_bison(self):
        return self.name.startswith("code-bison")

    def __str__(self):
        return self.name