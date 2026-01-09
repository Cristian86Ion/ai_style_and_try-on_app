import { useState, useRef, useEffect } from "react"
import { PaperAirplaneIcon } from "@heroicons/react/24/solid"
import { BookOpen } from "lucide-react"

interface Message {
  from: "user" | "llm"
  text?: string
  image?: string
  tips?: string
  alternativePalette?: string
  measurements?: {
    chest_circumference: number
    waist_circumference: number
    hip_circumference: number
    arm_length: number
    leg_length: number
    shoulder_hip_ratio: number
    bmi: number
  }
}

interface ChatWindowProps {
  theme?: string
  fontSize?: string
  messages: Message[]
  onMessagesUpdate: (messages: Message[] | ((prev: Message[]) => Message[])) => void
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
      onMessagesUpdate(prev => [
        ...prev,
        { from: "llm", text: "⚠️ Please complete your profile first." }
      ])
      return
    }

    setLoading(true)

    const userText = input.trim()
    const newUserMessage: Message = { from: "user", text: userText }

    const currentMessages = [...messages, newUserMessage]
    onMessagesUpdate(currentMessages)
    setInput("")

    try {
      const res = await fetch("http://127.0.0.1:8000/generate-outfit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_message: userText,
          body_type: bodyType,
          user_name: userName
        })
      })

      if (!res.ok) throw new Error(`Server error ${res.status}`)

      const data = await res.json()

      // 🔑 IMPORTANT: NU afișăm descrierea outfitului
      onMessagesUpdate(prev => [
        ...prev,
        {
          from: "llm",
          image: data.image_url,
          tips: data.styling_tips,
          alternativePalette: data.alternative_palette,
          measurements: data.measurements
        }
      ])

    } catch (err) {
      console.error("API error:", err)
      onMessagesUpdate(prev => [
        ...prev,
        {
          from: "llm",
          text: "❌ Failed to generate outfit. Please try again."
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const fontSizeClass =
    fontSize === "small" ? "text-sm" :
    fontSize === "large" ? "text-lg" : "text-base"

  return (
    <div className="flex flex-col bg-black/40 backdrop-blur-2xl border border-white/10 rounded-3xl p-6 shadow-2xl h-[78vh] w-full max-w-3xl mx-auto text-white">

      {/* Messages */}
      <div className="flex-1 overflow-y-auto mb-4 pr-2 space-y-4 custom-scrollbar">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${msg.from === "user" ? "items-end" : "items-start"}`}
          >

            {/* USER TEXT ONLY */}
            {msg.from === "user" && msg.text && (
              <div className={`px-4 py-2 rounded-2xl max-w-[90%] leading-relaxed
                bg-white/10 border border-white/20 ${fontSizeClass}`}>
                <div className="whitespace-pre-wrap">{msg.text}</div>
              </div>
            )}

            {/* IMAGE */}
            {msg.image && (
              <div
                className="mt-3 rounded-xl overflow-hidden border border-white/10 cursor-pointer hover:opacity-80 transition-all w-full max-w-[320px] shadow-xl"
                onClick={() => window.open(msg.image, "_blank")}
              >
                <img src={msg.image} alt="Generated Outfit" className="w-full h-auto block" />
              </div>
            )}

            {/* STYLING TIPS */}
            {msg.tips && (
              <div className="mt-3 px-4 py-3 rounded-xl bg-purple-500/10 border border-purple-400/20 max-w-[90%]">
                <div className="text-xs font-semibold text-purple-300 mb-1 tracking-wider">
                  STYLING TIPS
                </div>
                <div className="text-sm text-gray-200 leading-relaxed">
                  {msg.tips}
                </div>
              </div>
            )}

            {/* ALTERNATIVE COLORS */}
            {msg.alternativePalette && (
              <div className="mt-2 px-4 py-3 rounded-xl bg-blue-500/10 border border-blue-400/20 max-w-[90%]">
                <div className="text-xs font-semibold text-blue-300 mb-1 tracking-wider">
                  ALTERNATIVE COLORS
                </div>
                <div className="text-sm text-gray-200">
                  {msg.alternativePalette}
                </div>
              </div>
            )}

            {/* MEASUREMENTS */}
            {msg.measurements && (
              <div className="mt-2 px-4 py-3 rounded-xl bg-green-500/10 border border-green-400/20 max-w-[90%] w-full">
                <div className="text-xs font-semibold text-green-300 mb-2 tracking-wider">
                  BODY DIMENSIONS
                </div>
                <div className="text-[11px] text-gray-300 grid grid-cols-2 gap-x-4 gap-y-1 font-mono uppercase">
                  <span>Chest: {msg.measurements.chest_circumference}cm</span>
                  <span>Waist: {msg.measurements.waist_circumference}cm</span>
                  <span>Hips: {msg.measurements.hip_circumference}cm</span>
                  <span>Arm: {msg.measurements.arm_length}cm</span>
                  <span>Leg: {msg.measurements.leg_length}cm</span>
                  <span>Ratio: {msg.measurements.shoulder_hip_ratio}</span>
                  <span className="col-span-2 text-green-200/50 mt-1 border-t border-green-400/10 pt-1">
                    BMI: {msg.measurements.bmi}
                  </span>
                </div>
              </div>
            )}
          </div>
        ))}

        {/* LOADING */}
        {loading && (
          <div className="flex items-start">
            <div className="px-4 py-3 rounded-2xl bg-white/5 border border-white/5 text-gray-400 flex items-center gap-2">
              <div className="animate-spin h-4 w-4 border-2 border-purple-400 border-t-transparent rounded-full" />
              Tailoring your look...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* INPUT */}
      <div className="flex gap-2 items-center bg-white/5 p-2 rounded-xl border border-white/10 focus-within:border-white/20 transition-all">
        <textarea
          className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-2 px-3 resize-none outline-none placeholder:text-gray-500"
          rows={1}
          placeholder="male, 178, 80, 26, 43, zara massimo-dutti, style: elegant..."
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

      <div className="mt-2 flex items-center justify-between text-xs text-gray-500 px-1">
        <span>Format: sex, height, weight, age, shoe, brands, style</span>
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
