"use client"

import { X } from "lucide-react"
import { useState, useEffect } from "react"

interface ProfileModalProps {
  isOpen: boolean
  onClose: () => void
  userName: string
  setUserName: (name: string) => void
  bodyType: string
  setBodyType: (type: string) => void
  isFirstTime: boolean
}

const VALID_BODY_TYPES = ["slim", "athletic", "average", "muscular", "stocky", "plus-size"]

export default function ProfileModal({
  isOpen,
  onClose,
  userName,
  setUserName,
  bodyType,
  setBodyType,
  isFirstTime,
}: ProfileModalProps) {
  const [tempName, setTempName] = useState(userName)
  const [tempBodyType, setTempBodyType] = useState(bodyType)

  useEffect(() => {
    setTempName(userName)
    setTempBodyType(bodyType)
  }, [userName, bodyType])

  if (!isOpen) return null

  const handleSave = () => {
    if (!tempName.trim()) {
      alert("Please enter your name")
      return
    }
    if (!tempBodyType) {
      alert("Please select a body type")
      return
    }
    setUserName(tempName)
    setBodyType(tempBodyType)
    onClose()
  }

  const handleClose = () => {
    if (isFirstTime && (!tempName.trim() || !tempBodyType)) {
      alert("Please complete your profile to continue")
      return
    }
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-black/80 backdrop-blur-md rounded-2xl p-6 w-full max-w-md shadow-2xl border border-white/10">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">
            {isFirstTime ? "Welcome! Complete Your Profile" : "Profile"}
          </h2>
          {!isFirstTime && (
            <button
              onClick={handleClose}
              className="p-2 rounded-lg hover:bg-white/10 transition-colors"
              aria-label="Close"
            >
              <X className="w-5 h-5 text-white" />
            </button>
          )}
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold mb-2 text-white">
              Your Name <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              value={tempName}
              onChange={(e) => setTempName(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Enter your name"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-white">
              Body Type <span className="text-red-400">*</span>
            </label>
            <select
              value={tempBodyType}
              onChange={(e) => setTempBodyType(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/10 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 appearance-none cursor-pointer"
            >
              <option value="" className="bg-gray-900">
                Select body type
              </option>
              {VALID_BODY_TYPES.map((type) => (
                <option key={type} value={type} className="bg-gray-900">
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={handleSave}
            style={{ backgroundColor: "#400070" }}
            className="w-full px-4 py-3 rounded-lg text-white font-medium hover:opacity-80 transition-opacity"
          >
            {isFirstTime ? "Get Started" : "Save"}
          </button>
        </div>
      </div>
    </div>
  )
}