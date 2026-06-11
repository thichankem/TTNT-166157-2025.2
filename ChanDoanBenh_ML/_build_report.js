// Dung bao cao ChanDoanBenh_ML theo format docx mau (chi noi dung, khong anh)
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  TableOfContents, PageBreak, LevelFormat, Numbering, convertInchesToTwip,
} = require("docx");

const FONT = "Times New Roman";
const SZ = 26;        // 13pt
const OUT = "C:/Users/ADMIN/OneDrive/Máy tính/TTNT-166157-2025.2/BaoCao_ChanDoanBenh_ML.docx";

// ---- helpers ----
function p(text, opts = {}) {
  const runs = Array.isArray(text)
    ? text
    : [new TextRun({ text, font: FONT, size: SZ, bold: opts.bold, italics: opts.italics })];
  return new Paragraph({
    children: runs,
    alignment: opts.align,
    spacing: { after: opts.after ?? 120, line: 276, ...(opts.spacing || {}) },
    indent: opts.indent,
  });
}
function bullet(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SZ })],
    bullet: { level: 0 },
    spacing: { after: 80, line: 276 },
  });
}
function numbered(text, ref) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SZ })],
    numbering: { reference: ref, level: 0 },
    spacing: { after: 80, line: 276 },
  });
}
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, font: FONT, size: 30, bold: true, color: "1F4E79" })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 160, after: 100 },
    children: [new TextRun({ text, font: FONT, size: 28, bold: true, color: "2E75B6" })],
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 120, after: 80 },
    children: [new TextRun({ text, font: FONT, size: 26, bold: true, italics: true })],
  });
}
function imgNote(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 120 },
    children: [new TextRun({ text: `[ Hình: ${text} — chèn ảnh chụp ]`, font: FONT, size: 24, italics: true, color: "808080" })],
  });
}

const children = [];

