"use client"

import { X } from "lucide-react"

interface SettingsModalProps {
  isOpen: boolean
  onClose: () => void
  theme: string
  setTheme: (theme: string) => void
  fontSize: string
  setFontSize: (size: string) => void
}

export default function SettingsModal({ isOpen, onClose, theme, setTheme, fontSize, setFontSize }: SettingsModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-black/80 backdrop-blur-md rounded-2xl p-6 w-full max-w-md shadow-2xl border border-white/10">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Settings</h2>
          <button onClick={onClose} className="p-2 rounded-lg hover:bg-white/10 transition-colors" aria-label="Close">
            <X className="w-5 h-5 text-white" />
          </button>
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold mb-3 text-white">Theme</label>
            <div className="flex gap-3">
              <button
                onClick={() => setTheme("light")}
                style={{ backgroundColor: theme === "light" ? "#6b00bd" : "transparent" }}
                className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  theme === "light" ? "text-white" : "bg-white/10 text-white hover:bg-white/20"
                }`}
              >
                Light
              </button>
              <button
                onClick={() => setTheme("dark")}
                style={{ backgroundColor: theme === "dark" ? "#6b00bd" : "transparent" }}
                className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  theme === "dark" ? "text-white" : "bg-white/10 text-white hover:bg-white/20"
                }`}
              >
                Dark
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold mb-3 text-white">Font Size</label>
            <div className="flex gap-3">
              <button
                onClick={() => setFontSize("small")}
                style={{ backgroundColor: fontSize === "small" ? "#6b00bd" : "transparent" }}
                className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  fontSize === "small" ? "text-white" : "bg-white/10 text-white hover:bg-white/20"
                }`}
              >
                Small
              </button>
              <button
                onClick={() => setFontSize("medium")}
                style={{ backgroundColor: fontSize === "medium" ? "#6b00bd" : "transparent" }}
                className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  fontSize === "medium" ? "text-white" : "bg-white/10 text-white hover:bg-white/20"
                }`}
              >
                Medium
              </button>
              <button
                onClick={() => setFontSize("large")}
                style={{ backgroundColor: fontSize === "large" ? "#6b00bd" : "transparent" }}
                className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  fontSize === "large" ? "text-white" : "bg-white/10 text-white hover:bg-white/20"
                }`}
              >
                Large
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
