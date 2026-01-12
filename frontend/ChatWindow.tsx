import { useState, useRef, useEffect } from "react"
import { PaperAirplaneIcon } from "@heroicons/react/24/solid"
import { BookOpen, ExternalLink, ShoppingBag } from "lucide-react"

interface OutfitItem {
  id: string
  brand: string
  category: string
  colors: string[]
  price_eur: string
  url: string
  style: string
}

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
  outfit?: {
    top?: OutfitItem
    pants?: OutfitItem
    layer?: OutfitItem
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

// Card pentru piese de îmbrăcăminte
function OutfitItemCard({
  item,
  label,
  icon
}: {
  item: OutfitItem
  label: string
  icon: string
}) {
  const handleClick = () => {
    if (item.url && item.url !== 'N/A') {
      window.open(item.url.startsWith('http') ? item.url : `https://${item.url}`, '_blank')
    }
  }

  return (
    <div
      className="flex items-center justify-between p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-all cursor-pointer group"
      onClick={handleClick}
    >
      <div className="flex items-center gap-2">
        <span className="text-lg">{icon}</span>
        <div>
          <div className="text-xs text-gray-400 uppercase tracking-wider">{label}</div>
          <div className="text-sm text-white font-medium">
            {item.brand?.charAt(0).toUpperCase() + item.brand?.slice(1)} {item.category}
          </div>
          <div className="text-xs text-gray-500">
            {item.colors?.join(', ')}
          </div>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm text-green-400 font-medium">€{item.price_eur}</span>
        {item.url && item.url !== 'N/A' && (
          <ExternalLink className="w-4 h-4 text-gray-500 group-hover:text-white transition-colors" />
        )}
      </div>
    </div>
  )
}

// Afișarea selecției de haine
function OutfitDisplay({ outfit }: { outfit?: Message['outfit'] }) {
  if (!outfit) return null

  const items = [
    { key: 'top', item: outfit.top, label: 'Top', icon: '' },
    { key: 'pants', item: outfit.pants, label: 'Pants', icon: '' },
    { key: 'layer', item: outfit.layer, label: 'Layer', icon: '' },
  ].filter(({ item }) => item && item.id)

  const totalPrice = items.reduce((sum, { item }) => {
    const price = parseFloat(item?.price_eur || '0')
    return sum + (isNaN(price) ? 0 : price)
  }, 0)

  if (items.length === 0) return null

  return (
    <div className="mt-3 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-indigo-400/20 overflow-hidden max-w-[90%]">
      <div className="px-4 py-2 bg-indigo-500/10 border-b border-indigo-400/10 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShoppingBag className="w-4 h-4 text-indigo-300" />
          <span className="text-xs font-semibold text-indigo-300 uppercase tracking-wider">
            Selection
          </span>
        </div>
        {totalPrice > 0 && (
          <span className="text-sm font-bold text-green-400">
            Total: €{totalPrice.toFixed(0)}
          </span>
        )}
      </div>

      <div className="p-3 space-y-2">
        {items.map(({ key, item, label, icon }) => (
          <OutfitItemCard key={key} item={item!} label={label} icon={icon} />
        ))}
      </div>

      <div className="px-4 py-2 bg-black/20 text-xs text-gray-500 text-center">
        <span>Click items to view details</span>
      </div>
    </div>
  )
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
    onMessagesUpdate(prev => [...prev, { from: "user", text: userText }])
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

      onMessagesUpdate(prev => [
        ...prev,
        {
          from: "llm",
          image: data.image_url,
          tips: data.styling_tips,
          alternativePalette: data.alternative_palette,
          measurements: data.measurements,
          outfit: data.selected_items
        }
      ])

    } catch (err) {
      console.error("API error:", err)
      onMessagesUpdate(prev => [
        ...prev,
        { from: "llm", text: "❌ Connection error. Please try again." }
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

      <div className="flex-1 overflow-y-auto mb-4 pr-2 space-y-4 custom-scrollbar">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${msg.from === "user" ? "items-end" : "items-start"}`}
          >
            {/* User Message */}
            {msg.from === "user" && msg.text && (
              <div className={`px-4 py-2 rounded-2xl max-w-[90%] bg-white/10 border border-white/20 ${fontSizeClass}`}>
                <div className="whitespace-pre-wrap">{msg.text}</div>
              </div>
            )}

            {/* Error/Text Message */}
            {msg.from === "llm" && msg.text && !msg.image && (
              <div className={`px-4 py-2 rounded-2xl max-w-[90%] bg-white/5 border border-white/10 ${fontSizeClass}`}>
                <div className="whitespace-pre-wrap">{msg.text}</div>
              </div>
            )}

            {/* Image Result */}
            {msg.image && (
              <div
                className="mt-3 rounded-xl overflow-hidden border border-white/10 w-full max-w-[320px] shadow-xl"
              >
                <img src={msg.image} alt="Outfit Preview" className="w-full h-auto block" />
              </div>
            )}

            {/* Selection (Items) */}
            <OutfitDisplay outfit={msg.outfit} />

            {/* Styling Tips */}
            {msg.tips && (
              <div className="mt-3 px-4 py-3 rounded-xl bg-purple-500/10 border border-purple-400/20 max-w-[90%]">
                <div className="text-xs font-semibold text-purple-300 mb-1 tracking-wider uppercase">
                  Suggestions
                </div>
                <div className="text-sm text-gray-200 leading-relaxed">
                  {msg.tips}
                </div>
              </div>
            )}

            {/* Palette */}
            {msg.alternativePalette && (
              <div className="mt-2 px-4 py-3 rounded-xl bg-blue-500/10 border border-blue-400/20 max-w-[90%]">
                <div className="text-xs font-semibold text-blue-300 mb-1 tracking-wider uppercase">
                  Colors
                </div>
                <div className="text-sm text-gray-200">
                  {msg.alternativePalette}
                </div>
              </div>
            )}

            {/* Measurements */}
            {msg.measurements && (
              <div className="mt-2 px-4 py-3 rounded-xl bg-green-500/10 border border-green-400/20 max-w-[90%] w-full">
                <div className="text-xs font-semibold text-green-300 mb-2 tracking-wider uppercase">
                  Body Guide
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

        {loading && (
          <div className="flex items-start">
            <div className="px-4 py-3 rounded-2xl bg-white/5 border border-white/5 text-gray-400 flex items-center gap-2">
              <div className="animate-spin h-4 w-4 border-2 border-purple-400 border-t-transparent rounded-full" />
              Preparing your look...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

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
          <button onClick={onOpenGuide} className="flex items-center gap-1 hover:text-gray-300 transition-colors">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Guide</span>
          </button>
        )}
      </div>
    </div>
  )
}