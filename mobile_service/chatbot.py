from pathlib import Path

import torch
from transformers import pipeline

from mobiles.graph_models import Mobile

_pipe = None
GRAPH_READY_FILE = Path("/tmp/mobile_graph_ready")


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
        mobiles = Mobile.nodes.all()
        mobile_list = []
        for mobile in mobiles:
            manufacturer = mobile.manufacturer.all()[0] if mobile.manufacturer else None
            category = mobile.category.all()[0] if mobile.category else None
            cpu = mobile.cpu.all()[0] if mobile.cpu else None
            gpu = mobile.gpu.all()[0] if mobile.gpu else None
            ram = mobile.ram.all()[0] if mobile.ram else None
            camera = mobile.camera.all()[0] if mobile.camera else None

            mobile_list.append(
                {
                    "id": mobile.product_id,
                    "name": mobile.name,
                    "manufacturer": manufacturer.name if manufacturer else "",
                    "category": category.name if category else "",
                    "price": mobile.price,
                    "discount": mobile.discount,
                    "specs": {
                        "cpu": cpu.name if cpu else "",
                        "gpu": gpu.name if gpu else "",
                        "ram": ram.name if ram else "",
                        "camera": camera.name if camera else "",
                    },
                    "description": mobile.description,
                }
            )
        return {"mobiles": mobile_list}
    except Exception as e:
        print(f"Error querying Neo4j: {e}")
        return {"mobiles": []}


def build_system_prompt() -> str:
    kb = get_knowledge_base()
    mobiles = kb.get("mobiles", [])

    if not mobiles:
        product_text = "Hien chua co san pham nao."
    else:
        product_text = "\n".join(
            f"- {p['name']} | Gia: {p['price']:,.0f}$ | "
            f"CPU: {p['specs']['cpu']}, RAM: {p['specs']['ram']}, Camera: {p['specs']['camera']}"
            for p in mobiles
        )

    return f"""<|system|>
Ban la tro ly tu van ban dien thoai di dong than thien.
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
