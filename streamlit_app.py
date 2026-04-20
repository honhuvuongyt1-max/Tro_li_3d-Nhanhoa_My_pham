import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Cấu hình trang Web
st.set_page_config(page_title="Trợ Lý 3D Commercial", page_icon="🎬", layout="centered")

# Hàm đọc file text
def rfile(name_file):
    try:
        with open(name_file, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""

# 2. Cấu hình Gemini API (Lấy từ phần cài đặt biến môi trường)
try:
    api_key = "AIzaSyDQG0oaRth0C-6yzGxsLJGdSneCr2X9LkM"
    genai.configure(api_key=api_key)
    # Dùng model flash để xử lý cả văn bản và hình ảnh siêu tốc
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("⚠️ Chưa cấu hình GEMINI_API_KEY. Vui lòng thêm vào Secret của nền tảng.")

# 3. Đọc dữ liệu hệ thống
system_prompt = rfile("01.system_trainning.txt")
title_content = rfile("00.xinchao.txt")

# 4. GIAO DIỆN NGƯỜI DÙNG (Giống y hệt ảnh anh gửi)
st.title("🎬 Tool Tạo Video Nhân Hóa 3D")
if title_content:
    st.info(title_content)

st.markdown("### ⚙️ Cài đặt kịch bản")

# Các ô nhập liệu
topic = st.text_input("Chủ đề (Nội dung chính)", placeholder="Ví dụ: Công dụng của Serum Meso...")

col1, col2 = st.columns(2)
with col1:
    voice = st.selectbox("Giọng đọc (Voice)", [
        "Nữ trẻ (Năng động/Reviewer)", 
        "Nam trầm (Chuyên gia/Bác sĩ)", 
        "ASMR (Nhẹ nhàng/Thư giãn)",
        "Giọng châm biếm/Hài hước"
    ])
with col2:
    context = st.selectbox("Bối cảnh (Môi trường 3D)", [
        "Bàn trang điểm hiện đại", 
        "Studio tối giản (Đen/Trắng)", 
        "Phòng thí nghiệm High-tech",
        "Thiên nhiên/Organic"
    ])

humor_level = st.slider("Mức độ hài hước/Bắt trend", min_value=1, max_value=5, value=3)

# Ô tải ảnh lên
st.markdown("### 📸 Tải ảnh sản phẩm lên")
uploaded_file = st.file_uploader("Kéo thả file vào đây hoặc Click để duyệt", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Hiển thị ảnh thu nhỏ sau khi tải lên
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh sản phẩm đã tải lên", width=200)

# Nút bấm tạo Prompt
if st.button("🚀 Tạo Prompt Ngay", type="primary", use_container_width=True):
    if not topic:
        st.warning("Vui lòng nhập Chủ đề trước khi tạo Prompt anh nhé!")
    else:
        with st.spinner("⏳ Hệ thống đang phân tích ảnh và viết Prompt 3D..."):
            # Lắp ráp thông tin người dùng chọn thành 1 câu lệnh gửi cho AI
            user_request = f"""
            Hãy tạo kịch bản dựa trên các thông số sau:
            - Chủ đề: {topic}
            - Giọng đọc: {voice}
            - Bối cảnh: {context}
            - Mức độ hài hước (1-5): {humor_level}
            """
            
            try:
                # Nếu có ảnh thì gửi cả ảnh và chữ
                if uploaded_file is not None:
                    response = model.generate_content([system_prompt, user_request, image])
                # Nếu không có ảnh thì chỉ gửi chữ
                else:
                    response = model.generate_content([system_prompt, user_request])
                
                st.success("✅ Đã tạo xong!")
                st.markdown("### 📝 Kết quả của anh đây:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra trong quá trình tạo: {e}")