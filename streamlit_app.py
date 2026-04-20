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
    .main { background: #f0f2f6; }
    .block-container { padding: 1rem 1.5rem; }

    .header-box {
        display: flex; align-items: center; gap: 14px;
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 14px; padding: 14px 20px; margin-bottom: 1rem;
    }
    .header-box img { height: 48px; border-radius: 8px; }
    .header-title { color: white; font-size: 1.4rem; font-weight: 800; line-height: 1.2; }
    .header-sub { color: #a78bfa; font-size: 0.85rem; }

    .greeting {
        background: linear-gradient(90deg, #667eea22, #764ba222);
        border-left: 4px solid #667eea;
        border-radius: 8px; padding: 8px 14px;
        font-size: 0.9rem; color: #4c1d95; margin-bottom: 1rem;
    }

    .section-card {
        background: white; border-radius: 12px;
        padding: 1.1rem 1.3rem; margin-bottom: 0.9rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .section-title {
        font-weight: 700; font-size: 0.95rem;
        color: #1e293b; margin-bottom: 0.7rem;
        display: flex; align-items: center; gap: 6px;
        border-bottom: 2px solid #f1f5f9; padding-bottom: 6px;
    }
    .result-box {
        background: white; border-radius: 12px;
        padding: 1.4rem; min-height: 500px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .stButton > button {
        border-radius: 8px !important; font-weight: 600 !important;
        font-size: 0.85rem !important; transition: all 0.2s !important;
        border: none !important;
    }
    .btn-veo button    { background: #059669 !important; color: white !important; }
    .btn-pink button   { background: linear-gradient(135deg,#ec4899,#be185d) !important; color: white !important; }
    .btn-blue button   { background: linear-gradient(135deg,#3b82f6,#1d4ed8) !important; color: white !important; }
    .btn-orange button { background: linear-gradient(135deg,#f97316,#c2410c) !important; color: white !important; }
    .btn-red button    { background: linear-gradient(135deg,#ef4444,#b91c1c) !important; color: white !important; width:100% !important; font-size:1rem !important; }
    .btn-download button { background: #0891b2 !important; color: white !important; }
    .btn-clear button    { background: #64748b !important; color: white !important; }
    .btn-caption button  { background: linear-gradient(135deg,#8b5cf6,#6d28d9) !important; color: white !important; }
    .btn-script button   { background: linear-gradient(135deg,#06b6d4,#0891b2) !important; color: white !important; }
    .btn-analyze button  { background: linear-gradient(135deg,#10b981,#059669) !important; color: white !important; }
    .btn-prompt3d button { background: linear-gradient(135deg,#f59e0b,#d97706) !important; color: white !important; }

    .result-empty { text-align: center; color: #94a3b8; margin-top: 100px; }
    .result-empty .icon { font-size: 3rem; }
    .chude-popup {
        background: #f8fafc; border-radius: 10px;
        border: 1px solid #e2e8f0; padding: 1rem; margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ─── DỮ LIỆU CHỦ ĐỀ MẪU ─────────────────────────────────────────────────────
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
        "Viên serum tự kể chuyện hành trình lên da",
        "Mascara khóc vì bị dùng không đúng cách",
        "Son môi ghen tị với son bạn gái khác",
        "Kem chống nắng bị bỏ quên trong túi xách",
        "Bộ skincare tranh nhau được dùng trước",
        "Cục tẩy trang sợ bị vứt bỏ",
        "Chai nước hoa cuối cùng trong lọ",
        "Miếng mặt nạ kể chuyện 20 phút trên mặt",
        "Cây son tự nhận xét về màu của mình",
        "Hũ kem dưỡng tâm sự chuyện hết hạn sử dụng",
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
logo_path = "logo.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" />'
else:
    logo_html = '<div style="font-size:2.5rem">💄</div>'

st.markdown(f"""
<div class="header-box">
    {logo_html}
    <div>
        <div class="header-title">🎬 Tool Tạo Video Nhân Hóa 3D — Mỹ Phẩm</div>
        <div class="header-sub">✨ Tạo prompt video viral tự động với AI</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="greeting">💬 Chào Sếp, em là <b>Nhi</b> - Trợ Lý A.I Của Anh Lập Trình 🤖</div>',
    unsafe_allow_html=True
)

# ─── LAYOUT ──────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.1], gap="medium")

with col_left:

    # Công cụ phụ
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔧 Công cụ tạo Video</div>', unsafe_allow_html=True)
    st.markdown('<div class="btn-veo">', unsafe_allow_html=True)
    st.button("↗️ Mở Veo 3", use_container_width=True, key="btn_veo3")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Cấu hình
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ Cấu hình Video</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 Từ Chủ Đề", "🎥 Phân tích Video"])

    with tab1:
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown("**Chủ đề Video** *(bắt buộc)*")
        with c2:
            st.markdown('<div class="btn-pink">', unsafe_allow_html=True)
            if st.button("📋 Chọn chủ đề mẫu", key="btn_open_chude", use_container_width=True):
                st.session_state.show_chu_de = not st.session_state.show_chu_de
            st.markdown('</div>', unsafe_allow_html=True)

        chu_de = st.text_input(
            "", placeholder="Ví dụ: Son môi ghen tị với son bạn gái khác...",
            value=st.session_state.chu_de, key="input_chu_de",
            label_visibility="collapsed"
        )

        if st.session_state.show_chu_de:
            st.markdown('<div class="chude-popup">', unsafe_allow_html=True)
            st.markdown("**📚 Bấm để chọn chủ đề:**")
            for danh_muc, ds in CHU_DE_MAU.items():
                st.markdown(f"**{danh_muc}**")
                cols = st.columns(2)
                for i, cd in enumerate(ds):
                    with cols[i % 2]:
                        if st.button(cd, key=f"cd_{danh_muc}_{i}", use_container_width=True):
                            st.session_state.chu_de = cd
                            st.session_state.show_chu_de = False
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            phong_cach = st.selectbox("Phong cách (Voice)", [
                "Châm biếm","Hài hước","Cảm xúc","Kịch tính","Cute dễ thương","Nghiêm túc"])
        with c4:
            so_luong = st.number_input("Số lượng", 1, 20, 5)

        c5, c6 = st.columns(2)
        with c5:
            ty_le = st.selectbox("Tỉ lệ khung hình", ["9:16","16:9","1:1"])
        with c6:
            st.text_input("Độ dài (cố định)", value="8 Giây", disabled=True)

        # Nhân vật
        st.markdown("**Nhân vật/Đồ vật** *(Không bắt buộc)*")
        nv1, nv2 = st.columns([3, 2])
        with nv1:
            nhan_vat = st.text_input("", key="input_nhan_vat",
                placeholder="Ví dụ: Son MAC, Serum La Mer...",
                value=st.session_state.nhan_vat_ai, label_visibility="collapsed")
        with nv2:
            st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
            if st.button("🤖 AI gợi ý nhân vật", use_container_width=True, key="btn_nhanvat"):
                topic = st.session_state.chu_de or chu_de
                if topic:
                    with st.spinner("AI đang gợi ý..."):
                        res = call_gemini(
                            f"Gợi ý 5 nhân vật/đồ vật mỹ phẩm để nhân hóa 3D cho video về: '{topic}'. "
                            "Dạng danh sách ngắn, mỗi dòng 1 nhân vật.")
                        st.session_state.nhan_vat_ai = res
                        st.session_state.result = res
                else:
                    st.warning("Nhập chủ đề trước nhé anh!")
            st.markdown('</div>', unsafe_allow_html=True)

        c7, c8 = st.columns(2)
        with c7:
            giong_doc = st.selectbox("Giọng đọc", ["Nam trẻ","Nữ trẻ","Nữ dịu dàng","Nam trầm"])
        with c8:
            ngon_ngu = st.selectbox("Ngôn ngữ Voice", ["Tiếng Việt","English"])

        hai_huoc = st.slider("Mức độ hài hước", 1, 5, 3)

        # Bối cảnh
        st.markdown("**Bối cảnh ưu tiên** *(Không bắt buộc)*")
        bc1, bc2 = st.columns([3, 2])
        with bc1:
            boi_canh = st.text_input("", key="input_boi_canh",
                placeholder="Ví dụ: Bàn trang điểm, Studio neon...",
                value=st.session_state.boi_canh_ai, label_visibility="collapsed")
        with bc2:
            st.markdown('<div class="btn-orange">', unsafe_allow_html=True)
            if st.button("✨ AI đọc kịch bản", use_container_width=True, key="btn_boicanh"):
                topic = st.session_state.chu_de or chu_de
                nv = nhan_vat or "sản phẩm mỹ phẩm"
                if topic:
                    with st.spinner("AI đang phân tích kịch bản..."):
                        res = call_gemini(
                            f"Dựa vào kịch bản video nhân hóa 3D về '{topic}' với nhân vật '{nv}', "
                            "gợi ý 3 bối cảnh 3D phù hợp nhất (Pixar/Disney style). "
                            "Mỗi bối cảnh 1 dòng, ngắn gọn, phù hợp mỹ phẩm.")
                        st.session_state.boi_canh_ai = res
                        st.session_state.result = res
                else:
                    st.warning("Nhập chủ đề trước nhé anh!")
            st.markdown('</div>', unsafe_allow_html=True)

        noi_dung_cam = st.text_input("Nội dung cấm (Negative)", value="không nói tục")

        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        btn_tao = st.button("🚀 Tạo Prompt Ngay", key="btn_tao_prompt", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if btn_tao:
            topic = st.session_state.chu_de or chu_de
            if not topic:
                st.warning("⚠️ Anh chưa nhập chủ đề!")
            else:
                with st.spinner("⚡ Đang tạo prompt..."):
                    prompt = f"""Tạo {so_luong} prompt video nhân hóa 3D mỹ phẩm chuyên nghiệp cho Veo 3:
- Chủ đề: {topic}
- Nhân vật: {nhan_vat or 'tự chọn phù hợp'}
- Phong cách: {phong_cach}
- Bối cảnh: {boi_canh or st.session_state.boi_canh_ai or 'tự chọn'}
- Tỉ lệ: {ty_le}, Độ dài: 8 giây
- Mức hài hước: {hai_huoc}/5
- Không được: {noi_dung_cam}
- Ngôn ngữ voice: {ngon_ngu}

Mỗi prompt gồm:
1. [SCENE] Mô tả cảnh quay chi tiết
2. [CHARACTER] Nhân vật mỹ phẩm được nhân hóa
3. [VOICE] Script lời thoại ~15 giây
4. [STYLE] Phong cách 3D Pixar/Disney
5. [CAMERA] Góc máy và chuyển động

Trả lời tiếng Việt, sáng tạo và viral."""
                    st.session_state.result = call_gemini(prompt)

    with tab2:
        st.markdown("**Upload Video Mẫu** *(MP4, MOV - Max 50MB)*")
        video_file = st.file_uploader("", type=["mp4","mov"],
            label_visibility="collapsed", key="video_upload")
        st.caption("*AI giữ nguyên hình ảnh, tạo Voice/Script mới*")

        c9, c10 = st.columns(2)
        with c9:
            st.selectbox("Phong cách", ["Châm biếm","Hài hước","Cảm xúc"], key="pv2")
        with c10:
            st.number_input("Số lượng", 1, 10, 5, key="sl2")

        c11, c12 = st.columns(2)
        with c11:
            st.selectbox("Tỉ lệ", ["9:16","16:9"], key="tl2")
        with c12:
            st.text_input("Độ dài", "8 Giây", disabled=True, key="dl2")

        c13, c14 = st.columns(2)
        with c13:
            st.selectbox("Giọng đọc", ["Nam trẻ","Nữ trẻ"], key="gd2")
        with c14:
            st.selectbox("Ngôn ngữ", ["Tiếng Việt","English"], key="nn2")

        st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
        if st.button("🔍 Phân tích & Tạo Prompt", use_container_width=True, key="btn_phan_tich"):
            if not video_file:
                st.warning("⚠️ Anh chưa upload video!")
            else:
                st.info("🔄 Tính năng đang phát triển...")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Upload ảnh sản phẩm
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📸 Tải ảnh sản phẩm lên</div>', unsafe_allow_html=True)

    uploaded_img = st.file_uploader(
        "Kéo thả PNG/JPG vào đây hoặc Click để chọn",
        type=["png","jpg","jpeg"], key="img_upload")

    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, width=180)
        st.markdown("**🤖 Chức năng AI từ ảnh:**")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="btn-caption">', unsafe_allow_html=True)
            if st.button("💬 Gợi ý Caption", use_container_width=True, key="btn_caption"):
                with st.spinner("Đang phân tích..."):
                    st.session_state.result = call_gemini(
                        "Gợi ý 5 caption TikTok/Reels về sản phẩm mỹ phẩm trong ảnh. Có emoji và hashtag. Tiếng Việt.", image=img)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="btn-script">', unsafe_allow_html=True)
            if st.button("📝 Tạo Script từ ảnh", use_container_width=True, key="btn_script"):
                with st.spinner("Đang tạo script..."):
                    st.session_state.result = call_gemini(
                        "Tạo script video 15 giây nhân hóa 3D hài hước từ sản phẩm trong ảnh. Lời thoại + mô tả cảnh. Tiếng Việt.", image=img)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="btn-analyze">', unsafe_allow_html=True)
            if st.button("🔬 Phân tích sản phẩm", use_container_width=True, key="btn_analyze"):
                with st.spinner("Đang phân tích..."):
                    st.session_state.result = call_gemini(
                        "Phân tích sản phẩm mỹ phẩm trong ảnh: tên, loại, công dụng, đối tượng. Ngắn gọn, tiếng Việt.", image=img)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="btn-prompt3d">', unsafe_allow_html=True)
            if st.button("🎨 Tạo Prompt ảnh 3D", use_container_width=True, key="btn_prompt3d"):
                with st.spinner("Đang tạo prompt 3D..."):
                    st.session_state.result = call_gemini(
                        "Tạo 3 prompt tiếng Anh để tạo ảnh 3D animation nhân hóa sản phẩm mỹ phẩm trong ảnh (Pixar/Disney style). Mỗi prompt: nhân vật, bối cảnh, ánh sáng, chuyển động.", image=img)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─── KẾT QUẢ ─────────────────────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✨ Kết quả</div>', unsafe_allow_html=True)

    if st.session_state.result:
        st.markdown(st.session_state.result)
        st.divider()
        cd1, cd2 = st.columns(2)
        with cd1:
            st.markdown('<div class="btn-download">', unsafe_allow_html=True)
            st.download_button("📥 Tải xuống", data=st.session_state.result,
                file_name="prompt_video.txt", mime="text/plain", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with cd2:
            st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
            if st.button("🗑️ Xóa kết quả", use_container_width=True, key="btn_clear"):
                st.session_state.result = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-empty">
            <div class="icon">✨</div><br>
            <p><b>Chưa có kết quả nào</b><br><br>
            Nhập chủ đề → bấm <b>🚀 Tạo Prompt Ngay</b><br>
            hoặc upload ảnh → dùng các nút AI bên trái</p>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
