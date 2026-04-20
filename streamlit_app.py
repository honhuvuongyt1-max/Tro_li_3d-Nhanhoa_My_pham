import streamlit as st
import google.generativeai as genai
import base64
from PIL import Image
import io
import os

# ─── CẤU HÌNH ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tool Tạo Video Nhân Hóa 3D - Mỹ Phẩm",
    page_icon="💄",
    layout="wide"
)

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    header {visibility: hidden;}  /* FIX HEADER */

    .main { background: #f0f2f6; }

    /* FIX BỊ CHE */
    .block-container { 
        padding: 1rem 1.5rem;
        padding-top: 80px !important;
    }

    .header-box {
        display: flex; align-items: center; gap: 14px;
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 14px; padding: 14px 20px; margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── DỮ LIỆU CHỦ ĐỀ MẪU ─────────────────────────────────────────────────────
CHU_DE_MAU = {
    "💄 3D Mỹ phẩm (Hot Trend)": [
        "Serum nhân hóa kể chuyện hấp thụ vào da",
        "Son môi ghen tị với son khác",
        "Kem chống nắng chiến đấu với tia UV",
        "Retinol biến hình ban đêm",
        "Niacinamide cứu làn da mụn",
    ],
    "💄 Mỹ phẩm & Làm đẹp": [
        "Serum Vitamin C có tác dụng gì cho da",
        "Cách dùng kem chống nắng đúng cách",
    ],
    "🎓 Giáo dục - Học tập": [
        "Giải thích skincare cho người mới",
        "Cách đọc bảng thành phần mỹ phẩm",
    ],
    "✨ Nhân hóa 3D & Xu hướng": [
        "Mascara khóc vì bị dùng sai",
        "Son môi tự kể câu chuyện của mình",
    ]
}

# ─── HELPER ──────────────────────────────────────────────────────────────────
def image_to_base64(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def call_gemini(prompt, image=None):
    if not GEMINI_API_KEY:
        return "⚠️ Chưa có GEMINI_API_KEY trong Secrets."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        if image:
            b64 = image_to_base64(image)
            response = model.generate_content([{"mime_type": "image/png", "data": b64}, prompt])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Lỗi Gemini: {str(e)}"

# ─── SESSION STATE ────────────────────────────────────────────────────────────
for key, val in {
    "result": None, "chu_de": "", "show_chu_de": False,
    "nhan_vat_ai": "", "boi_canh_ai": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <div style="font-size:2.5rem">💄</div>
    <div>
        <div style="color:white;font-size:1.4rem;font-weight:800;">🎬 Tool Tạo Video Nhân Hóa 3D</div>
        <div style="color:#a78bfa;font-size:0.85rem;">AI hỗ trợ tạo video viral</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── UI ──────────────────────────────────────────────────────────────────────

st.markdown("### 📌 Chủ đề Video (BẮT BUỘC)")

if st.button("📋 Chọn chủ đề mẫu"):
    st.session_state.show_chu_de = not st.session_state.show_chu_de

chu_de = st.text_input(
    "", 
    value=st.session_state.chu_de,
    placeholder="Nhập chủ đề..."
)

# FIX: cập nhật realtime
st.session_state.chu_de = chu_de

# popup chọn chủ đề
if st.session_state.show_chu_de:
    for danh_muc, ds in CHU_DE_MAU.items():
        st.markdown(f"**{danh_muc}**")
        for cd in ds:
            if st.button(cd):
                st.session_state.chu_de = cd
                st.rerun()

# PHONG CÁCH
phong_cach = st.selectbox("🎨 Phong cách", [
    "Châm biếm","Hài hước","Cảm xúc","Kịch tính","Cute dễ thương","Nghiêm túc","Giáo dục"
])

# NHÂN VẬT
st.markdown("### 🧍 Nhân vật / Đồ vật")
nhan_vat = st.text_input("", value=st.session_state.nhan_vat_ai)

if st.button("🤖 AI gợi ý nhân vật"):
    if chu_de:
        res = call_gemini(f"Gợi ý nhân vật cho chủ đề: {chu_de}")
        st.session_state.nhan_vat_ai = res
        st.rerun()
    else:
        st.warning("Nhập chủ đề trước!")

# BỐI CẢNH
st.markdown("### 🌍 Bối cảnh ưu tiên")
boi_canh = st.text_input("", value=st.session_state.boi_canh_ai)

if st.button("✨ AI tạo bối cảnh từ kịch bản"):
    if chu_de:
        res = call_gemini(f"Tạo bối cảnh video cho: {chu_de}")
        st.session_state.boi_canh_ai = res
        st.rerun()
    else:
        st.warning("Nhập chủ đề trước!")

# OUTPUT
st.markdown("### 🚀 Kết quả")
if st.button("Tạo Prompt"):
    if not chu_de:
        st.warning("Phải nhập chủ đề!")
    else:
        st.write("Chủ đề:", chu_de)
        st.write("Phong cách:", phong_cach)
        st.write("Nhân vật:", nhan_vat)
        st.write("Bối cảnh:", boi_canh)