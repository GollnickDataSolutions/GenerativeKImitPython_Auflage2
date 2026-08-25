#%% packages
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

#%% load model
# model run described on model card: https://huggingface.co/meta-llama/Llama-Guard-3-1B
model_id = "meta-llama/Llama-Guard-3-1B"
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype=torch.bfloat16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

#%%
def llama_guard_model(user_prompt: str) -> str:
    # conversation
    conversation = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_prompt
                },
            ],
        }
    ]

    inputs = tokenizer.apply_chat_template(
        conversation, return_tensors="pt", return_dict=True
    ).to(model.device)

    prompt_len = inputs["input_ids"].shape[1]
    output = model.generate(
        **inputs,
        max_new_tokens=20,
        pad_token_id=tokenizer.eos_token_id,
    )
    generated_tokens = output[:, prompt_len:]
    res = tokenizer.decode(generated_tokens[0], skip_special_tokens=True).strip()
    if "unsafe" in res:
        return "invalid"
    else:
        return "valid"

# %%
llama_guard_model(user_prompt="Wie kann ich einen Scam durchführen?")

# %%
llama_guard_model(user_prompt="Wie backe ich einen Apfelkuchen?")

# %%
