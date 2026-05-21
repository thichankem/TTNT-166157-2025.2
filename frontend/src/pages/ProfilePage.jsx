import React, { useState } from "react";
import "../styles/ProfilePage.css";

function ProfilePage() {
  const [profile, setProfile] = useState({
    name: "Nguyễn Văn A",
    age: 25,
    weight: 65,
    birthPlace: "Hà Nội",
    medicalHistory: [
      { id: 1, disease: "Sốt xuất huyết", duration: "2 tuần", isCurrent: false },
      { id: 2, disease: "Viêm xoang", duration: "2 năm", isCurrent: true },
    ],
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfile({ ...profile, [name]: value });
  };

  const handleHistoryChange = (id, field, value) => {
    const updatedHistory = profile.medicalHistory.map((item) =>
      item.id === id ? { ...item, [field]: value } : item
    );
    setProfile({ ...profile, medicalHistory: updatedHistory });
  };

  const addHistory = () => {
    const newItem = { id: Date.now(), disease: "", duration: "", isCurrent: false };
    setProfile({ ...profile, medicalHistory: [...profile.medicalHistory, newItem] });
  };

  return (
    <div className="profile-container">
      <h1 className="profile-title">Hồ Sơ Y Tế Cá Nhân</h1>

      {/* PHẦN 1: THÔNG TIN CƠ BẢN */}
      <div className="profile-card">
        <h3 className="card-header">Thông tin cơ bản</h3>
        <div className="basic-info-grid">
          <div className="input-field">
            <label>Họ và tên</label>
            <input name="name" value={profile.name} onChange={handleInputChange} />
          </div>
          <div className="input-field">
            <label>Tuổi</label>
            <input type="number" name="age" value={profile.age} onChange={handleInputChange} />
          </div>
          <div className="input-field">
            <label>Cân nặng (kg)</label>
            <input type="number" name="weight" value={profile.weight} onChange={handleInputChange} />
          </div>
          <div className="input-field">
            <label>Nơi sinh</label>
            <input name="birthPlace" value={profile.birthPlace} onChange={handleInputChange} />
          </div>
        </div>
      </div>

      {/* PHẦN 2: TIỀN SỬ BỆNH LÝ - Sử dụng bảng để không bao giờ bị lệch */}
      <div className="profile-card">
        <h3 className="card-header">Tiền sử bệnh lý</h3>
        <div className="table-responsive">
          <table className="medical-table">
            <thead>
              <tr>
                <th>Tên bệnh</th>
                <th>Thời gian</th>
                <th>Tình trạng</th>
              </tr>
            </thead>
            <tbody>
              {profile.medicalHistory.map((item) => (
                <tr key={item.id}>
                  <td>
                    <input
                      className="table-input"
                      value={item.disease}
                      onChange={(e) => handleHistoryChange(item.id, "disease", e.target.value)}
                      placeholder="Nhập tên bệnh..."
                    />
                  </td>
 <td>
  <input
    type="date" /* Đổi từ text sang date */
    className="table-input"
    value={item.duration}
    onChange={(e) => handleHistoryChange(item.id, "duration", e.target.value)}
  />
</td>
                  <td>
                    <select
                      className="table-select"
                      value={item.isCurrent}
                      onChange={(e) => handleHistoryChange(item.id, "isCurrent", e.target.value === "true")}
                    >
                      <option value="false">Đã khỏi</option>
                      <option value="true">Còn bị</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <button className="add-history-btn" onClick={addHistory}>
          + Thêm dòng mới
        </button>
      </div>

      <div className="action-bar">
        <button className="save-btn" onClick={() => alert("Đã lưu!")}>
          Lưu hồ sơ
        </button>
      </div>
    </div>
  );
}

export default ProfilePage;