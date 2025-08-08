import torch
import torch.nn as nn
from symspellpy.symspellpy import SymSpell, Verbosity

# SymSpell for correction
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary("correction_dict.txt", term_index=0, count_index=1)

# Correct input
def correct_input_with_symspell(user_input: str) -> str:
    corrected_words = []
    for word in user_input.lower().split():
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        corrected_words.append(suggestions[0].term if suggestions else word)
    return " ".join(corrected_words)

class Vocab:
    def __init__(self):
        self.word2idx = {"<pad>": 0, "<sos>": 1, "<eos>": 2}
        self.idx2word = {0: "<pad>", 1: "<sos>", 2: "<eos>"}
        self.next_index = 3

    def encode(self, text, add_eos=True):
        tokens = text.lower().split()
        encoded = []
        for token in tokens:
            if token not in self.word2idx:
                self.word2idx[token] = self.next_index
                self.idx2word[self.next_index] = token
                self.next_index += 1
            encoded.append(self.word2idx[token])
        if add_eos:
            encoded.append(self.word2idx["<eos>"])
        return encoded

    def decode(self, indices):
        words = [self.idx2word.get(idx, "<unk>") for idx in indices]
        return " ".join(word for word in words if word not in ("<pad>", "<eos>", "<sos>"))

    def size(self):
        return self.next_index

# Step 2: Transformer Block
class MiniTransformerBlock(nn.Module):
    def __init__(self, vocab_size, model_dim, heads):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, model_dim)
        self.attn = nn.MultiheadAttention(embed_dim=model_dim, num_heads=heads, batch_first=True)
        self.ff = nn.Sequential(
            nn.Linear(model_dim, model_dim * 4),
            nn.ReLU(),
            nn.Linear(model_dim * 4, model_dim)
        )
        self.norm1 = nn.LayerNorm(model_dim)
        self.norm2 = nn.LayerNorm(model_dim)
        self.output_head = nn.Linear(model_dim, vocab_size)

    def forward(self, x):
        x = self.embed(x)
        attn_out, _ = self.attn(x, x, x)
        x = self.norm1(x + attn_out)
        ff_out = self.ff(x)
        x = self.norm2(x + ff_out)
        logits = self.output_head(x)
        return logits

# Step 3: Advanced Simulated AI Response
def generate_response(input_text):
    vocab = Vocab()

    # Rule-based smart responses
    lower = input_text.lower()
    if "how are you" in lower:
        response_text = "i am doing great thank you for asking"
    elif "your name" in lower:
        response_text = "i am a mini transformer bot created by vaseem"
    elif "what is ai" in lower:
        response_text = "artificial intelligence is the simulation of human intelligence by machines"
    elif "what is your purpose" in lower or "what can you do" in lower:
        response_text = "i can simulate conversations using transformer architecture"
    elif "who are you" in lower:
        response_text = "i am your personal ai assistant"
    elif "hello" in lower or "hi" in lower:
        response_text = "hello there how can i help you today"
    elif "bye" in lower or "goodbye" in lower:
        response_text = "goodbye have a great day"
    else:
        response_text = "sorry i am still learning to answer that"

    # Encode input and response
    input_ids = vocab.encode(input_text)
    response_ids = vocab.encode(response_text)

    # Prepare tensors
    input_tensor = torch.tensor([input_ids])
    model = MiniTransformerBlock(vocab_size=vocab.size(), model_dim=64, heads=4)
    logits = model(input_tensor)

    # Use reference response instead of logits (for now)
    predicted_ids = response_ids  # <- simulate real model output
    output_text = vocab.decode(predicted_ids)

    return input_text.strip(), output_text.strip()

# # Run chatbot
# if __name__ == "__main__":
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("Bot: Goodbye! 🤖")
#             break
#         inp, reply = generate_response(user_input)
#         print("Bot:", reply)
