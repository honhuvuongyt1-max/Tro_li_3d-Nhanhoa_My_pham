import streamlit as st
import google.generativeai as genai
import base64
from PIL import Image
import io
import json

# ─── CẤU HÌNH ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tool Tạo Video Nhân Hóa 3D",
    page_icon="🎬",
    layout="wide"
)

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background: #f8f9fa; }
    .block-container { padding: 1.5rem 2rem; }
    h1 { font-size: 1.6rem !important; font-weight: 700 !important; }
    .section-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .section-title {
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .result-box {
        background: white;
        border-radius: 12px;
        padding: 1.4rem;
        min-height: 400px;
        border: 1px solid #e9ecef;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .btn-main > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        width: 100%;
        padding: 0.6rem !important;
    }
    .btn-green > button {
        background: #28a745 !important;
        color: white !important;
        border: none !important;
        width: 100%;
    }
    .tag-pill {
        display: inline-block;
        background: #f0f0f0;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.78rem;
        margin: 2px;
        cursor: pointer;
        border: 1px solid #ddd;
    }
    .result-empty {
        text-align: center;
        color: #adb5bd;
        margin-top: 80px;
    }
    .result-empty .icon { font-size: 2.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── DỮ LIỆU CHỦ ĐỀ MẪU ────────────────────────────────────────────────────
CHU_DE_MAU = {
    "💄 Mỹ phẩm & Làm đẹp": [
        "Serum Vitamin C có tác dụng gì cho da",
        "Cách dùng kem chống nắng đúng cách",
        "Tẩy trang dầu vs nước - cái nào tốt hơn",
        "Retinol là gì và dùng như thế nào",
        "Son dưỡng có thực sự dưỡng môi không",
        "Kem dưỡng ẩm ban ngày vs ban đêm khác gì",
        "Niacinamide - thần dược trị thâm mụn",
        "Cách chăm sóc da dầu mụn đúng chuẩn",
        "AHA BHA là gì - có nên dùng không",
        "Collagen uống hay bôi hiệu quả hơn",
    ],
    "✨ Nhân hóa 3D & Xu hướng": [
        "Cây cỏ nổi giận khi bị hái lá",
        "Viên serum tự kể chuyện hành trình lên da",
        "Mascara khóc vì bị dùng không đúng cách",
        "Son môi ghen tị với son bạn gái khác",
        "Kem chống nắng bị bỏ quên trong túi xách",
        "Bộ skincare tranh nhau được dùng trước",
        "Cục tẩy trang sợ bị vứt bỏ",
        "Chai nước hoa cuối cùng trong lọ",
        "Miếng mặt nạ kể chuyện 20 phút trên mặt",
        "Cây son tự nhận xét về màu của mình",
    ],
    "🌿 Nguyên liệu thiên nhiên": [
        "Nghệ có thực sự trị mụn không",
        "Dầu dừa dùng cho da mặt được không",
        "Nha đam - công dụng thật vs lời đồn",
        "Trà xanh bôi mặt có tốt không",
        "Mật ong làm đẹp da đúng cách",
        "Gạo lứt và bí quyết làng đẹp Nhật Bản",
        "Dầu hoa hồng - xa xỉ phẩm hay thực sự hiệu quả",
        "Bơ shea là gì và dùng thế nào",
    ],
    "💆 Chăm sóc da chuyên sâu": [
        "Da nhạy cảm nên dùng gì và tránh gì",
        "Cách trị thâm mụn nhanh nhất",
        "Lỗ chân lông to phải làm sao",
        "Da khô bong tróc mùa lạnh - cách xử lý",
        "Cách làm đều màu da mặt tự nhiên",
        "Vùng chữ T dầu mà má khô - combo da hỗn hợp",
        "Cách chăm sóc da sau khi nặn mụn",
        "Tại sao da vẫn dầu dù đã rửa mặt nhiều lần",
    ],
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
            response = model.generate_content([
                {"mime_type": "image/png", "data": b64},
                prompt
            ])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Lỗi Gemini: {str(e)}"

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "chu_de" not in st.session_state:
    st.session_state.chu_de = ""
if "show_chu_de" not in st.session_state:
    st.session_state.show_chu_de = False

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("## 🎬 Tool Tạo Video Nhân Hóa 3D")
st.markdown(
    '<div style="background:#e8f4fd;padding:8px 14px;border-radius:8px;'
    'font-size:0.9rem;color:#1a73e8;margin-bottom:1rem">'
    '💬 Chào Sếp, em là <b>Nhi</b> - Trợ Lý A.I Của Anh Lập Trình</div>',
    unsafe_allow_html=True
)

# ─── LAYOUT CHÍNH ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.1], gap="medium")

with col_left:
    # Công cụ phụ
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔧 Công cụ tạo Video</div>', unsafe_allow_html=True)
    st.markdown('<div class="btn-green">', unsafe_allow_html=True)
    st.button("↗️ Tải Veo 3", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Cấu hình video
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ Cấu hình Video</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 Từ Chủ Đề", "🎥 Phân tích Video"])

    # ── TAB 1: TỪ CHỦ ĐỀ ────────────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("**Chủ đề Video** *(bắt buộc)*")
        with c2:
            if st.button("📋 Chọn chủ đề mẫu", key="btn_open_chude"):
                st.session_state.show_chu_de = not st.session_state.show_chu_de

        chu_de = st.text_input(
            "", placeholder="Ví dụ: Son môi ghen tị với son bạn gái khác...",
            value=st.session_state.chu_de, key="input_chu_de", label_visibility="collapsed"
        )

        # Popup chọn chủ đề
        if st.session_state.show_chu_de:
            st.markdown("---")
            st.markdown("**📚 Danh sách Chủ đề mẫu**")
            for danh_muc, ds in CHU_DE_MAU.items():
                st.markdown(f"**{danh_muc}**")
                cols = st.columns(2)
                for i, cd in enumerate(ds):
                    with cols[i % 2]:
                        if st.button(cd, key=f"cd_{danh_muc}_{i}", use_container_width=True):
                            st.session_state.chu_de = cd
                            st.session_state.show_chu_de = False
                            st.rerun()
            st.markdown("---")

        c3, c4 = st.columns(2)
        with c3:
            phong_cach = st.selectbox("Phong cách (Voice)", [
                "Châm biếm", "Hài hước", "Cảm xúc", "Kịch tính", "Cute dễ thương", "Nghiêm túc"
            ])
        with c4:
            so_luong = st.number_input("Số lượng", min_value=1, max_value=20, value=5)

        c5, c6 = st.columns(2)
        with c5:
            ty_le = st.selectbox("Tỉ lệ khung hình", ["9:16", "16:9", "1:1"])
        with c6:
            st.text_input("Độ dài (cố định)", value="8 Giây", disabled=True)

        nhan_vat = st.text_input(
            "Nhân vật/Đồ vật cụ thể *(Không bắt buộc)*",
            placeholder="Ví dụ: Cây son MAC, Chai serum La Mer..."
        )
        if st.button("🤖 Gợi ý nhân vật", use_container_width=True):
            if chu_de:
                with st.spinner("Đang gợi ý..."):
                    res = call_gemini(f"Gợi ý 5 nhân vật/đồ vật phù hợp cho video nhân hóa 3D về chủ đề: '{chu_de}'. Trả lời ngắn gọn dạng danh sách.")
                    st.info(res)

        c7, c8 = st.columns(2)
        with c7:
            giong_doc = st.selectbox("Giọng đọc", ["Nam trẻ", "Nữ trẻ", "Nữ dịu dàng", "Nam trầm"])
        with c8:
            ngon_ngu = st.selectbox("Ngôn ngữ Voice", ["Tiếng Việt", "English"])

        hai_huoc = st.slider("Mức độ hài hước", 1, 5, 3)

        boi_canh = st.text_input(
            "Bối cảnh ưu tiên *(Không bắt buộc)*",
            placeholder="Ví dụ: Bàn trang điểm, Studio ánh sáng neon..."
        )
        if st.button("✨ Gợi ý Bối cảnh AI", use_container_width=True):
            if chu_de:
                with st.spinner("Đang gợi ý..."):
                    res = call_gemini(f"Gợi ý 5 bối cảnh 3D đẹp cho video nhân hóa về: '{chu_de}'. Ngắn gọn, sáng tạo.")
                    st.info(res)

        noi_dung_cam = st.text_input("Nội dung cấm (Negative)", value="không nói tục")

        st.markdown('<div class="btn-main">', unsafe_allow_html=True)
        btn_tao = st.button("🚀 Tạo Prompt Ngay", key="btn_tao_prompt", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if btn_tao:
            if not chu_de and not st.session_state.chu_de:
                st.warning("⚠️ Anh chưa nhập chủ đề!")
            else:
                topic = st.session_state.chu_de or chu_de
                with st.spinner("Đang tạo prompt..."):
                    prompt = f"""Tạo {so_luong} prompt video nhân hóa 3D chuyên nghiệp cho Veo 3 với các thông tin:
- Chủ đề: {topic}
- Nhân vật: {nhan_vat or 'tự chọn phù hợp'}
- Phong cách: {phong_cach}
- Bối cảnh: {boi_canh or 'tự chọn'}
- Tỉ lệ: {ty_le}
- Mức hài hước: {hai_huoc}/5
- Không được: {noi_dung_cam}
- Ngôn ngữ voice: {ngon_ngu}

Mỗi prompt gồm:
1. [SCENE] Mô tả cảnh quay chi tiết
2. [CHARACTER] Nhân vật/đồ vật được nhân hóa như thế nào
3. [VOICE] Script lời thoại ngắn (~15 giây)
4. [STYLE] Phong cách hình ảnh 3D
5. [CAMERA] Góc máy và chuyển động

Trả lời bằng tiếng Việt, sáng tạo và hấp dẫn."""
                    result = call_gemini(prompt)
                    st.session_state.result = result

    # ── TAB 2: PHÂN TÍCH VIDEO ───────────────────────────────────────────
    with tab2:
        st.markdown("**Upload Video Mẫu** *")
        video_file = st.file_uploader(
            "", type=["mp4", "mov"],
            label_visibility="collapsed", key="video_upload"
        )
        st.caption("*AI sẽ giữ nguyên hình ảnh từ video nhưng tạo Voice/Script mới*")

        c9, c10 = st.columns(2)
        with c9:
            pc2 = st.selectbox("Phong cách", ["Châm biếm", "Hài hước", "Cảm xúc"], key="pv2")
        with c10:
            sl2 = st.number_input("Số lượng", 1, 10, 5, key="sl2")

        c11, c12 = st.columns(2)
        with c11:
            tl2 = st.selectbox("Tỉ lệ", ["9:16", "16:9"], key="tl2")
        with c12:
            st.text_input("Độ dài", "8 Giây", disabled=True, key="dl2")

        c13, c14 = st.columns(2)
        with c13:
            gd2 = st.selectbox("Giọng đọc", ["Nam trẻ", "Nữ trẻ"], key="gd2")
        with c14:
            nn2 = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"], key="nn2")

        if st.button("🔍 Phân tích & Tạo Prompt", use_container_width=True, key="btn_phan_tich"):
            if not video_file:
                st.warning("⚠️ Anh chưa upload video!")
            else:
                st.info("🔄 Tính năng phân tích video đang được phát triển...")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── UPLOAD ẢNH SẢN PHẨM ──────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📸 Tải ảnh sản phẩm lên</div>', unsafe_allow_html=True)

    uploaded_img = st.file_uploader(
        "Kéo thả file vào đây hoặc Click để duyệt",
        type=["png", "jpg", "jpeg"],
        key="img_upload"
    )

    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, width=200)

        st.markdown("**🤖 Chức năng AI từ ảnh:**")
        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("💬 Gợi ý Caption", use_container_width=True):
                with st.spinner("Đang phân tích ảnh..."):
                    res = call_gemini(
                        "Nhìn vào ảnh sản phẩm mỹ phẩm này, hãy gợi ý 5 caption hấp dẫn cho TikTok/Reels bằng tiếng Việt. Mỗi caption có emoji và hashtag.",
                        image=img
                    )
                    st.session_state.result = res

            if st.button("📝 Tạo Script từ ảnh", use_container_width=True):
                with st.spinner("Đang tạo script..."):
                    res = call_gemini(
                        "Nhìn vào ảnh sản phẩm này, hãy tạo 1 script video ngắn 15 giây theo phong cách nhân hóa 3D hài hước cho TikTok. Bao gồm lời thoại và mô tả cảnh quay.",
                        image=img
                    )
                    st.session_state.result = res

        with col_b:
            if st.button("🔬 Phân tích sản phẩm", use_container_width=True):
                with st.spinner("Đang phân tích..."):
                    res = call_gemini(
                        "Phân tích sản phẩm mỹ phẩm trong ảnh: tên sản phẩm (nếu thấy), loại sản phẩm, công dụng có thể có, đối tượng phù hợp. Trả lời ngắn gọn bằng tiếng Việt.",
                        image=img
                    )
                    st.session_state.result = res

            if st.button("🎨 Tạo Prompt ảnh 3D", use_container_width=True):
                with st.spinner("Đang tạo prompt..."):
                    res = call_gemini(
                        "Dựa vào ảnh sản phẩm này, hãy tạo 3 prompt chi tiết để tạo ảnh 3D animation nhân hóa sản phẩm (như Pixar/Disney style). Mỗi prompt bao gồm: mô tả nhân vật, bối cảnh, ánh sáng, chuyển động, phong cách. Bằng tiếng Anh cho Midjourney/DALL-E.",
                        image=img
                    )
                    st.session_state.result = res

    st.markdown('</div>', unsafe_allow_html=True)

# ─── CỘT PHẢI: KẾT QUẢ ───────────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✨ Kết quả</div>', unsafe_allow_html=True)

    if st.session_state.result:
        st.markdown(st.session_state.result)
        st.divider()
        c_copy, c_clear = st.columns(2)
        with c_copy:
            st.download_button(
                "📥 Tải xuống kết quả",
                data=st.session_state.result,
                file_name="prompt_video.txt",
                mime="text/plain",
                use_container_width=True
            )
        with c_clear:
            if st.button("🗑️ Xóa kết quả", use_container_width=True):
                st.session_state.result = None
                st.rerun()
    else:
        st.markdown("""
        <div class="result-empty">
            <div class="icon">✨</div>
            <p>Chưa có prompt nào.<br>Hãy nhấn <b>"Tạo Prompt"</b> hoặc<br>dùng các nút AI từ ảnh sản phẩm.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
