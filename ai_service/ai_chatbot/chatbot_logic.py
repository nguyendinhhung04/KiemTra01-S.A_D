import os
import logging
import torch
import threading
from transformers import pipeline
from neomodel import config as neoconfig
from . import graph_models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_pipe = None
_loading_thread = None

def is_model_ready():
    return _pipe is not None

def start_loading_model():
    global _pipe
    try:
        model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        hf_token = os.environ.get('HF_TOKEN')
        logger.info(f"Initializing chatbot model in background: {model_id}...")
        _pipe = pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.float32},
            device="cpu",
            token=hf_token
        )
        logger.info("Chatbot model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load chatbot model: {e}")

# Initialize Neo4j config
neo4j_url = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:password@neo4j:7687')
neoconfig.DATABASE_URL = neo4j_url

# Start loading model in background thread
if _pipe is None and _loading_thread is None:
    _loading_thread = threading.Thread(target=start_loading_model)
    _loading_thread.daemon = True
    _loading_thread.start()

def get_chatbot_pipe():
    global _pipe
    if _pipe is None:
        if _loading_thread and _loading_thread.is_alive():
            logger.info("Waiting for background model loading to complete...")
            _loading_thread.join()
        
        if _pipe is None:
            start_loading_model()
            
        if _pipe is None:
            raise Exception("Failed to initialize chatbot model")
            
    return _pipe

def get_knowledge_base():
    try:
        laptops = graph_models.Laptop.nodes.all()
        mobiles = graph_models.Mobile.nodes.all()
        item_list = []
        
        def get_first_name(rel):
            nodes = rel.all()
            return nodes[0].name if nodes else ""

        for item in laptops:
            item_list.append({
                "type": "Laptop",
                "name": item.name,
                "price": item.price,
                "specs": f"CPU: {get_first_name(item.cpu)}, RAM: {get_first_name(item.ram)}, GPU: {get_first_name(item.gpu)}"
            })
            
        for item in mobiles:
            item_list.append({
                "type": "Mobile",
                "name": item.name,
                "price": item.price,
                "specs": f"CPU: {get_first_name(item.cpu)}, RAM: {get_first_name(item.ram)}, Camera: {get_first_name(item.camera)}"
            })
            
        return item_list
    except Exception as e:
        logger.error(f"Error querying Neo4j: {e}")
        return []

import traceback

def chat(user_message: str) -> str:
    try:
        logger.info(f"Received message: {user_message}")
        items = get_knowledge_base()
        logger.info(f"Using all {len(items)} products for context")
        
        if not items:
            product_text = "Hien chua co san pham nao."
        else:
            product_text = "\n".join(
                f"- {p['name']} ({p['price']}$): {p['specs']}"
                for p in items
            )

        system_prompt = f"Ban la tro ly ban hang. San pham: {product_text}. Tra loi ngan gon bang tieng Viet."

        logger.info("Getting pipe...")
        pipe = get_chatbot_pipe()
        prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{user_message}</s>\n<|assistant|>\n"
        
        logger.info("Starting model inference...")
        with torch.no_grad():
            outputs = pipe(
                prompt,
                max_new_tokens=64,
                do_sample=False,
                pad_token_id=pipe.tokenizer.eos_token_id,
                # Bo qua cac tham so gay canh bao neu can
            )
        logger.info("Inference completed")

        full_response = outputs[0]["generated_text"]
        reply = full_response.split("<|assistant|>\n")[-1]
        return reply.strip()
    except Exception as e:
        logger.error(f"Error in chat logic: {str(e)}")
        logger.error(traceback.format_exc())
        raise e
