# Microservice System Redesign - AI Service Extraction

## Overview
This project has been refactored to extract AI chatbot capabilities into a dedicated microservice. This improves resource utilization and provides a centralized AI logic hub.

## Key Changes
1.  **AI Service (`ai_service`)**: 
    *   Framework: Django.
    *   Responsibility: Handles all product consultation requests (Laptop & Mobile).
    *   Model: TinyLlama-1.1B-Chat-v1.0.
    *   Optimization: Model is pre-downloaded during Docker build and uses `bfloat16` for memory efficiency.
2.  **API Gateway**:
    *   Unified routing: All chat requests are now routed through `/api/ai-service/ai/chat/`.
3.  **Laptop & Mobile Services**:
    *   Removed `torch`, `transformers`, and `chatbot.py`.
    *   Significantly reduced RAM footprint.
4.  **Frontend**:
    *   Updated `home.html` and `cart.html` to use the unified AI endpoint with a `type` parameter (`laptop` or `mobile`).

## How to Run
1.  **Rebuild the containers**:
    ```bash
    docker-compose up --build
    ```
    *Note: The first build will take some time as it downloads the 2.5GB model and bakes it into the image.*
2.  **Access the application**:
    *   Home: `http://localhost:8003/home/`
    *   Gateway: `http://localhost:8005/`
    *   AI Service: `http://localhost:8005/api/ai-service/ai/chat/` (via Gateway)

## Technical Notes
*   The AI Service connects directly to Neo4j to retrieve real-time knowledge base data.
*   System Prompts are dynamically generated based on the `type` parameter to provide specialized consultation for Laptops or Mobiles.
*   Timeout for AI requests is set to 600 seconds in the Gateway to accommodate CPU inference times.
