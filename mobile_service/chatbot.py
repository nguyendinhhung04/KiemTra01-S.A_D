# chatbot/services.py
import torch
import json
import os
from transformers import pipeline

_pipe = None

def get_chatbot_pipe():
    global _pipe
    if _pipe is None:
        model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        _pipe = pipeline(
            "text-generation", 
            model=model_id, 
            torch_dtype=torch.bfloat16, 
            device_map="auto"
        )
    return _pipe


def get_knowledge_base():
    """Đọc dữ liệu từ file JSON Knowledge Base local của service."""
    kb_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'knowledge_base.json')
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"mobiles": []}


def build_system_prompt() -> str:
    kb = get_knowledge_base()
    mobiles = kb.get("mobiles", [])
    
    if not mobiles:
        product_text = "Hiện chưa có sản phẩm nào."
    else:
        product_text = "\n".join(
            f"- {p['name']} | Giá: {p['price']:,.0f}$ | "
            f"CPU: {p['specs']['cpu']}, RAM: {p['specs']['ram']}, Camera: {p['specs']['camera']}"
            for p in mobiles
        )

    return f"""<|system|>
Bạn là trợ lý trợ lý tư vấn bán điện thoại di động. 
Danh sách sản phẩm từ Local Knowledge Base (JSON):
{product_text}
Chỉ tư vấn sản phẩm có trong danh sách. Trả lời bằng tiếng Việt.</s>"""


def chat(user_message: str) -> str:
    system_prompt = build_system_prompt()
    pipe = get_chatbot_pipe()
    
    prompt = f"{system_prompt}\n<|user|>\n{user_message}</s>\n<|assistant|>\n"
    
    outputs = pipe(
        prompt, 
        max_new_tokens=256, 
        do_sample=True, 
        temperature=0.7
    )
    
    full_response = outputs[0]["generated_text"]
    reply = full_response.split("<|assistant|>\n")[-1]
    
    return reply.strip()