// ===================== TRANG BÌA =====================
children.push(
  new Paragraph({ spacing: { before: 1200, after: 200 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "TRƯỜNG ĐẠI HỌC ........................", font: FONT, size: 28, bold: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 1000 },
    children: [new TextRun({ text: "KHOA CÔNG NGHỆ THÔNG TIN", font: FONT, size: 26, bold: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: "BÁO CÁO BÀI TẬP LỚN", font: FONT, size: 40, bold: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 800 },
    children: [new TextRun({ text: "NHẬP MÔN TRÍ TUỆ NHÂN TẠO", font: FONT, size: 40, bold: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: "Đề tài: Xây dựng hệ thống chẩn đoán bệnh từ triệu chứng", font: FONT, size: 30, bold: true, italics: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 1200 },
    children: [new TextRun({ text: "bằng thuật toán Machine Learning (module ChanDoanBenh_ML)", font: FONT, size: 30, bold: true, italics: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "Giảng viên hướng dẫn: ........................", font: FONT, size: 26 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "Nhóm sinh viên thực hiện: ........................", font: FONT, size: 26 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "Hà Nội, 2025", font: FONT, size: 26, italics: true })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ===================== MUC LUC =====================
children.push(
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 },
    children: [new TextRun({ text: "MỤC LỤC", font: FONT, size: 32, bold: true })] }),
  new TableOfContents("Mục lục", { hyperlink: true, headingStyleRange: "1-3" }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ===================== CHUONG 1 =====================
children.push(h1("CHƯƠNG 1: MỞ ĐẦU"));

children.push(h2("1.1. Lý do chọn đề tài"));
children.push(p("Trong những năm gần đây, trí tuệ nhân tạo (AI) đã tạo ra nhiều thay đổi mang tính bước ngoặt, đặc biệt trong lĩnh vực y tế. Hệ thống y tế hiện nay thường xuyên rơi vào tình trạng quá tải tại các bệnh viện tuyến đầu, dẫn đến thời gian chờ đợi kéo dài, trong khi người dân có nhu cầu sàng lọc sức khỏe ban đầu lại thường tra cứu thông tin thiếu kiểm chứng trên internet."));
children.push(p("Một hệ thống có khả năng tiếp nhận mô tả triệu chứng bằng ngôn ngữ tự nhiên và dự đoán nhóm bệnh phù hợp sẽ giúp sàng lọc nhanh và định hướng người dùng tới chuyên khoa. Xuất phát từ thực tế đó, nhóm thực hiện module ChanDoanBenh_ML nhằm xây dựng một quy trình học máy hoàn chỉnh: từ dữ liệu triệu chứng – bệnh, qua tiền xử lý và xử lý ngôn ngữ, đến huấn luyện và đánh giá mô hình phân loại bệnh."));

children.push(h2("1.2. Mục tiêu đề tài"));
children.push(p("Module ChanDoanBenh_ML hướng tới các mục tiêu cụ thể:"));
children.push(numbered("Xây dựng quy trình tiền xử lý chuyển dữ liệu triệu chứng dạng chữ thành bảng số (one-hot có trọng số) để máy học được.", "n12"));
children.push(numbered("Cho phép người dùng nhập triệu chứng bằng câu tiếng Việt tự do và tự động nhận diện các triệu chứng (NLP).", "n12"));
children.push(numbered("Huấn luyện, so sánh và đánh giá ba thuật toán phân loại: Random Forest, K-Nearest Neighbors và Naive Bayes để chọn mô hình tốt nhất.", "n12"));

children.push(h2("1.3. Đối tượng và phạm vi nghiên cứu"));
children.push(h3("1.3.1. Đối tượng nghiên cứu"));
children.push(p("Các thuật toán phân loại trong học máy, kỹ thuật xử lý ngôn ngữ tự nhiên tiếng Việt và tập dữ liệu gồm danh sách triệu chứng cùng loại bệnh tương ứng."));
children.push(h3("1.3.2. Phạm vi nghiên cứu"));
children.push(bullet("Về bệnh lý: tập trung vào 400 loại bệnh phổ biến với 135 triệu chứng thường gặp."));
children.push(bullet("Về dữ liệu: sử dụng bộ dữ liệu triệu chứng – bệnh dạng bảng và tệp trọng số mức độ nghiêm trọng đã qua tiền xử lý."));
children.push(bullet("Về công nghệ: hệ thống mang tính hỗ trợ tham khảo, không thay thế chỉ định của bác sĩ chuyên khoa."));

children.push(new Paragraph({ children: [new PageBreak()] }));

// ===================== CHUONG 2 =====================
children.push(h1("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT"));

children.push(h2("2.1. Tổng quan về Machine Learning trong y tế"));
children.push(p("Machine Learning là một nhánh của Trí tuệ nhân tạo, cho phép máy tính học từ dữ liệu để đưa ra dự đoán mà không cần lập trình tường minh. Trong y tế, công nghệ này hỗ trợ chẩn đoán bệnh, phân tích bệnh án, xử lý hình ảnh y khoa và cá nhân hóa điều trị. Bài toán trong đề tài thuộc nhóm phân lớp (classification): dự đoán tên bệnh từ tập triệu chứng đầu vào."));

children.push(h2("2.2. Các thuật toán phân lớp sử dụng"));
children.push(h3("2.2.1. Random Forest"));
children.push(p("Random Forest là tập hợp của nhiều cây quyết định; mỗi cây được huấn luyện trên một phần dữ liệu và kết quả cuối cùng được quyết định bằng cách bỏ phiếu đa số. Thuật toán mạnh, ít phải tinh chỉnh tham số và hạn chế được hiện tượng quá khớp so với một cây đơn lẻ."));
children.push(h3("2.2.2. K-Nearest Neighbors (KNN)"));
children.push(p("KNN là thuật toán học có giám sát, phân loại một ca bệnh mới dựa trên k ca bệnh gần nhất (theo khoảng cách) trong dữ liệu huấn luyện, rồi chọn nhãn xuất hiện nhiều nhất. Ưu điểm là dễ cài đặt, trực quan; nhược điểm là chậm với dữ liệu lớn và nhạy cảm với nhiễu."));
children.push(h3("2.2.3. Naive Bayes"));
children.push(p("Naive Bayes dựa trên định lý Bayes với giả định các đặc trưng độc lập nhau. Ưu điểm là huấn luyện rất nhanh và phù hợp với dữ liệu nhiều chiều; hạn chế là giả định độc lập không phải lúc nào cũng đúng trong thực tế."));

children.push(h2("2.3. Các độ đo đánh giá mô hình"));
children.push(p("Báo cáo sử dụng các độ đo tiêu chuẩn: Accuracy (tỷ lệ dự đoán đúng), Precision (độ chính xác của các dự đoán dương tính) và Recall (khả năng phát hiện đúng các trường hợp dương tính). Ngoài ra dùng validation curve và learning curve để phát hiện hiện tượng quá khớp (overfitting) hoặc chưa khớp (underfitting)."));

children.push(new Paragraph({ children: [new PageBreak()] }));

// ===================== CHUONG 3 =====================
children.push(h1("CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG"));

children.push(h2("3.1. Thiết kế dữ liệu"));
children.push(p("Hệ thống sử dụng hai tệp dữ liệu chính trong thư mục 01_data:"));
children.push(bullet("benh_trieuchung.csv: 5.000 ca bệnh, mỗi dòng gồm tên bệnh và tối đa 8 triệu chứng (cột TrieuChung_1…8). Bộ dữ liệu bao phủ 400 loại bệnh khác nhau."));
children.push(bullet("trongso_mucdo_nghiemtrong.csv: trọng số mức độ nghiêm trọng (Severity) của 135 triệu chứng, nhận giá trị từ 1 đến 7 tùy mức độ ảnh hưởng tới sức khỏe."));
children.push(imgNote("trích benh_trieuchung.csv và trongso_mucdo_nghiemtrong.csv"));

children.push(h2("3.2. Quy trình xử lý dữ liệu (Data Pipeline)"));
children.push(p("Kỹ thuật one-hot encoding có trọng số được áp dụng để chuyển dữ liệu chữ thành bảng số. Mỗi triệu chứng trở thành một cột; với mỗi ca bệnh, nếu có triệu chứng đó thì điền đúng trọng số nghiêm trọng của nó, ngược lại điền 0. Cột Benh là nhãn cần dự đoán. Cách mã hóa này vừa cho biết triệu chứng có xuất hiện hay không, vừa phản ánh mức độ nguy hiểm của từng triệu chứng."));
children.push(p("Kết quả thu được bảng đặc trưng kích thước 5.000 × 136 (135 cột triệu chứng + 1 cột nhãn), được lưu ra tệp 01_data/processed/features.csv để dùng cho huấn luyện."));
children.push(imgNote("trích features.csv — bảng one-hot có trọng số"));

children.push(h2("3.3. Quy trình xử lý Input (NLP)"));
children.push(p("Khi người dùng nhập câu mô tả tiếng Việt tự do, hệ thống thực hiện ba bước:"));
children.push(numbered("Chuẩn hóa và tách từ: đưa về chữ thường, loại bỏ dấu câu; nếu có thư viện underthesea thì tách từ chuẩn, nếu không thì tách theo khoảng trắng.", "n33"));
children.push(numbered("Nhận diện triệu chứng: dò trực tiếp các cụm triệu chứng trong câu, ưu tiên khớp cụm dài trước (ví dụ \"sốt cao\" trước \"sốt\") và bổ sung từ điển đồng nghĩa (ví dụ \"tức ngực\" → \"đau ngực\", \"sợ ánh sáng\" → \"nhạy cảm ánh sáng\").", "n33"));
children.push(numbered("Vector hóa: tạo vector số có cùng thứ tự cột với dữ liệu huấn luyện, bật giá trị trọng số tại vị trí các triệu chứng đã nhận diện, rồi đưa thẳng vào mô hình đã huấn luyện.", "n33"));
children.push(p("Ví dụ với input \"Mấy hôm nay tôi sốt cao, đau nhức cơ và mệt mỏi, kèm theo ho và ớn lạnh\", hệ thống nhận diện đúng các triệu chứng: sốt cao, đau nhức cơ, mệt mỏi, ho, ớn lạnh.", { italics: true }));
children.push(imgNote("bảng kết quả NLP: câu mô tả → triệu chứng nhận diện"));

children.push(new Paragraph({ children: [new PageBreak()] }));

// ===================== CHUONG 4 =====================
children.push(h1("CHƯƠNG 4: CÀI ĐẶT VÀ THỰC NGHIỆM"));

children.push(h2("4.1. Môi trường cài đặt"));
children.push(p("Hệ thống được xây dựng bằng Python 3.11 với hệ sinh thái khoa học dữ liệu. Các công cụ chính:"));
children.push(bullet("Pandas, NumPy: cấu trúc hóa dữ liệu và xử lý ma trận triệu chứng."));
children.push(bullet("Scikit-learn: triển khai Random Forest, KNN, Naive Bayes, chia tập dữ liệu và vẽ validation/learning curve."));
children.push(bullet("underthesea (tùy chọn): tách từ tiếng Việt cho phần xử lý input NLP."));
children.push(bullet("Jupyter Notebook: môi trường huấn luyện và trình bày từng bước xử lý."));

children.push(h2("4.2. Huấn luyện mô hình"));
children.push(p("Dữ liệu sau tiền xử lý (features.csv) được chia theo tỷ lệ 80% huấn luyện (4.000 mẫu) và 20% kiểm tra (1.000 mẫu) với stratify theo nhãn để giữ phân bố bệnh. Nhãn bệnh dạng chữ được mã hóa thành số bằng LabelEncoder. Ba mô hình được huấn luyện với cấu hình mặc định hợp lý: Random Forest (100 cây), KNN (k = 5), Naive Bayes (GaussianNB)."));
children.push(p("Với mỗi mô hình, nhóm vẽ thêm validation curve (theo n_estimators của Random Forest và theo k của KNN) và learning curve để khảo sát ảnh hưởng của tham số và của số lượng mẫu huấn luyện. Mô hình sau khi huấn luyện được lưu ra tệp .pkl kèm bộ mã hóa nhãn để tái sử dụng cho dự đoán."));

children.push(h2("4.3. Đánh giá kết quả"));
children.push(p("Kết quả đánh giá trên tập kiểm tra (1.000 mẫu, 400 lớp bệnh) được tổng hợp trong bảng sau:"));
// Bang ket qua
children.push(new (require("docx").Table)({
  width: { size: 100, type: require("docx").WidthType.PERCENTAGE },
  rows: [
    tableRow(["Mô hình", "Accuracy", "Precision", "Recall"], true),
    tableRow(["Random Forest", "0,318", "0,302", "0,299"]),
    tableRow(["Naive Bayes", "0,316", "0,238", "0,299"]),
    tableRow(["KNN (k=5)", "0,278", "0,253", "0,259"]),
  ],
}));
children.push(p("Nhận xét:", { bold: true, after: 60 }));
children.push(bullet("Random Forest cho kết quả tốt nhất (Accuracy ≈ 0,318), nhỉnh hơn Naive Bayes (0,316) và vượt rõ KNN (0,278)."));
children.push(bullet("Mức chính xác này tuy chưa cao nhưng cần đặt trong bối cảnh bài toán có tới 400 lớp bệnh: nếu đoán ngẫu nhiên xác suất đúng chỉ là 1/400 ≈ 0,25%, nên mô hình đã tốt hơn khoảng 125 lần so với ngẫu nhiên."));
children.push(bullet("Validation curve của Random Forest cho thấy độ chính xác tăng và ổn định khi số cây đạt khoảng 150–200; KNN đạt tốt nhất ở k nhỏ. Khoảng cách giữa đường Train và đường kiểm tra (CV) phản ánh mô hình vẫn còn dư địa cải thiện khi tăng dữ liệu, thể hiện rõ trên learning curve."));
children.push(bullet("Nguyên nhân chính khiến độ chính xác bị giới hạn là dữ liệu khá thưa (mỗi ca chỉ có vài triệu chứng trên tổng 135 triệu chứng) và nhiều bệnh chia sẻ chung triệu chứng phổ biến như sốt, mệt mỏi, buồn nôn."));
children.push(imgNote("biểu đồ so sánh Accuracy 3 mô hình"));
children.push(imgNote("validation curve Random Forest / KNN và learning curve Random Forest"));

children.push(new Paragraph({ children: [new PageBreak()] }));

// ===================== KET LUAN =====================
children.push(h1("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN"));
children.push(p("Module ChanDoanBenh_ML đã xây dựng hoàn chỉnh một quy trình học máy cho bài toán chẩn đoán bệnh từ triệu chứng: tiền xử lý dữ liệu bằng one-hot encoding có trọng số, xử lý câu mô tả tiếng Việt tự do thành vector triệu chứng (NLP), và huấn luyện – so sánh ba mô hình Random Forest, KNN, Naive Bayes. Trong đó Random Forest cho kết quả tốt nhất và được chọn làm mô hình chính."));
children.push(p("Hạn chế hiện tại là độ chính xác còn khiêm tốn do số lớp bệnh lớn và dữ liệu triệu chứng thưa. Hướng phát triển tiếp theo gồm: mở rộng và làm giàu dữ liệu triệu chứng cho mỗi bệnh, bổ sung từ điển đồng nghĩa và dùng mô hình NLP mạnh hơn để nhận diện triệu chứng chính xác hơn, thử nghiệm các mô hình nâng cao (Gradient Boosting, mạng nơ-ron), và phát triển khả năng hỏi – đáp nhiều lượt thay vì dự đoán từ một câu mô tả duy nhất."));

children.push(h1("TÀI LIỆU THAM KHẢO"));
children.push(p("[1] Bộ dữ liệu triệu chứng – bệnh và trọng số mức độ nghiêm trọng (Disease – Symptoms), nguồn tham khảo từ Kaggle."));
children.push(p("[2] Tài liệu thư viện scikit-learn: https://scikit-learn.org."));

// ---- bang helpers (dat cuoi de tranh hoisting issue voi require) ----
function tableRow(cells, header) {
  const { TableRow, TableCell, WidthType } = require("docx");
  return new TableRow({
    children: cells.map((c) => new TableCell({
      shading: header ? { fill: "2E75B6" } : undefined,
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: c, font: FONT, size: SZ, bold: header, color: header ? "FFFFFF" : "000000" })],
      })],
    })),
  });
}

// ===================== DOCUMENT =====================
const doc = new Document({
  features: { updateFields: true },
  numbering: {
    config: [
      { reference: "n12", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START }] },
      { reference: "n33", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START }] },
    ],
  },
  styles: {
    default: { document: { run: { font: FONT, size: SZ } } },
  },
  sections: [{
    properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1080 } } },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("WROTE", OUT, buf.length, "bytes");
});
