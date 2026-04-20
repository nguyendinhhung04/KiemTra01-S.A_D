# BÁO CÁO BÀI TẬP LỚN: THIẾT KẾ HỆ THỐNG PHẦN MỀM
## ĐỀ TÀI: XÂY DỰNG HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ ĐA DỊCH VỤ TÍCH HỢP TRỢ LÝ ẢO AI LOCAL (RAG)

---

## MỤC LỤC
1. GIỚI THIỆU DỰ ÁN
2. KIẾN TRÚC HỆ THỐNG (MICROSERVICES)
3. THIẾT KẾ MÃ NGUỒN VÀ DỮ LIỆU (PRODUCT DESIGN)
4. TÍCH HỢP DỊCH VỤ AI (LOCAL DEEP LEARNING, KNOWLEDGE BASE, RAG)
5. QUY TRÌNH NGHIỆP VỤ E-COMMERCE
6. CÔNG NGHỆ VÀ TRIỂN KHAI (DOCKER, TRANSFORMERS)
7. KẾT LUẬN
8. PHỤ LỤC: HÌNH ẢNH MÃ NGUỒN (4 TRANG)

---

## 1. GIỚI THIỆU DỰ ÁN
Dự án tập trung vào việc xây dựng một nền tảng thương mại điện tử hiện đại áp dụng kiến trúc Microservices. Điểm nhấn của dự án là việc tích hợp Trợ lý ảo AI chạy trực tiếp trên hạ tầng của hệ thống (Local Inference), không phụ thuộc vào các dịch vụ đám mây bên thứ ba, nhằm đảm bảo tính bảo mật dữ liệu và giảm chi phí vận hành.

---

## 2. KIẾN TRÚC HỆ THỐNG (MICROSERVICES)
... (Giữ nguyên phần kiến trúc Service như trước)

---

## 3. THIẾT KẾ MÃ NGUỒN VÀ DỮ LIỆU (PRODUCT DESIGN)
... (Giữ nguyên phần thiết kế Model như trước)

---

## 4. TÍCH HỢP DỊCH VỤ AI (LOCAL DEEP LEARNING, RAG)

### 4.1 Nền tảng Deep Learning Local
Thay vì sử dụng các API trả phí, hệ thống tích hợp thư viện **Hugging Face Transformers** để chạy các mô hình ngôn ngữ lớn (LLM) cục bộ. 
- **Model sử dụng**: `TinyLlama-1.1B-Chat-v1.0`. Đây là model có kích thước nhỏ (khoảng 2.2GB), được tối ưu hóa để có thể chạy trên cả CPU thông thường thông qua kỹ thuật Quantization.
- **Tự động tải model**: Hệ thống sử dụng cơ chế `pipeline` để tự động tải model từ internet trong lần chạy đầu tiên và lưu trữ vào bộ nhớ đệm (cache).

### 4.2 Xây dựng Knowledge Base (Cơ sở tri thức)
Hệ thống sử dụng cơ sở dữ liệu sản phẩm (PostgreSQL) làm Knowledge Base. Dữ liệu được trích xuất động và cấu trúc hóa dưới dạng văn bản để đưa vào bộ nhớ của mô hình AI trước khi thực hiện trả lời.

### 4.3 Quy trình RAG Local (Retrieval-Augmented Generation)
Quy trình thực hiện:
1. **Retrieval**: Truy vấn database để lấy thông tin sản phẩm (tên, giá, thông số).
2. **Context Construction**: Xây dựng prompt theo cấu trúc ChatML (`<|system|>`, `<|user|>`, `<|assistant|>`).
3. **Local Generation**: Model TinyLlama thực hiện suy luận (Inference) dựa trên context vừa xây dựng để đưa ra câu trả lời bằng tiếng Việt.

---

## 5. QUY TRÌNH NGHIỆM VỤ E-COMMERCE
... (Giữ nguyên phần luồng nghiệp vụ như trước)

---

## 6. CÔNG NGHỆ VÀ TRIỂN KHAI

### 6.1 Công nghệ AI
- **Framework**: `PyTorch` và `Transformers`.
- **Optimization**: Sử dụng `torch_dtype=torch.bfloat16` để giảm mức tiêu thụ RAM nhưng vẫn giữ được độ chính xác của model.
- **Singleton Pattern**: Model AI được tải một lần duy nhất vào bộ nhớ thông qua biến toàn cục `_pipe`, giúp các request sau đó có tốc độ phản hồi cực nhanh.

### 6.2 Triển khai với Docker
Các service được đóng gói bao gồm cả các thư viện AI. Khi khởi chạy, Docker container sẽ đảm nhiệm việc cài đặt môi trường Torch và tải model về volume lưu trữ.

---

## 7. KẾT LUẬN
Việc chuyển đổi sang mô hình AI Local giúp dự án làm chủ hoàn toàn công nghệ. Hệ thống không chỉ có khả năng quản lý sản phẩm linh hoạt nhờ Microservices mà còn cung cấp trải nghiệm mua sắm thông minh, riêng tư và hoàn toàn miễn phí về chi phí duy trì API.

---

## 8. PHỤ LỤC: HÌNH ẢNH MÃ NGUỒN (SOURCE CODE IMAGES)

### TRANG 1: CẤU TRÚC THƯ MỤC VÀ DOCKER CONFIGURATION
\pagebreak
<div style="height: 800px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center;">
    [CHÈN ẢNH: PROJECT STRUCTURE & REQUIREMENTS.TXT VỚI TRANSFORMERS/TORCH]
</div>

---

### TRANG 2: THIẾT KẾ MODEL SẢN PHẨM (LAPTOP & MOBILE SERVICES)
\pagebreak
<div style="height: 800px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center;">
    [CHÈN ẢNH: MODELS.PY - CẤU TRÚC DỮ LIỆU LÀM KNOWLEDGE BASE]
</div>

---

### TRANG 3: LOGIC TRỢ LÝ ẢO AI LOCAL (CHATBOT.PY)
\pagebreak
<div style="height: 800px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center;">
    [CHÈN ẢNH: CHATBOT.PY - SỬ DỤNG HUGGING FACE PIPELINE & TINYLLAMA]
</div>

---

### TRANG 4: HỆ THỐNG GIỎ HÀNG VÀ API GATEWAY
\pagebreak
<div style="height: 800px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center;">
    [CHÈN ẢNH: GATEWAY SERVICES.PY & LOGIC XỬ LÝ ĐƠN HÀNG]
</div>
