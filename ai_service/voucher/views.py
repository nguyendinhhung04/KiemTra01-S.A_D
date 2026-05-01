import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

# Load model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'voucher', 'buy_product_prediction_model.keras')
model = None

try:
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    else:
        print(f"Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")

# Mappings (These should match how the model was trained)
action_map = {
    "VIEW": 0,
    "CLICK": 1,
    "SEARCH": 2,
    "ADD_TO_CART": 3,
    "REMOVE_FROM_CART": 4,
    "ADD_TO_WISHLIST": 5,
    "PURCHASE": 6
}

category_map = {
    "Mobile": 0,
    "Laptop": 1
}

max_len = 10

class PredictVoucherView(APIView):
    def post(self, request):
        if model is None:
            return Response({"error": "Model not loaded"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        user_actions = request.data.get('user_actions', [])
        user_products = request.data.get('user_products', [])
        user_categories = request.data.get('user_categories', [])

        if not (user_actions and user_products and user_categories):
            return Response({"error": "Missing required data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            results = self.predict_from_history(user_actions, user_products, user_categories)
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def predict_from_history(self, user_actions, user_products, user_categories):
        batch_a = []
        batch_p = []
        batch_c = []
        product_list = []
        category_list = []

        product_dict = {}

        for a, p, c in zip(user_actions, user_products, user_categories):
            if p not in product_dict:
                product_dict[p] = {"actions": [], "categories": []}

            product_dict[p]["actions"].append(a)
            product_dict[p]["categories"].append(c)

        # Build batch
        for product, data in product_dict.items():
            # Use 0 for unknown actions/categories
            actions = [action_map.get(x, 0) for x in data["actions"]]
            categories = [category_map.get(x, 0) for x in data["categories"]]

            # Get latest category
            category_name = data["categories"][-1]

            # In the original snippet, products was a list of IDs.
            # We'll assume the model expects a sequence of product IDs or similar.
            # Based on the snippet: products = [product] * len(actions)
            # However, product IDs in the model are usually mapped too.
            # But we'll follow the provided logic:
            products_seq = [product] * len(actions)
            # If products are strings like 'laptop_1', we might need to convert to int
            # or use a product map. For now, we'll try to convert to int or keep as is.
            # Usually product IDs in Keras embeddings are integers.
            clean_product = product
            if isinstance(product, str):
                if '_' in product:
                    try:
                        clean_product = int(product.split('_')[-1])
                    except:
                        pass
                else:
                    try:
                        clean_product = int(product)
                    except:
                        pass

            a_padded = pad_sequences([actions], maxlen=max_len, padding='post')[0]
            p_padded = pad_sequences([[clean_product] * len(actions)], maxlen=max_len, padding='post')[0]
            c_padded = pad_sequences([categories], maxlen=max_len, padding='post')[0]

            batch_a.append(a_padded)
            batch_p.append(p_padded)
            batch_c.append(c_padded)

            product_list.append(product)
            category_list.append(category_name)

        # Convert to numpy
        batch_a = np.array(batch_a)
        batch_p = np.array(batch_p)
        batch_c = np.array(batch_c)

        # Predict
        probs = model.predict([batch_a, batch_p, batch_c], verbose=0)

        # Format output
        results = []
        for i in range(len(product_list)):
            results.append({
                "product_id": product_list[i],
                "category": category_list[i],
                "probability": float(probs[i][0])
            })

        # Sort by probability descending
        results = sorted(results, key=lambda x: x["probability"], reverse=True)

        return results
