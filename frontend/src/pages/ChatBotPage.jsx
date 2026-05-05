import React, { useState, useEffect, useRef } from "react";
import { Send, Bot, User } from "lucide-react";
import { sendChatMessage } from "../services/chatService";
import "../styles/ChatBotPage.css";

function ChatBotPage() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Xin chào! Tôi là trợ lý AI y tế. Bạn đang gặp vấn đề gì về sức khỏe?" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false); // 2. Thêm trạng thái loading
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 3. Hàm gửi tin nhắn gọi API
  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;
    
    const userMessage = { from: "user", text: input };
    
    // Hiển thị tin nhắn của người dùng trước
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Gọi service API trong frontend/service
      const response = await sendChatMessage(input);
      const botResponse = { from: "bot", text: response.reply };
      setMessages((prev) => [...prev, botResponse]);
    } catch (error) {
      console.error("Lỗi kết nối API:", error);
      const errorMessage = { 
        from: "bot", 
        text: "Rất tiếc, tôi không thể kết nối với hệ thống lúc này. Vui lòng thử lại sau." 
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <Bot size={24} color="#10a37f" />
        <h2>Trợ lý AI Y Tế</h2>
      </div>

      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message-row ${msg.from}`}>
            <div className="avatar">
              {msg.from === "user" ? <User size={16} /> : <Bot size={16} />}
            </div>
            <div className="message-bubble">
              <p>{msg.text}</p>
            </div>
          </div>
        ))}
        {/* Hiển thị trạng thái đang xử lý */}
        {isLoading && (
          <div className="message-row bot">
            <div className="avatar"><Bot size={16} /></div>
            <div className="message-bubble">
              <p className="typing-dots">Đang phân tích...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="input-wrapper">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Mô tả triệu chứng của bạn tại đây..."
            disabled={isLoading} // Khóa input khi đang chờ API
          />
          <button 
            className="send-btn" 
            onClick={sendMessage} 
            disabled={isLoading || !input.trim()}
          >
            <Send size={20} />
          </button>
        </div>
        <p className="disclaimer">AI có thể đưa ra câu trả lời sai. Hãy tham khảo ý kiến bác sĩ.</p>
      </div>
    </div>
  );
}

export default ChatBotPage;