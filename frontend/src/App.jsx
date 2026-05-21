import { HashRouter as Router, Routes, Route, Link } from "react-router-dom";
import ChatBotPage from "./pages/ChatBotPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import HistoryPage from "./pages/HistoryPage.jsx"; // Tên trang
import "./App.css";
import { MessageSquare, User, History } from 'lucide-react'; // History ở đây là ICON

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* SIDEBAR - Thanh điều hướng bên trái */}
        <aside className="sidebar">
          <div className="sidebar-header">
            <h2>AI Medical</h2>
          </div>
          <nav>
            <ul className="sidebar-nav">
              <li>
                <Link to="/" className="nav-item">
                  <MessageSquare size={20} />
                  <span>Đoạn chat mới</span>
                </Link>
              </li>
              <li>
                <Link to="/extra" className="nav-item">
                  <History size={20} /> {/* Dùng ICON History ở đây, không dùng HistoryPage */}
                  <span>Lịch sử chat</span>
                </Link>
              </li>
              <li>
                <Link to="/profile" className="nav-item">
                  <User size={20} />
                  <span>Trang cá nhân</span>
                </Link>
              </li>
            </ul>
          </nav>
        </aside>

        {/* NỘI DUNG CHÍNH - Hiển thị bên phải */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<ChatBotPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/extra" element={<HistoryPage />} /> {/* Dùng TRANG HistoryPage ở đây */}
            <Route path="*" element={<ChatBotPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;