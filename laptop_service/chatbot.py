# chatbot/services.py

from google import genai
from google.genai import types
from django.conf import settings
from laptops.models import Laptop

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def get_products_from_db():
    """Lấy toàn bộ sản phẩm laptop từ database."""
    return Laptop.objects.all()


def build_system_prompt(products) -> str:
    if not products.exists():
        product_text = "Hiện chưa có sản phẩm nào."
    else:
        product_text = "\n".join(
            f"- {p.name} | Giá: {p.price:,.0f}đ | "
            f"CPU: {p.cpu}, RAM: {p.ram}, GPU: {p.gpu}, Màn hình: {p.screen} | "
            f"Mô tả: {p.properties}"
            for p in products
        )

    return f"""Bạn là trợ lý tư vấn bán hàng điện tử thân thiện.
Chỉ tư vấn các sản phẩm có trong danh sách dưới đây.
Nếu hết hàng thì thông báo và gợi ý sản phẩm thay thế.
Trả lời ngắn gọn bằng tiếng Việt.

DANH SÁCH SẢN PHẨM:
{product_text}"""


def chat(user_message: str) -> str:
    """
    Gửi tin nhắn tới Gemini API (không lưu lịch sử).

    Args:
        user_message: Tin nhắn của người dùng.

    Returns:
        reply: Câu trả lời từ Gemini.
    """
    products = get_products_from_db()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=build_system_prompt(products),
        ),
    )

    return response.text