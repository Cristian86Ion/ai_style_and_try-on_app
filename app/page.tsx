"use client"

import { useState, useEffect } from "react"
import LiquidEther from "@/frontend/LiquidEther"
import ChatWindow from "@/frontend/ChatWindow"
import Header from "@/frontend/Header"
import HistorySidebar from "@/frontend/HistorySidebar"
import SettingsModal from "@/frontend/SettingsModal"
import ProfileModal from "@/frontend/ProfileModal"
import StyleGuide from "@/frontend/StyleGuide"
import "@/frontend/LiquidEther.css"

interface Message {
  from: "user" | "llm"
  text: string
  image?: string
  tips?: string
  alternativePalette?: string
}

interface ChatHistory {
  id: string
  title: string
  userName: string
  timestamp: number
  bodyType: string
}

export default function Page() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const [styleGuideOpen, setStyleGuideOpen] = useState(false)
  const [theme, setTheme] = useState("dark")
  const [fontSize, setFontSize] = useState("medium")
  const [userName, setUserName] = useState("")
  const [bodyType, setBodyType] = useState("")
  const [isFirstTime, setIsFirstTime] = useState(true)
  const [profileComplete, setProfileComplete] = useState(false)

  const [chatHistory, setChatHistory] = useState<ChatHistory[]>([])
  const [currentChatId, setCurrentChatId] = useState<string | null>(null)
  const [currentMessages, setCurrentMessages] = useState<Message[]>([])

  useEffect(() => {
    const savedName = localStorage.getItem("userName")
    const savedBodyType = localStorage.getItem("bodyType")

    if (savedName && savedBodyType) {
      setUserName(savedName)
      setBodyType(savedBodyType)
      setIsFirstTime(false)
      setProfileComplete(true)
    } else {
      setProfileOpen(true)
    }
  }, [])

  useEffect(() => {
    if (userName && bodyType) {
      localStorage.setItem("userName", userName)
      localStorage.setItem("bodyType", bodyType)
      setProfileComplete(true)
      setIsFirstTime(false)
    }
  }, [userName, bodyType])

  useEffect(() => {
    if (theme === "light") {
      document.documentElement.classList.remove("dark")
    } else {
      document.documentElement.classList.add("dark")
    }
  }, [theme])

  const handleNewChat = () => {
    if (currentMessages.length > 0 && currentChatId) {
      const chatToSave: ChatHistory = {
        id: currentChatId,
        title: currentMessages[0]?.text.slice(0, 30) || "New conversation",
        userName: userName,
        timestamp: Date.now(),
        bodyType: bodyType,
      }

      setChatHistory((prev) => {
        const filtered = prev.filter((chat) => chat.id !== currentChatId)
        return [chatToSave, ...filtered]
      })
    }

    setCurrentChatId(Date.now().toString())
    setCurrentMessages([])
    setSidebarOpen(false)
  }

  const handleLoadChat = (chatId: string) => {
    if (currentMessages.length > 0 && currentChatId) {
      const chatToSave: ChatHistory = {
        id: currentChatId,
        title: currentMessages[0]?.text.slice(0, 30) || "New conversation",
        userName: userName,
        timestamp: Date.now(),
        bodyType: bodyType,
      }

      setChatHistory((prev) => {
        const filtered = prev.filter((chat) => chat.id !== currentChatId)
        return [chatToSave, ...filtered]
      })
    }

    setCurrentChatId(Date.now().toString())
    setCurrentMessages([])
    setSidebarOpen(false)
  }

  const handleMessagesUpdate = (messages: Message[]) => {
    setCurrentMessages(messages)
  }

  useEffect(() => {
    if (!currentChatId && profileComplete) {
      setCurrentChatId(Date.now().toString())
    }
  }, [profileComplete])

  const bgClass = theme === "light" ? "bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100" : "bg-black"

  if (!profileComplete) {
    return (
      <div className={`relative w-screen h-screen overflow-hidden ${bgClass}`}>
        <LiquidEther
          colors={theme === "light" ? ["#9b87f5", "#ffa6f6", "#c4b5fd"] : ["#5227ff", "#ff9ffc", "#b19eef"]}
          mouseForce={15}
          cursorSize={100}
          resolution={0.4}
          autoDemo={true}
          autoSpeed={0.5}
          autoIntensity={1.2}
        />
        <ProfileModal
          isOpen={profileOpen}
          onClose={() => setProfileOpen(false)}
          userName={userName}
          setUserName={setUserName}
          bodyType={bodyType}
          setBodyType={setBodyType}
          isFirstTime={isFirstTime}
        />
      </div>
    )
  }

  return (
    <div className={`relative w-screen h-screen overflow-hidden ${bgClass}`}>
      <LiquidEther
        colors={theme === "light" ? ["#9b87f5", "#ffa6f6", "#c4b5fd"] : ["#5227ff", "#ff9ffc", "#b19eef"]}
        mouseForce={15}
        cursorSize={100}
        resolution={0.4}
        autoDemo={true}
        autoSpeed={0.5}
        autoIntensity={1.2}
      />

      <Header
        onProfileClick={() => setProfileOpen(true)}
        onSettingsClick={() => setSettingsOpen(true)}
        onHistoryToggle={() => setSidebarOpen(!sidebarOpen)}
      />

      <HistorySidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        theme={theme}
        chatHistory={chatHistory}
        onNewChat={handleNewChat}
        onLoadChat={handleLoadChat}
        currentChatId={currentChatId}
      />

      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 w-[85%] md:w-[55%] lg:w-[45%] max-w-2xl">
        <ChatWindow
          theme={theme}
          fontSize={fontSize}
          messages={currentMessages}
          onMessagesUpdate={handleMessagesUpdate}
          bodyType={bodyType}
          userName={userName}
        />
      </div>

      <button
        onClick={() => setStyleGuideOpen(!styleGuideOpen)}
        className="fixed bottom-6 right-6 z-30 p-4 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-2xl hover:scale-110 transition-transform duration-200 border-2 border-white/20"
        aria-label="Toggle Style Guide"
      >
        <span className="text-2xl">📚</span>
      </button>

      <div
        className={`fixed bottom-24 right-6 z-20 w-[500px] max-h-[70vh] transition-all duration-300 ${
          styleGuideOpen ? "translate-x-0 opacity-100" : "translate-x-[120%] opacity-0"
        }`}
      >
        <div className="relative">
          <StyleGuide />
        </div>
      </div>

      <SettingsModal
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        theme={theme}
        setTheme={setTheme}
        fontSize={fontSize}
        setFontSize={setFontSize}
      />

      <ProfileModal
        isOpen={profileOpen}
        onClose={() => setProfileOpen(false)}
        userName={userName}
        setUserName={setUserName}
        bodyType={bodyType}
        setBodyType={setBodyType}
        isFirstTime={false}
      />
    </div>
  )
}