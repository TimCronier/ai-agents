import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./Chat.css";               //  ⬅︎ ajoute la feuille CSS

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const bottomRef = useRef(null);

  /* Scroll auto vers le dernier message */
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function send(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;

    setInput("");
    setMessages((m) => [...m, { from: "user", text }]);

    try {
      const r = await fetch("/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await r.json();
      setMessages((m) => [...m, { from: "bot", text: data.answer }]);
    } catch (err) {
      setMessages((m) => [...m, { from: "bot", text: `⚠️ ${err.message}` }]);
    }
  }

  return (
    <div className="chat-wrapper">
      {/* -------- zone messages -------- */}
      <div className="chat-box">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`message-row ${m.from === "user" ? "user" : "bot"}`}
          >
            <div
              className={`message-bubble ${
                m.from === "user" ? "user" : "bot"
              }`}
            >
              <ReactMarkdown>{m.text}</ReactMarkdown>
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* -------- formulaire -------- */}
      <form className="chat-form" onSubmit={send}>
        <input
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Pose ta question…"
        />
        <button
          className="chat-button"
          disabled={!input.trim()}
          type="submit"
        >
          Envoyer
        </button>
      </form>
    </div>
  );
}
