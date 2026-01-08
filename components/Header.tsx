"use client"

import { CircleUserRound, Settings, MessageCircleMore } from "lucide-react"

interface HeaderProps {
  onProfileClick: () => void
  onSettingsClick: () => void
  onHistoryToggle: () => void
}

export default function Header({ onProfileClick, onSettingsClick, onHistoryToggle }: HeaderProps) {
  return (
    <header className="absolute top-0 left-0 right-0 px-4 py-4 text-white z-20 flex items-center justify-center">
      <div className="absolute left-4 top-20">
        <button
          onClick={onHistoryToggle}
          className="p-2 rounded-lg hover:bg-white/10 transition-colors"
          aria-label="Toggle History"
        >
          <MessageCircleMore className="w-5 h-5" />
        </button>
      </div>

      <h1 className="text-2xl font-bold tracking-tight">Clothing App</h1>

      <div className="absolute right-4 flex gap-2">
        <button
          onClick={onProfileClick}
          className="p-2 rounded-lg hover:bg-white/10 transition-colors"
          aria-label="Profile"
        >
          <CircleUserRound className="w-5 h-5" />
        </button>
        <button
          onClick={onSettingsClick}
          className="p-2 rounded-lg hover:bg-white/10 transition-colors"
          aria-label="Settings"
        >
          <Settings className="w-5 h-5" />
        </button>
      </div>
    </header>
  )
}
