"""Forced single-token policy choices using the local Qwen checkpoint."""
class LocalChoice:
    def __init__(self, path):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(path, local_files_only=True, torch_dtype=torch.bfloat16)
        model.to("cuda" if torch.cuda.is_available() else "cpu").eval()
        self._bind(path, tokenizer, model)

    @classmethod
    def from_loaded(cls, path, tokenizer, model):
        reader = cls.__new__(cls)
        reader._bind(path, tokenizer, model)
        return reader

    def _bind(self, path, tokenizer, model):
        import torch
        self.torch, self.tokenizer, self.model = torch, tokenizer, model
        self.letters = "ABCDE"
        ids = [self.tokenizer.encode(letter, add_special_tokens=False) for letter in self.letters]
        if any(len(seq) != 1 for seq in ids):
            raise ValueError("choice labels must be single tokens")
        self.ids = [seq[0] for seq in ids]
        self.last_usage = {}
        self.identity = str(path)

    def __call__(self, instruction, content):
        messages = [{"role": "system", "content": instruction}, {"role": "user", "content": content}]
        ids = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
        if ids.shape[1] > self.model.config.max_position_embeddings:
            raise ValueError("evidence does not fit the model context")
        with self.torch.inference_mode():
            hidden = self.model.model(input_ids=ids.to(self.model.device), use_cache=False).last_hidden_state[:, -1, :]
            logits = self.model.lm_head(hidden)[0, self.ids]
        self.last_usage = {"input_tokens": ids.shape[1], "scored_tokens": 1}
        return self.letters[int(logits.argmax())]
