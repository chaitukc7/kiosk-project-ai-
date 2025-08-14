// =============================================================================
// SALES ASSISTANT CHATBOT COMPONENT
// =============================================================================
// This React component provides a chatbot interface for the kiosk app.
// Features:
// - Natural language queries about sales data
// - PDF report generation and download
// - Real-time communication with backend services
// - User-friendly interface with quick action buttons
// =============================================================================

import { useState } from "react";
import { MessageSquare, BarChart3, TrendingUp, TrendingDown, Calendar, Clock, X } from "lucide-react";

// =============================================================================
// QUICK ACTION OPTIONS
// =============================================================================
// Predefined buttons for common queries and report generation
// Each option has a label, icon, value (query text), and optional type
const quickOptions = [
  // Query Options - These send natural language questions to the backend
  { 
    label: "Best Selling Item", 
    icon: <TrendingUp className="w-4 h-4 mr-1" />, 
    value: "What's the best selling item?" 
  },
  { 
    label: "Least Selling Item", 
    icon: <TrendingDown className="w-4 h-4 mr-1" />, 
    value: "What's the least selling item?" 
  },
  // PDF Report Options - These generate downloadable PDF reports
  { 
    label: "Last Month's Sales", 
    icon: <Calendar className="w-4 h-4 mr-1" />, 
    value: "generate_monthly_report", 
    type: "pdf" 
  },
  { 
    label: "Last Week's Sales", 
    icon: <BarChart3 className="w-4 h-4 mr-1" />, 
    value: "generate_weekly_report", 
    type: "pdf" 
  },
  { 
    label: "Today's Sales", 
    icon: <Clock className="w-4 h-4 mr-1" />, 
    value: "generate_daily_report", 
    type: "pdf" 
  }
];

// =============================================================================
// MAIN CHATBOT COMPONENT
// =============================================================================

