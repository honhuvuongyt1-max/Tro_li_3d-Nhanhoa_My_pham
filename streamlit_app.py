<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>AI Video Builder</title>

<style>
body {
    font-family: Arial;
    margin: 0;
    background: #f5f5f5;
}

/* FIX HEADER KHÔNG BỊ CHE */
header {
    position: fixed;
    top: 0;
    width: 100%;
    background: #111;
    color: white;
    padding: 15px;
    z-index: 999;
}

/* CONTENT KHÔNG BỊ CHE */
.container {
    margin-top: 80px;
    padding: 20px;
}

/* UI */
.box {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

input, select, textarea {
    width: 100%;
    padding: 10px;
    margin-top: 8px;
}

button {
    margin-top: 10px;
    padding: 8px 12px;
    border: none;
    background: #007bff;
    color: white;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background: #0056b3;
}
</style>
</head>

<body>

<header>
    🚀 AI VIDEO SYSTEM - Út YouTube Build
</header>

<div class="container">

    <!-- CHỦ ĐỀ -->
    <div class="box">
        <label>📌 Chọn chủ đề:</label>
        <select id="topicSelect">
            <option value="">-- Chọn chủ đề --</option>
            <option>3D Mỹ phẩm</option>
            <option>Review sản phẩm</option>
            <option>Video sức khỏe</option>
            <option>Quân sự giả lập</option>
            <option>What If (Giả định)</option>
            <option>Kể chuyện ma</option>
            <option>Động lực - phát triển bản thân</option>
            <option>Công nghệ AI</option>
            <option>Top list (Top 5, Top 10)</option>
            <option>Giáo dục - học tập</option>
            <option>Affiliate bán hàng</option>
        </select>

        <label>🎯 Chủ đề video (BẮT BUỘC):</label>
        <input id="topicInput" placeholder="Tự động điền khi chọn...">
    </div>

    <!-- PHONG CÁCH -->
    <div class="box">
        <label>🎨 Phong cách:</label>
        <select>
            <option>Giải trí</option>
            <option>Cinematic</option>
            <option>Hài hước</option>
            <option>Drama</option>
            <option>Giáo dục</option> <!-- ĐÃ THÊM -->
        </select>
    </div>

    <!-- NHÂN VẬT -->
    <div class="box">
        <label>🧍 Nhân vật / Đồ vật:</label>
        <input id="characterInput" placeholder="Nhập hoặc dùng AI gợi ý">

        <button onclick="aiSuggestCharacter()">🤖 AI gợi ý nhân vật</button>
    </div>

    <!-- KỊCH BẢN -->
    <div class="box">
        <label>📝 Kịch bản:</label>
        <textarea id="scriptInput" rows="5" placeholder="Dán kịch bản vào đây..."></textarea>
    </div>

    <!-- BỐI CẢNH -->
    <div class="box">
        <label>🌍 Bối cảnh ưu tiên:</label>
        <input id="sceneInput" placeholder="Tự nhập hoặc AI tạo">

        <button onclick="aiGenerateScene()">🤖 AI tạo bối cảnh từ kịch bản</button>
    </div>

</div>

<script>

/* AUTO ĐỔ CHỦ ĐỀ */
document.getElementById("topicSelect").addEventListener("change", function(){
    document.getElementById("topicInput").value = this.value;
});


/* AI GỢI Ý NHÂN VẬT */
function aiSuggestCharacter() {

    let topics = document.getElementById("topicInput").value;

    if (!topics) {
        alert("Chọn chủ đề trước!");
        return;
    }

    let suggestions = {
        "3D Mỹ phẩm": "Cô gái da đẹp + chai serum phát sáng 3D",
        "Review sản phẩm": "Người dùng thật + sản phẩm cận cảnh",
        "Video sức khỏe": "Bác sĩ + bệnh nhân lớn tuổi",
        "Quân sự giả lập": "Lính đặc nhiệm + xe tăng",
        "What If (Giả định)": "Nhân vật giả tưởng + quái vật",
        "Kể chuyện ma": "Nhân vật bí ẩn + bóng đen",
        "Động lực - phát triển bản thân": "Doanh nhân + người thất bại",
        "Công nghệ AI": "Robot AI + con người",
        "Top list (Top 5, Top 10)": "MC + hình ảnh minh họa",
        "Giáo dục - học tập": "Giáo viên + học sinh",
        "Affiliate bán hàng": "Người review + sản phẩm"
    };

    document.getElementById("characterInput").value =
        suggestions[topics] || "Nhân vật phù hợp với nội dung";
}


/* AI TẠO BỐI CẢNH */
function aiGenerateScene() {

    let script = document.getElementById("scriptInput").value;

    if (!script) {
        alert("Nhập kịch bản trước!");
        return;
    }

    // Fake AI logic (sau này nối GPT API)
    let scene = "";

    if (script.includes("bác sĩ") || script.includes("sức khỏe")) {
        scene = "Phòng khám hiện đại, ánh sáng trắng, màn hình y khoa";
    }
    else if (script.includes("chiến đấu") || script.includes("quân")) {
        scene = "Chiến trường khói bụi, xe tăng, ánh sáng cháy nổ";
    }
    else if (script.includes("ma") || script.includes("bí ẩn")) {
        scene = "Ngôi nhà tối, ánh sáng yếu, sương mù";
    }
    else {
        scene = "Studio chuyên nghiệp, ánh sáng cinematic";
    }

    document.getElementById("sceneInput").value = scene;
}

</script>

</body>
</html>