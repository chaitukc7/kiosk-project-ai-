import { useState } from "react";
import { MessageSquare, BarChart3, TrendingUp, TrendingDown, Calendar, Clock, X } from "lucide-react";

const quickOptions = [
  { label: "Best Selling Item", icon: <TrendingUp className="w-4 h-4 mr-1" />, value: "What's the best selling item?" },
  { label: "Least Selling Item", icon: <TrendingDown className="w-4 h-4 mr-1" />, value: "What's the least selling item?" },
  { label: "Last Month's Sales", icon: <Calendar className="w-4 h-4 mr-1" />, value: "Show me last month's sales report." },
  { label: "Last Week's Sales", icon: <BarChart3 className="w-4 h-4 mr-1" />, value: "Show me last week's sales report." },
  { label: "Today's Sales", icon: <Clock className="w-4 h-4 mr-1" />, value: "Show me today's sales report." }
];

export default function NovaAIChatbot() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! I’m nova.ai. How can I help you with your sales & inventory today?" }
  ]);
  const [input, setInput] = useState("");

  const handleSend = (text) => {
    if (!text.trim()) return;
    setMessages([...messages, { from: "user", text }]);
    setInput("");
    // TODO: Integrate with your backend AI service here.
    setTimeout(() => {
      setMessages((msgs) => [
        ...msgs,
        { from: "bot", text: "I'm fetching that info for you..." }
      ]);
    }, 600);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!open ? (
        <button
          onClick={() => setOpen(true)}
          className="flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-full shadow-lg hover:bg-orange-600 transition-all"
        >
          <MessageSquare className="w-5 h-5" />
          Chat with nova.ai
        </button>
      ) : (
        <div className="w-80 bg-slate-900 rounded-2xl shadow-2xl border border-slate-800 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="flex items-center gap-3 p-4 bg-gradient-to-b from-slate-900 to-slate-800 border-b border-slate-800">
            <div className="w-10 h-10 rounded-full bg-orange-500 flex items-center justify-center text-white text-lg font-bold shadow">
              {/* Placeholder Avatar, replace with image if you want */}
              <span>🤖</span>
            </div>
            <div>
              <div className="font-bold text-orange-400 text-lg">nova.ai</div>
              <div className="text-xs text-slate-400">AI Sales Assistant</div>
            </div>
            <button className="ml-auto text-slate-400 hover:text-orange-400" onClick={() => setOpen(false)}>
              <X className="w-5 h-5" />
            </button>
          </div>
          {/* Messages */}
          <div className="flex-1 p-4 space-y-2 overflow-y-auto bg-slate-900">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={
                  msg.from === "bot"
                    ? "flex items-start gap-2"
                    : "flex items-end justify-end"
                }
              >
                {msg.from === "bot" && (
                  <div className="w-8 h-8 rounded-full bg-orange-500 flex items-center justify-center text-white">🤖</div>
                )}
                <div
                  className={
                    "px-4 py-2 rounded-xl " +
                    (msg.from === "bot"
                      ? "bg-slate-800 text-white"
                      : "bg-orange-500 text-white")
                  }
                >
                  {msg.text}
                </div>
              </div>
            ))}
          </div>
          {/* Quick Options */}
          <div className="flex flex-wrap gap-2 px-4 pb-2">
            {quickOptions.map((option) => (
              <button
                key={option.label}
                className="flex items-center px-3 py-1.5 text-xs font-medium rounded-full border border-orange-400 text-orange-400 bg-slate-800 hover:bg-orange-500 hover:text-white transition"
                onClick={() => handleSend(option.value)}
              >
                {option.icon}
                {option.label}
              </button>
            ))}
          </div>
          {/* Input */}
          <form
            className="flex items-center border-t border-slate-800 p-3 bg-slate-800"
            onSubmit={e => {
              e.preventDefault();
              handleSend(input);
            }}
          >
            <input
              className="flex-1 bg-transparent outline-none text-white placeholder-slate-400 px-2"
              placeholder="Type your question..."
              value={input}
              onChange={e => setInput(e.target.value)}
              autoFocus
            />
            <button type="submit" className="ml-2 text-orange-400 hover:text-orange-500">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 20l16-8-16-8v16z" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
