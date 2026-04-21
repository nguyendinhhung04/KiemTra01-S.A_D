from pathlib import Path

import torch
from transformers import pipeline

from laptops.graph_models import Laptop

_pipe = None
GRAPH_READY_FILE = Path("/tmp/laptop_graph_ready")


def get_chatbot_pipe():
    global _pipe
    if _pipe is None:
        model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        _pipe = pipeline(
            "text-generation",
            model=model_id,
            torch_dtype=torch.float32,
            device_map="cpu",
        )
    return _pipe


def is_graph_ready() -> bool:
    return GRAPH_READY_FILE.exists()


def get_knowledge_base():
    if not is_graph_ready():
        raise RuntimeError("Graph data is still being seeded")

    try:
        laptops = Laptop.nodes.all()
        laptop_list = []
        for laptop in laptops:
            manufacturer = laptop.manufacturer.all()[0] if laptop.manufacturer else None
            category = laptop.category.all()[0] if laptop.category else None
            cpu = laptop.cpu.all()[0] if laptop.cpu else None
            gpu = laptop.gpu.all()[0] if laptop.gpu else None
            ram = laptop.ram.all()[0] if laptop.ram else None
            screen = laptop.screen.all()[0] if laptop.screen else None

            laptop_list.append(
                {
                    "id": laptop.product_id,
                    "name": laptop.name,
                    "manufacturer": manufacturer.name if manufacturer else "",
                    "category": category.name if category else "",
                    "price": laptop.price,
                    "discount": laptop.discount,
                    "specs": {
                        "cpu": cpu.name if cpu else "",
                        "gpu": gpu.name if gpu else "",
                        "ram": ram.name if ram else "",
                        "screen": screen.name if screen else "",
                    },
                    "description": laptop.description,
                }
            )
        return {"laptops": laptop_list}
    except Exception as e:
        print(f"Error querying Neo4j: {e}")
        return {"laptops": []}


def build_system_prompt() -> str:
    kb = get_knowledge_base()
    laptops = kb.get("laptops", [])

    if not laptops:
        product_text = "Hien chua co san pham nao."
    else:
        product_text = "\n".join(
            f"- {p['name']} | Gia: {p['price']:,.0f}$ | "
            f"CPU: {p['specs']['cpu']}, RAM: {p['specs']['ram']}, GPU: {p['specs']['gpu']}"
            for p in laptops
        )

    return f"""<|system|>
Ban la tro ly tu van ban hang laptop than thien.
Duoi day la danh sach san pham tu Graph Knowledge Base (Neo4j):
{product_text}
Chi tu van san pham co trong danh sach. Tra loi ngan gon bang tieng Viet.</s>"""


def chat(user_message: str) -> str:
    system_prompt = build_system_prompt()
    pipe = get_chatbot_pipe()

    prompt = f"{system_prompt}\n<|user|>\n{user_message}</s>\n<|assistant|>\n"
    outputs = pipe(
        prompt,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
    )

    full_response = outputs[0]["generated_text"]
    reply = full_response.split("<|assistant|>\n")[-1]
    return reply.strip()
