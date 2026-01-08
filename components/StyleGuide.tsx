import { useState } from 'react'
import { ChevronLeft, ChevronRight, X } from 'lucide-react'

interface StyleGuideProps {
  onClose?: () => void
}

interface VibeOption {
  name: string
  keywords: string[]
  example: string
  result: string
}

interface PantsOption {
  name: string
  description: string
  keywords: string[]
  example: string
  bestFor: string[]
  note: string
  warning?: boolean
}

interface TopOption {
  name: string
  description: string
  keywords: string[]
  example: string
  bestFor: string[]
  note: string
}

interface BodyTypeRules {
  name: string
  rules: {
    elegant: string
    casual: string
    pants: string
    tops: string
  }
}

interface ExampleInput {
  style: string
  input: string
  result: string
}

export default function StyleGuide({ onClose }: StyleGuideProps) {
  const [currentPanel, setCurrentPanel] = useState(0)

  const panels = [
    {
      title: "Vibe & Aesthetic",
      content: {
        type: 'vibe' as const,
        description: "Define the overall feeling and mood of your outfit",
        options: [
          {
            name: "Elegant / Sophisticated",
            keywords: ["elegant", "sophisticated", "formal", "refined", "professional"],
            example: "elegant and sophisticated with clean lines",
            result: "Tailored pieces, structured silhouettes, dress shoes"
          },
          {
            name: "Casual / Comfortable",
            keywords: ["casual", "comfortable", "relaxed", "easy", "laid-back"],
            example: "casual and comfortable for everyday wear",
            result: "Relaxed fits, soft fabrics, sneakers"
          },
          {
            name: "Streetwear / Urban",
            keywords: ["streetwear", "urban", "modern", "hip-hop", "street"],
            example: "urban streetwear with oversized pieces",
            result: "Oversized hoodies, baggy pants, chunky sneakers"
          },
          {
            name: "Minimalist / Clean",
            keywords: ["minimalist", "minimal", "clean", "simple", "understated"],
            example: "minimalist clean lines with neutral tones",
            result: "Simple cuts, neutral colors, minimal details"
          },
          {
            name: "Bold / Statement",
            keywords: ["bold", "statement", "vibrant", "colorful", "eye-catching"],
            example: "bold and colorful with statement pieces",
            result: "Vibrant colors, unique cuts, attention-grabbing"
          }
        ] as VibeOption[]
      }
    },
    {
      title: "Pants Cut",
      content: {
        type: 'pants' as const,
        description: "Choose the fit and silhouette for your lower body",
        options: [
          {
            name: "Slim Fit",
            description: "Fitted through entire leg, tapered ankle",
            keywords: ["slim fit pants", "fitted pants", "skinny pants"],
            example: "slim fit pants with tapered ankle",
            bestFor: ["Slim body type ONLY"],
            note: "Only slim body type should use slim-fit"
          },
          {
            name: "Regular Fit",
            description: "Regular upper leg, slightly tapered lower leg",
            keywords: ["regular pants", "regular fit"],
            example: "regular fit trousers",
            bestFor: ["Slim (elegant)", "Athletic (elegant)", "Average (elegant)"],
            note: "Versatile, balanced - use for elegant styles"
          },
          {
            name: "Loose Fit",
            description: "Regular upper leg, looser/tapered lower leg",
            keywords: ["loose pants", "loose fit", "relaxed pants"],
            example: "loose fit comfortable pants",
            bestFor: ["Athletic (casual)", "Average (casual)"],
            note: "For athletic/average body types in casual styles"
          },
          {
            name: "Straight Fit",
            description: "Consistent width from hip to ankle",
            keywords: ["straight pants", "straight leg"],
            example: "straight leg pants",
            bestFor: ["Muscular", "Stocky", "Plus-size"],
            note: "Best for larger builds, no taper"
          },
          {
            name: "Baggy / Wide-Leg",
            description: "Very wide, dramatic streetwear silhouette",
            keywords: ["baggy pants", "wide leg", "wide-leg"],
            example: "baggy wide-leg cargo pants",
            bestFor: ["All body types"],
            note: "Streetwear staple, explicitly request it"
          },
          {
            name: "Flared / Bootcut",
            description: "Fitted thigh, flares from knee (MUST EXPLICITLY REQUEST)",
            keywords: ["flared pants", "flare", "bootcut", "bell-bottom"],
            example: "flared pants with fitted thigh",
            bestFor: ["Slim, Athletic, Average (>175cm M / >162cm F)"],
            note: "CRITICAL: Say 'flared' or won't be generated!",
            warning: true
          }
        ] as PantsOption[]
      }
    },
    {
      title: "Upper Part Cut",
      content: {
        type: 'tops' as const,
        description: "Define the fit and style for tops and shirts",
        options: [
          {
            name: "Slim Fit",
            description: "Form-fitting, follows body contours",
            keywords: ["fitted top", "slim top", "tight top"],
            example: "fitted turtleneck",
            bestFor: ["Slim (elegant)", "Athletic (elegant)"],
            note: "Shows physique, modern look"
          },
          {
            name: "Regular Fit",
            description: "Classic fit with slight room",
            keywords: ["regular top", "regular fit", "classic fit"],
            example: "regular fit shirt",
            bestFor: ["All body types"],
            note: "Safe choice, professional"
          },
          {
            name: "Relaxed Fit",
            description: "Comfortable with extra room",
            keywords: ["relaxed top", "comfortable top"],
            example: "relaxed fit sweater",
            bestFor: ["Athletic (casual)", "Average (casual)", "Muscular", "Stocky", "Plus-size"],
            note: "Comfort without being oversized"
          },
          {
            name: "Oversized",
            description: "Intentionally large, streetwear style",
            keywords: ["oversized hoodie", "oversized top", "baggy top"],
            example: "oversized hoodie",
            bestFor: ["All body types (if requested)"],
            note: "Statement piece, must explicitly request"
          },
          {
            name: "Boxy",
            description: "Square silhouette, drops from shoulders",
            keywords: ["boxy", "boxy shirt", "square top"],
            example: "boxy structured shirt",
            bestFor: ["Slim", "Athletic", "Average"],
            note: "Architectural, modern minimalist"
          },
          {
            name: "Cropped",
            description: "Ends above waistline",
            keywords: ["cropped", "crop top"],
            example: "cropped fitted top",
            bestFor: ["Slim", "Athletic"],
            note: "Fashion-forward, shows proportions"
          },
          {
            name: "Longline",
            description: "Extended length, covers hips",
            keywords: ["longline", "long top"],
            example: "longline shirt",
            bestFor: ["All body types"],
            note: "Modern streetwear, elongates"
          }
        ] as TopOption[]
      }
    },
    {
      title: "Body Type Rules",
      content: {
        type: 'bodyTypes' as const,
        description: "Fit recommendations based on your body type",
        bodyTypes: [
          {
            name: "Slim",
            rules: {
              elegant: "Slim-fit or regular-fit (can use slim-fit)",
              casual: "Regular-fit (avoid oversized)",
              pants: "Slim or regular upper leg, tapered lower",
              tops: "Slim-fit (elegant) or regular-fit (casual)"
            }
          },
          {
            name: "Athletic",
            rules: {
              elegant: "Regular-fit (regular upper leg, tapered lower)",
              casual: "Loose-fit (regular upper leg, looser lower)",
              pants: "Regular upper leg, looser/tapered lower leg",
              tops: "Regular (elegant) or relaxed/loose (casual)"
            }
          },
          {
            name: "Average",
            rules: {
              elegant: "Regular-fit (regular upper leg, tapered lower)",
              casual: "Loose-fit (regular upper leg, looser lower)",
              pants: "Regular upper leg, tapered or loose lower leg",
              tops: "Regular (elegant) or relaxed/loose (casual)"
            }
          },
          {
            name: "Muscular",
            rules: {
              elegant: "Straight-fit with room in thighs",
              casual: "Straight/loose-fit",
              pants: "Straight fit, room for muscle mass",
              tops: "Regular with room for chest/shoulders"
            }
          },
          {
            name: "Stocky",
            rules: {
              elegant: "Straight/regular (not tapered)",
              casual: "Straight/relaxed",
              pants: "Straight fit, avoid tapered",
              tops: "Regular/relaxed"
            }
          },
          {
            name: "Plus-Size",
            rules: {
              elegant: "Straight/wide-leg for comfort",
              casual: "Wide-leg/relaxed",
              pants: "Straight/wide-leg, no taper",
              tops: "Relaxed/oversized, flowing fabrics"
            }
          }
        ] as BodyTypeRules[]
      }
    },
    {
      title: "Example Inputs",
      content: {
        type: 'examples' as const,
        description: "Copy these examples to get started",
        examples: [
          {
            style: "Classic Male (Average Build)",
            input: "male, 178, 75, 28, 42, zara-hm, style: casual comfortable with regular fit",
            result: "Regular-fit outfit, balanced, everyday style"
          },
          {
            style: "Classic Female (Slim Build)",
            input: "female, 165, 58, 26, 38, mango-zara, style: elegant with fitted pieces",
            result: "Fitted outfit, polished, feminine"
          },
          {
            style: "Bold Male (Tall Athletic)",
            input: "male, 188, 90, 24, 44, diesel-versace, style: bold colorful with statement pieces and loose fit",
            result: "Vibrant colors, loose fit, attention-grabbing"
          },
          {
            style: "Bold Female (Tall Slim)",
            input: "female, 175, 62, 25, 39, gucci-balmain, style: bold with flared pants and vibrant colors",
            result: "Flared pants, bold palette, high-fashion"
          }
        ] as ExampleInput[]
      }
    }
  ]

  const nextPanel = () => setCurrentPanel((prev) => (prev + 1) % panels.length)
  const prevPanel = () => setCurrentPanel((prev) => (prev - 1 + panels.length) % panels.length)

  const currentData = panels[currentPanel]

  return (
    <div className="fixed inset-x-4 bottom-4 mx-auto w-full max-w-3xl bg-black/90 backdrop-blur-md border border-white/20 rounded-xl shadow-2xl overflow-hidden z-50 font-serif">
      {/* Navigation at Top */}
      <div className="bg-white/5 border-b border-white/10 px-4 py-2 flex items-center justify-between">
        <button
          onClick={prevPanel}
          className="flex items-center gap-1 px-3 py-1.5 hover:bg-white/10 rounded-lg transition-all text-white text-sm"
        >
          <ChevronLeft className="w-4 h-4 text-white" />
          <span className="hidden sm:inline font-sans">Prev</span>
        </button>

        <div className="flex gap-1.5">
          {panels.map((_, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentPanel(idx)}
              className={`h-1.5 rounded-full transition-all ${
                idx === currentPanel ? 'bg-white w-6' : 'bg-white/30 w-1.5'
              }`}
              aria-label={`Go to panel ${idx + 1}`}
            />
          ))}
        </div>

        <button
          onClick={nextPanel}
          className="flex items-center gap-1 px-3 py-1.5 hover:bg-white/10 rounded-lg transition-all text-white text-sm"
        >
          <span className="hidden sm:inline font-sans">Next</span>
          <ChevronRight className="w-4 h-4 text-white" />
        </button>
      </div>

      {/* Header */}
      <div className="bg-transparent px-4 py-4">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-serif text-white tracking-wide">{currentData.title}</h2>
          <div className="flex items-center gap-3">
            <div className="text-xs text-white/50 font-sans">
              {currentPanel + 1} / {panels.length}
            </div>
            {onClose && (
              <button
                onClick={onClose}
                className="text-white/70 hover:text-white transition-colors p-1"
                aria-label="Close guide"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Content Area - Compact with hidden scrollbar */}
      <div className="px-4 pb-4 max-h-[50vh] overflow-y-auto scrollbar-hide font-sans">
        <style jsx>{`
          .scrollbar-hide::-webkit-scrollbar {
            display: none;
          }
          .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
          }
        `}</style>

        {currentData.content.type === 'vibe' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {currentData.content.options.map((option, idx) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3 hover:bg-white/10 transition-all">
                  <h3 className="text-white font-serif text-lg mb-1">{option.name}</h3>
                  <div className="text-xs text-purple-300 mb-1 font-medium uppercase tracking-wider">
                    {option.keywords.join(", ")}
                  </div>
                  <div className="text-xs text-white/60 italic mb-2">
                    "{option.example}"
                  </div>
                  <div className="text-xs text-orange-200">
                    → {option.result}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'pants' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.options.map((option, idx) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3 hover:bg-white/10 transition-all">
                  <div className="flex justify-between items-baseline">
                    <h3 className="text-white font-serif text-lg mb-1">{option.name}</h3>
                    {option.warning && <span className="text-xs text-orange-400 font-bold uppercase">Attention</span>}
                  </div>
                  <p className="text-xs text-white/70 mb-2">{option.description}</p>
                  <div className="text-xs text-purple-300 mb-1 font-medium">
                    {option.keywords.join(", ")}
                  </div>
                  <div className={`text-xs ${option.warning ? 'text-orange-400' : 'text-orange-200'} italic`}>
                    {option.note}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'tops' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.options.map((option, idx) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3 hover:bg-white/10 transition-all">
                  <h3 className="text-white font-serif text-lg mb-1">{option.name}</h3>
                  <p className="text-xs text-white/70 mb-2">{option.description}</p>
                  <div className="text-xs text-purple-300 mb-1 font-medium">
                    {option.keywords.join(", ")}
                  </div>
                  <div className="text-xs text-orange-200 italic">
                    {option.note}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'bodyTypes' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.bodyTypes.map((bodyType, idx) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3">
                  <h3 className="text-white font-serif text-lg mb-3 border-b border-white/10 pb-1">{bodyType.name}</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    <div>
                      <div className="text-purple-300 font-serif text-sm mb-1">Elegant</div>
                      <div className="text-white/80">{bodyType.rules.elegant}</div>
                    </div>
                    <div>
                      <div className="text-orange-300 font-serif text-sm mb-1">Casual</div>
                      <div className="text-white/80">{bodyType.rules.casual}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'examples' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.examples.map((example, idx) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-white font-serif text-lg">{example.style}</h3>
                  </div>
                  <div className="bg-black/40 border border-white/10 rounded p-2 mb-2 font-mono text-xs text-white overflow-x-auto">
                    {example.input}
                  </div>
                  <div className="text-xs text-white/60">
                    <span className="text-orange-300 font-medium">Result:</span> {example.result}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}