export default function NovaAIChatbot() {
  // =============================================================================
  // STATE MANAGEMENT
  // =============================================================================
  
  // Controls whether the chatbot is open or closed
  const [open, setOpen] = useState(false);
  
  // Stores all chat messages (both user and bot messages)
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! I'm your sales assistant. How can I help you with your sales & inventory today?" }
  ]);
  
  // Current input text in the chat input field
  const [input, setInput] = useState("");
  
  // Loading state to show when processing requests
  const [isLoading, setIsLoading] = useState(false);

  // =============================================================================
  // MESSAGE HANDLING FUNCTION
  // =============================================================================
  // This function processes all user interactions (text input and button clicks)
  
  const handleSend = async (text) => {
    // Don't process empty messages
    if (!text.trim()) return;
    
    // Add user message to chat
    setMessages(prev => [...prev, { from: "user", text }]);
    setInput(""); // Clear input field
    setIsLoading(true); // Show loading state

    try {
      // =============================================================================
      // PDF REPORT GENERATION
      // =============================================================================
      // Check if this is a PDF generation request
      const pdfOption = quickOptions.find(option => option.value === text && option.type === "pdf");
      
      if (pdfOption) {
        // Show loading message for PDF generation
        setMessages(prev => [...prev, { from: "bot", text: "📊 Generating your report..." }]);

        // Map the option value to the correct endpoint URL
        // Frontend uses underscores, backend uses hyphens
        const endpointMap = {
          "generate_daily_report": "generate-daily-report",
          "generate_weekly_report": "generate-weekly-report", 
          "generate_monthly_report": "generate-monthly-report"
        };
        
        const endpoint = endpointMap[text] || text;

        // Make API call to backend PDF generation endpoint
        const response = await fetch(`/api/llm/${endpoint}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          // Create a blob from the PDF response
          const blob = await response.blob();
          
          // Create download link and trigger download
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = response.headers.get('content-disposition')?.split('filename=')[1] || `${text}.pdf`;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);

          // Remove loading message and add success message
          setMessages(prev => {
            const newMessages = prev.slice(0, -1); // Remove loading message
            return [...newMessages, { from: "bot", text: "✅ Your report has been generated and downloaded!" }];
          });
        } else {
          // Handle PDF generation error
          setMessages(prev => {
            const newMessages = prev.slice(0, -1); // Remove loading message
            return [...newMessages, { from: "bot", text: "Sorry, I couldn't generate the report. Please try again." }];
          });
        }
      } else {
        // =============================================================================
        // QUERY PROCESSING
        // =============================================================================
        // Regular query - send natural language question to backend
        
        // Show loading message
        setMessages(prev => [...prev, { from: "bot", text: "🤔 Let me check that for you..." }]);

        // Send question to backend endpoint
        const response = await fetch("/api/llm/ai-query", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ question: text }),
        });

        const data = await response.json();

        if (data.success) {
          // Remove loading message and add response
          setMessages(prev => {
            const newMessages = prev.slice(0, -1); // Remove loading message
            return [...newMessages, { from: "bot", text: data.response }];
          });
        } else {
          // Handle query error
          setMessages(prev => {
            const newMessages = prev.slice(0, -1); // Remove loading message
            return [...newMessages, { from: "bot", text: `Sorry, I encountered an error: ${data.error}` }];
          });
        }
      }
    } catch (error) {
      // =============================================================================
      // ERROR HANDLING
      // =============================================================================
      // Handle network errors, connection issues, etc.
      console.error("Error calling service:", error);
      setMessages(prev => {
        const newMessages = prev.slice(0, -1); // Remove loading message
        return [...newMessages, { from: "bot", text: "Sorry, I'm having trouble connecting to my services. Please make sure the backend is running." }];
      });
    } finally {
      // Always clear loading state
      setIsLoading(false);
    }
  };

  // =============================================================================
  // RENDER COMPONENT
  // =============================================================================

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!open ? (
        // =============================================================================
        // CLOSED STATE - SHOW CHAT BUTTON
        // =============================================================================
        <button
          onClick={() => setOpen(true)}
          className="flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-full shadow-lg hover:bg-orange-600 transition-all"
        >
          <MessageSquare className="w-5 h-5" />
          Sales Assistant
        </button>
      ) : (
        // =============================================================================
        // OPEN STATE - SHOW CHAT INTERFACE
        // =============================================================================
        <div className="w-80 bg-slate-900 rounded-2xl shadow-2xl border border-slate-800 flex flex-col overflow-hidden">
          
          {/* =============================================================================
              HEADER SECTION
              ============================================================================= */}
          <div className="flex items-center gap-3 p-4 bg-gradient-to-b from-slate-900 to-slate-800 border-b border-slate-800">
            {/* Assistant Avatar */}
            <div className="w-10 h-10 rounded-full bg-orange-500 flex items-center justify-center text-white text-lg font-bold shadow">
              <span>💬</span>
            </div>
            
            {/* Chatbot Info */}
            <div>
              <div className="font-bold text-orange-400 text-lg">Sales Assistant</div>
              <div className="text-xs text-slate-400">Your Business Helper</div>
            </div>
            
            {/* Close Button */}
            <button className="ml-auto text-slate-400 hover:text-orange-400" onClick={() => setOpen(false)}>
              <X className="w-5 h-5" />
            </button>
          </div>
          
          {/* =============================================================================
              MESSAGES SECTION
              ============================================================================= */}
          <div className="flex-1 p-4 space-y-2 overflow-y-auto bg-slate-900 max-h-96">
            {/* Render all chat messages */}
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={
                  msg.from === "bot"
                    ? "flex items-start gap-2" // Bot messages aligned left
                    : "flex items-end justify-end" // User messages aligned right
                }
              >
                {/* Assistant avatar (only for assistant messages) */}
                {msg.from === "bot" && (
                  <div className="w-8 h-8 rounded-full bg-orange-500 flex items-center justify-center text-white">💬</div>
                )}
                
                {/* Message bubble */}
                <div
                  className={
                    "px-4 py-2 rounded-xl max-w-[80%] " +
                    (msg.from === "bot"
                      ? "bg-slate-800 text-white" // Bot message styling
                      : "bg-orange-500 text-white") // User message styling
                  }
                >
                  {msg.text}
                </div>
              </div>
            ))}
            
            {/* =============================================================================
                LOADING ANIMATION
                ============================================================================= */}
            {isLoading && (
              <div className="flex items-start gap-2">
                <div className="w-8 h-8 rounded-full bg-orange-500 flex items-center justify-center text-white">💬</div>
                <div className="px-4 py-2 rounded-xl bg-slate-800 text-white">
                  {/* Animated bouncing dots */}
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* =============================================================================
              QUICK ACTION BUTTONS
              ============================================================================= */}
          <div className="flex flex-wrap gap-2 px-4 pb-2">
            {quickOptions.map((option) => (
              <button
                key={option.label}
                className="flex items-center px-3 py-1.5 text-xs font-medium rounded-full border border-orange-400 text-orange-400 bg-slate-800 hover:bg-orange-500 hover:text-white transition"
                onClick={() => handleSend(option.value)}
                disabled={isLoading} // Disable buttons during processing
              >
                {option.icon}
                {option.label}
              </button>
            ))}
          </div>
          
          {/* =============================================================================
              INPUT SECTION
              ============================================================================= */}
          <form
            className="flex items-center border-t border-slate-800 p-3 bg-slate-800"
            onSubmit={e => {
              e.preventDefault(); // Prevent form submission
              handleSend(input); // Send the input text
            }}
          >
            {/* Text input field */}
            <input
              className="flex-1 bg-transparent outline-none text-white placeholder-slate-400 px-2"
              placeholder="Type your question..."
              value={input}
              onChange={e => setInput(e.target.value)}
              disabled={isLoading} // Disable input during processing
              autoFocus // Focus input when chat opens
            />
            
            {/* Send button */}
            <button 
              type="submit" 
              className="ml-2 text-orange-400 hover:text-orange-500 disabled:opacity-50"
              disabled={isLoading} // Disable button during processing
            >
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
