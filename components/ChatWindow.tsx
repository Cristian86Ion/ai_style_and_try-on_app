import { useState, useRef, useEffect } from "react"
import { PaperAirplaneIcon } from "@heroicons/react/24/solid"
import { BookOpen } from "lucide-react"

interface Message {
  from: "user" | "llm"
  text: string
  image?: string
  tips?: string
  alternativePalette?: string
}

interface ChatWindowProps {
  theme?: string
  fontSize?: string
  messages: Message[]
  onMessagesUpdate: (messages: Message[]) => void
  bodyType: string
  userName: string
  onOpenGuide?: () => void
}

export default function ChatWindow({
  theme = "dark",
  fontSize = "medium",
  messages,
  onMessagesUpdate,
  bodyType,
  userName,
  onOpenGuide
}: ChatWindowProps) {
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    if (!bodyType || !userName) {
      onMessagesUpdate([...messages, {
        from: "llm",
        text: "⚠️ Please complete your profile first (name and body type)."
      }])
      return
    }

    setLoading(true)
    const userText = input.trim()
    const newUserMessage: Message = { from: "user", text: userText }
    const updatedMessages = [...messages, newUserMessage]

    onMessagesUpdate(updatedMessages)
    setInput("")

    try {
      console.log("🔄 Sending request to backend...")

      const res = await fetch("http://127.0.0.1:8000/generate-outfit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_message: userText,
          body_type: bodyType,
          user_name: userName
        }),
      })

      console.log("📥 Response status:", res.status)

      if (!res.ok) {
        let errorMessage = `Server error (${res.status})`
        try {
          const errorData = await res.json()
          errorMessage = errorData?.detail?.message || errorData?.detail || errorMessage
        } catch {
          errorMessage = await res.text() || errorMessage
        }
        throw new Error(errorMessage)
      }

      const data = await res.json()
      console.log("✅ Response received:", data)

      onMessagesUpdate([...updatedMessages, {
        from: "llm",
        text: data.outfit_description || "No outfit description available.",
        image: data.image_url || undefined,
        tips: data.styling_tips || undefined,
        alternativePalette: data.alternative_palette || undefined
      }])

    } catch (err) {
      console.error("❌ API Error:", err)

      let errorMessage = "Failed to generate outfit."

      if (err instanceof TypeError && err.message.includes("fetch")) {
        errorMessage = `❌ Cannot connect to backend server.

🔧 Troubleshooting:
1. Is the backend running? Start it with:
   cd backend && python main.py

2. Check it's running at: http://127.0.0.1:8000
   
3. Make sure your .env file has:
   OPENAI_API_KEY=your_key_here
   TOGETHER_API_KEY=your_key_here (optional)

4. Check for CORS errors in browser console.`
      } else if (err instanceof Error) {
        errorMessage = `❌ Error: ${err.message}`
      }

      onMessagesUpdate([...updatedMessages, {
        from: "llm",
        text: errorMessage
      }])
    } finally {
      setLoading(false)
    }
  }

  const fontSizeClass =
    fontSize === "small" ? "text-sm" :
    fontSize === "large" ? "text-lg" : "text-base"

  return (
    <div className="flex flex-col bg-black/40 backdrop-blur-2xl border border-white/10 rounded-3xl p-6 shadow-2xl h-[78vh] w-full max-w-3xl mx-auto text-white">

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto mb-4 pr-2 space-y-4 custom-scrollbar">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${msg.from === "user" ? "items-end" : "items-start"}`}
          >
            {/* Message Text */}
            <div className={`px-4 py-2 rounded-2xl max-w-[90%] leading-relaxed ${
              msg.from === "user" 
                ? "bg-white/10 border border-white/20" 
                : "bg-white/5 border border-white/5 text-gray-300"
            } ${fontSizeClass}`}>
              <div className="whitespace-pre-wrap">{msg.text}</div>
            </div>

            {/* Generated Image */}
            {msg.image && (
              <div
                className="mt-3 rounded-xl overflow-hidden border border-white/10 cursor-pointer hover:opacity-80 transition-all w-full max-w-[320px] shadow-xl"
                onClick={() => window.open(msg.image, "_blank")}
                title="Click to view full size"
              >
                <img
                  src={msg.image}
                  alt="Generated Outfit"
                  className="w-full h-auto block"
                />
              </div>
            )}

            {/* Styling Tips */}
            {msg.tips && (
              <div className="mt-3 px-4 py-3 rounded-xl bg-purple-500/10 border border-purple-400/20 max-w-[90%]">
                <div className="text-xs font-semibold text-purple-300 mb-1">STYLING TIPS</div>
                <div className="text-sm text-gray-200 leading-relaxed">{msg.tips}</div>
              </div>
            )}

            {/* Alternative Color Palette */}
            {msg.alternativePalette && (
              <div className="mt-2 px-4 py-3 rounded-xl bg-blue-500/10 border border-blue-400/20 max-w-[90%]">
                <div className="text-xs font-semibold text-blue-300 mb-1">ALTERNATIVE COLORS</div>
                <div className="text-sm text-gray-200">{msg.alternativePalette}</div>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-start">
            <div className="px-4 py-3 rounded-2xl bg-white/5 border border-white/5 text-gray-400">
              <div className="flex items-center gap-2">
                <div className="animate-spin h-4 w-4 border-2 border-purple-400 border-t-transparent rounded-full"></div>
                <span>Generating your outfit...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="flex gap-2 items-center bg-white/5 p-2 rounded-xl border border-white/10 focus-within:border-white/20 transition-all">
        <textarea
          className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-2 px-3 resize-none outline-none placeholder:text-gray-500"
          rows={1}
          placeholder={loading ? "Generating outfit..." : "e.g., male, 180, 70, 30, 43, nike, style: casual with loose pants"}
          value={input}
          disabled={loading}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault()
              handleSend()
            }
          }}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="p-2 bg-white text-black rounded-lg active:scale-95 transition-all disabled:opacity-20 shadow-md hover:bg-gray-100"
        >
          <PaperAirplaneIcon className="w-4 h-4 -rotate-45" />
        </button>
      </div>

      {/* Help Text with Book Icon Guide Link */}
      <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
        <span>Format: sex, height, weight, age, shoe, brands, style: description</span>
        {onOpenGuide && (
          <button
            onClick={onOpenGuide}
            className="flex items-center gap-1 hover:text-gray-300 transition-colors"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>Style Guide</span>
          </button>
        )}
      </div>
    </div>
  )
}