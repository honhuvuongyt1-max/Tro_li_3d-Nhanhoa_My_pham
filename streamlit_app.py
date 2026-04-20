import streamlit as st

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="AI Video Builder", layout="wide")

# ======================
# CSS (FIX HEADER + UI)
# ======================
st.markdown("""
<style>
header {visibility: hidden;}

.main-title {
    position: fixed;
    top: 0;
    width: 100%;
    background: #111;
    color: white;
    padding: 15px;
    z-index: 999;
    font-size: 20px;
}

.block-container {
    padding-top: 80px;
}

.box {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-title">🚀 AI VIDEO SYSTEM - Út YouTube</div>', unsafe_allow_html=True)

# ======================
# DATA
# ======================
topics = [
    "3D Mỹ phẩm",
    "Review sản phẩm",
    "Video sức khỏe",
    "Quân sự giả lập",
    "What If (Giả định)",
    "Kể chuyện ma",
    "Động lực - phát triển bản thân",
    "Công nghệ AI",
    "Top list (Top 5, Top 10)",
    "Giáo dục - học tập",
    "Affiliate bán hàng"
]

styles = [
    "Giải trí",
    "Cinematic",
    "Hài hước",
    "Drama",
    "Giáo dục"
]

# ======================
# UI
# ======================
st.markdown("## 📌 Chọn chủ đề")
selected_topic = st.selectbox("Chọn chủ đề:", topics)

topic_input = st.text_input("🎯 Chủ đề video (BẮT BUỘC):", value=selected_topic)

# ======================
# PHONG CÁCH
# ======================
st.markdown("## 🎨 Phong cách")
selected_style = st.selectbox("Chọn phong cách:", styles)

# ======================
# NHÂN VẬT
# ======================
st.markdown("## 🧍 Nhân vật / Đồ vật")

character_input = st.text_input("Nhập hoặc dùng AI gợi ý:")

if st.button("🤖 AI gợi ý nhân vật"):
    suggestions = {
        "3D Mỹ phẩm": "Cô gái da đẹp + serum phát sáng 3D",
        "Review sản phẩm": "Người dùng thật + sản phẩm",
        "Video sức khỏe": "Bác sĩ + người lớn tuổi",
        "Quân sự giả lập": "Lính + xe tăng",
        "What If (Giả định)": "Nhân vật giả tưởng + quái vật",
        "Kể chuyện ma": "Nhân vật bí ẩn + bóng đen",
        "Động lực - phát triển bản thân": "Doanh nhân + người thất bại",
        "Công nghệ AI": "Robot + con người",
        "Top list (Top 5, Top 10)": "MC + hình minh họa",
        "Giáo dục - học tập": "Giáo viên + học sinh",
        "Affiliate bán hàng": "Người review + sản phẩm"
    }

    character_input = suggestions.get(selected_topic, "Nhân vật phù hợp")
    st.success(character_input)

# ======================
# KỊCH BẢN
# ======================
st.markdown("## 📝 Kịch bản")
script_input = st.text_area("Dán kịch bản vào đây:", height=150)

# ======================
# BỐI CẢNH
# ======================
st.markdown("## 🌍 Bối cảnh ưu tiên")

scene_input = st.text_input("Tự nhập hoặc dùng AI tạo:")

if st.button("🤖 AI tạo bối cảnh từ kịch bản"):

    if not script_input:
        st.warning("⚠️ Nhập kịch bản trước!")
    else:
        if "bác sĩ" in script_input or "sức khỏe" in script_input:
            scene = "Phòng khám hiện đại, ánh sáng trắng"
        elif "chiến đấu" in script_input or "quân" in script_input:
            scene = "Chiến trường, khói bụi, xe tăng"
        elif "ma" in script_input:
            scene = "Ngôi nhà tối, sương mù"
        else:
            scene = "Studio ánh sáng cinematic"

        scene_input = scene
        st.success(scene)

# ======================
# OUTPUT (DEBUG)
# ======================
st.markdown("## 🔍 Kết quả")

st.write("Chủ đề:", topic_input)
st.write("Phong cách:", selected_style)
st.write("Nhân vật:", character_input)
st.write("Bối cảnh:", scene_input)