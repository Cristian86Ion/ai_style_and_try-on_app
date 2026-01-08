"use client"

import { MessageSquare, Plus } from "lucide-react"
import { useEffect } from "react"

interface Message {
  from: "user" | "llm"
  text: string
}

interface ChatHistory {
  id: string
  title: string
  userName: string
  timestamp: number
  bodyType?: string
}

interface HistorySidebarProps {
  isOpen: boolean
  onToggle: () => void
  theme: string
  chatHistory: ChatHistory[]
  onNewChat: () => void
  onLoadChat: (chatId: string) => void
  currentChatId: string | null
}

export default function HistorySidebar({
  isOpen,
  onToggle,
  theme,
  chatHistory,
  onNewChat,
  onLoadChat,
  currentChatId,
}: HistorySidebarProps) {
  const bgColor = "bg-black/70 backdrop-blur-md"
  const textColor = theme === "light" ? "text-gray-100" : "text-gray-100"
  const itemHover = "hover:bg-white/10"

  const groupChatsByDate = () => {
    const now = Date.now()
    const oneDay = 24 * 60 * 60 * 1000
    const sevenDays = 7 * oneDay

    const today: ChatHistory[] = []
    const yesterday: ChatHistory[] = []
    const lastSevenDays: ChatHistory[] = []

    if (!chatHistory || !Array.isArray(chatHistory)) {
      return []
    }

    chatHistory.forEach((chat) => {
      const diff = now - chat.timestamp
      if (diff < oneDay) {
        today.push(chat)
      } else if (diff < 2 * oneDay) {
        yesterday.push(chat)
      } else if (diff < sevenDays) {
        lastSevenDays.push(chat)
      }
    })

    return [
      { date: "Today", chats: today },
      { date: "Yesterday", chats: yesterday },
      { date: "Last 7 Days", chats: lastSevenDays },
    ].filter((group) => group.chats.length > 0)
  }

  const historyGroups = groupChatsByDate()

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const sidebar = document.getElementById("history-sidebar")
      const toggleButton = document.querySelector('[aria-label="Toggle History"]')

      if (
        isOpen &&
        sidebar &&
        !sidebar.contains(event.target as Node) &&
        toggleButton &&
        !toggleButton.contains(event.target as Node)
      ) {
        onToggle()
      }
    }

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside)
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [isOpen, onToggle])

  return (
    <div
      id="history-sidebar"
      className={`fixed top-0 left-0 h-screen w-64 ${bgColor} ${textColor} shadow-xl z-20 transition-transform duration-300 flex flex-col ${
        isOpen ? "translate-x-0" : "-translate-x-full"
      }`}
    >
      <div className="p-3 border-b border-gray-800">
        <button
          onClick={onNewChat}
          className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors`}
        >
          <Plus className="w-5 h-5" />
          <span className="font-medium">New chat</span>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-3">
        {historyGroups.length === 0 ? (
          <div className="text-center text-gray-500 text-sm mt-8">
            <p>No chat history yet.</p>
            <p className="mt-2">Start a conversation!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {historyGroups.map((group, idx) => (
              <div key={idx}>
                <h3 className="text-xs font-semibold text-gray-500 px-3 mb-2">{group.date}</h3>
                <div className="space-y-1">
                  {group.chats.map((chat) => (
                    <button
                      key={chat.id}
                      onClick={() => onLoadChat(chat.id)}
                      className={`w-full flex items-start gap-3 text-left px-3 py-2 rounded-lg ${itemHover} transition-colors text-sm group ${
                        chat.id === currentChatId ? "bg-white/20" : ""
                      }`}
                    >
                      <MessageSquare className="w-4 h-4 flex-shrink-0 opacity-70 mt-1" />
                      <div className="flex-1 min-w-0">
                        <div className="truncate font-medium">{chat.title}</div>
                        <div className="text-xs text-gray-400 truncate">
                          {chat.userName}
                          {chat.bodyType && <span className="text-gray-500"> • {chat.bodyType}</span>}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
