import React, { useState } from "react";
import { Search, CheckCircle, XCircle, Edit3, Trash2 } from "lucide-react";
import "../styles/HistoryPage.css";

function HistoryPage() {
  const [historyData, setHistoryData] = useState([
    { id: 1, disease: "Cảm cúm", date: "2024-03-20", rating: null, actualDisease: "" },
    { id: 2, disease: "Viêm họng", date: "2024-03-22", rating: "wrong", actualDisease: "Viêm Amidan" },
    { id: 3, disease: "Đau dạ dày", date: "2024-03-25", rating: "ok", actualDisease: "" },
  ]);

  const [searchTerm, setSearchTerm] = useState("");
  const [filterDate, setFilterDate] = useState("");

  // Hàm thay đổi trạng thái đánh giá (Đúng/Sai/Chưa đánh giá)
  const handleRate = (id, status) => {
    const updated = historyData.map(item => 
      item.id === id ? { ...item, rating: status, actualDisease: status === 'ok' ? "" : item.actualDisease } : item
    );
    setHistoryData(updated);
  };

  // Hàm cập nhật tên bệnh thực sự
  const handleActualChange = (id, value) => {
    const updated = historyData.map(item => 
      item.id === id ? { ...item, actualDisease: value } : item
    );
    setHistoryData(updated);
  };

  const filteredData = historyData.filter((item) => {
    return item.disease.toLowerCase().includes(searchTerm.toLowerCase()) &&
           (filterDate ? item.date === filterDate : true);
  });

  return (
    <div className="history-page">
      <h1 className="page-title">Lịch Sử Chẩn Đoán Hệ Thống</h1>

      <div className="filter-bar">
        <div className="search-box">
          <Search size={18} />
          <input 
            placeholder="Tìm theo tên bệnh..." 
            onChange={(e) => setSearchTerm(e.target.value)} 
          />
        </div>
        <input 
          type="date" 
          className="date-input" 
          onChange={(e) => setFilterDate(e.target.value)} 
        />
      </div>

      <div className="table-container">
        <table className="history-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Bệnh AI chẩn đoán</th>
              <th>Thời gian</th>
              <th>Đánh giá</th>
              <th>Cập nhật bệnh thực tế</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.map((item, index) => (
              <tr key={item.id}>
                <td>{index + 1}</td>
                <td className="disease-name">{item.disease}</td>
                <td>{item.date}</td>
                <td>
                  <div className="rating-buttons">
                    <button 
                      className={`rate-btn ok ${item.rating === 'ok' ? 'active' : ''}`}
                      onClick={() => handleRate(item.id, 'ok')}
                      title="Đúng"
                    >
                      <CheckCircle size={18} />
                    </button>
                    <button 
                      className={`rate-btn wrong ${item.rating === 'wrong' ? 'active' : ''}`}
                      onClick={() => handleRate(item.id, 'wrong')}
                      title="Sai"
                    >
                      <XCircle size={18} />
                    </button>
                  </div>
                </td>
                <td>
                  {item.rating === 'wrong' ? (
                    <div className="edit-cell">
                      <Edit3 size={14} />
                      <input 
                        type="text"
                        placeholder="Nhập bệnh thực tế..."
                        value={item.actualDisease}
                        onChange={(e) => handleActualChange(item.id, e.target.value)}
                      />
                    </div>
                  ) : (
                    <span className="text-muted">{item.rating === 'ok' ? "N/A" : "Chờ đánh giá..."}</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default HistoryPage;