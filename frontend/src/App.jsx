import Chat from "./Chat.jsx";
import "./chat.css";                 // on ré-utilise la même feuille

export default function App() {
  return (
    <div className="page">
      <header className="page-header">
        Assistant Financier • Multi-Agents
      </header>

      {/* notre colonne de chat */}
      <Chat />
    </div>
  );
}
