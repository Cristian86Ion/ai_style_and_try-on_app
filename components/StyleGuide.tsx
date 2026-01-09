import { useState } from 'react'
import { ChevronLeft, ChevronRight, X } from 'lucide-react'

interface StyleGuideProps {
  onClose?: () => void
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
        ]
      }
    },
    {
      title: "Pants Cut",
      content: {
        type: 'pants' as const,
        description: "Choose the fit and silhouette for your lower body",
        options: [
          {
            name: "Regular Fit",
            description: "Regular upper leg, slightly tapered lower leg",
            keywords: ["regular pants", "regular fit"],
            example: "regular fit trousers",
            bestFor: ["Slim (elegant)", "Athletic (elegant)", "Average (elegant)"],
            note: "Default for elegant styles - balanced and versatile"
          },
          {
            name: "Loose Fit",
            description: "Regular upper leg, looser/relaxed lower leg",
            keywords: ["loose pants", "loose fit", "relaxed pants"],
            example: "loose fit comfortable pants",
            bestFor: ["Athletic (casual)", "Average (casual)"],
            note: "Default for casual styles - comfortable and modern"
          },
          {
            name: "Straight Fit",
            description: "Consistent width from hip to ankle, no taper",
            keywords: ["straight pants", "straight leg"],
            example: "straight leg pants",
            bestFor: ["Muscular", "Stocky", "Plus-size"],
            note: "Best for larger builds - provides room without baggy look"
          },
          {
            name: "Baggy / Wide-Leg",
            description: "Very wide, dramatic streetwear silhouette",
            keywords: ["baggy pants", "wide leg", "wide-leg"],
            example: "baggy wide-leg cargo pants",
            bestFor: ["All body types"],
            note: "Must explicitly request - streetwear staple"
          },
          {
            name: "Flared / Bootcut",
            description: "Fitted thigh, flares from knee",
            keywords: ["flared pants", "flare", "bootcut"],
            example: "flared pants with fitted thigh",
            bestFor: ["Slim, Athletic, Average"],
            note: "⚠️ CRITICAL: Must say 'flared' explicitly or won't be generated!",
            warning: true
          }
        ]
      }
    },
    {
      title: "Upper Part Cut",
      content: {
        type: 'tops' as const,
        description: "Define the fit and style for tops and shirts",
        options: [
          {
            name: "Regular Fit",
            description: "Classic fit with slight room - most versatile",
            keywords: ["regular top", "regular fit", "classic fit"],
            example: "regular fit shirt",
            bestFor: ["All body types"],
            note: "Default choice - professional and comfortable"
          },
          {
            name: "Relaxed Fit",
            description: "Comfortable with extra room, modern drape",
            keywords: ["relaxed top", "comfortable top", "relaxed fit"],
            example: "relaxed fit sweater",
            bestFor: ["Athletic (casual)", "Average (casual)", "Muscular", "Stocky", "Plus-size"],
            note: "Default for casual - comfort without being oversized"
          },
          {
            name: "Oversized",
            description: "Intentionally large, streetwear style (1.3x-1.7x larger)",
            keywords: ["oversized hoodie", "oversized top", "baggy top"],
            example: "oversized hoodie",
            bestFor: ["All body types (if requested)"],
            note: "Must explicitly request - makes garments significantly larger"
          },
          {
            name: "Cropped",
            description: "Ends above waistline - fashion-forward",
            keywords: ["cropped", "crop top", "cropped shirt"],
            example: "cropped fitted top",
            bestFor: ["Slim", "Athletic"],
            note: "Must explicitly request - shows proportions"
          },
          {
            name: "Longline",
            description: "Extended length, covers hips - modern streetwear",
            keywords: ["longline", "long top"],
            example: "longline shirt",
            bestFor: ["All body types"],
            note: "Elongates silhouette, trendy look"
          }
        ]
      }
    },
    {
      title: "Body Type Rules",
      content: {
        type: 'bodyTypes' as const,
        description: "How garments are sized based on body type",
        bodyTypes: [
          {
            name: "Slim (1.5x larger)",
            rules: {
              elegant: "Regular-fit pants and tops with comfortable drape",
              casual: "Regular-fit with relaxed silhouette",
              pants: "Regular fit - balanced proportions",
              tops: "Regular fit - highlights lean build without being tight"
            }
          },
          {
            name: "Athletic (1.7x larger)",
            rules: {
              elegant: "Regular-fit with extra room for shoulders",
              casual: "Loose-fit pants, relaxed tops for athletic build",
              pants: "Regular (elegant) or loose (casual) - room for thighs",
              tops: "Regular (elegant) or relaxed (casual) - room for shoulders/chest"
            }
          },
          {
            name: "Average (1.7x larger)",
            rules: {
              elegant: "Regular-fit - balanced and versatile",
              casual: "Loose-fit pants, relaxed tops",
              pants: "Regular (elegant) or loose (casual)",
              tops: "Regular (elegant) or relaxed (casual)"
            }
          },
          {
            name: "Muscular (1.8x larger)",
            rules: {
              elegant: "Straight-fit pants with room for muscle mass",
              casual: "Straight/loose-fit for comfort",
              pants: "Straight fit - significant room in thighs",
              tops: "Regular with extra room for developed chest/shoulders"
            }
          },
          {
            name: "Stocky (2.0x DOUBLE SIZE)",
            rules: {
              elegant: "Straight-fit for maximum comfort and flow",
              casual: "Straight/relaxed with generous proportions",
              pants: "Straight fit - avoid tapered, double-sized",
              tops: "Regular/relaxed - double-sized for comfort"
            }
          },
          {
            name: "Plus-Size (2.0x DOUBLE SIZE)",
            rules: {
              elegant: "Straight/wide-leg for flowing comfortable fit",
              casual: "Wide-leg/relaxed with flowing fabrics",
              pants: "Straight/wide-leg - double-sized, no taper",
              tops: "Relaxed/oversized - double-sized, flowing fabrics"
            }
          }
        ]
      }
    },
    {
      title: "Example Inputs",
      content: {
        type: 'examples' as const,
        description: "Copy these examples to get started",
        examples: [
          {
            style: "Classic Male (Average)",
            input: "male, 178, 75, 28, 42, zara hm, style: casual comfortable with regular fit",
            result: "Regular outfit (1.7x), balanced everyday style"
          },
          {
            style: "Classic Female (Slim)",
            input: "female, 165, 58, 26, 38, mango zara, style: elegant with fitted pieces",
            result: "Regular-fit outfit (1.5x), polished feminine look"
          },
          {
            style: "Bold Male (Athletic)",
            input: "male, 188, 90, 24, 44, diesel versace, style: bold colorful with loose fit",
            result: "Loose-fit (1.7x), vibrant colors, attention-grabbing"
          },
          {
            style: "Bold Female (Slim, Tall)",
            input: "female, 175, 62, 25, 39, gucci balmain, style: bold with flared pants and vibrant colors",
            result: "Flared pants (1.5x), bold palette, high-fashion"
          },
          {
            style: "Streetwear Male (Stocky)",
            input: "male, 175, 95, 30, 43, supreme off-white, style: streetwear with oversized pieces",
            result: "Oversized (2.0x DOUBLE), baggy streetwear style"
          },
          {
            style: "Multi-Brand Example",
            input: "female, 168, 65, 27, 39, massimo-dutti ralph-lauren, style: elegant minimalist",
            result: "Note: massimo-dutti and ralph-lauren use hyphens"
          },
          {
            style: "Brand Mix Example",
            input: "male, 182, 80, 29, 43, zara massimo-dutti hm, style: casual modern",
            result: "Mixing single-word (zara, hm) and multi-word (massimo-dutti) brands"
          }
        ]
      }
    }
  ]

  const nextPanel = () => setCurrentPanel((prev) => (prev + 1) % panels.length)
  const prevPanel = () => setCurrentPanel((prev) => (prev - 1 + panels.length) % panels.length)

  const currentData = panels[currentPanel]

  return (
    <div className="fixed inset-x-4 bottom-4 mx-auto w-full max-w-3xl bg-black/90 backdrop-blur-md border border-white/20 rounded-xl shadow-2xl overflow-hidden z-50 font-serif">
      {/* Navigation */}
      <div className="bg-white/5 border-b border-white/10 px-4 py-2 flex items-center justify-between">
        <button onClick={prevPanel} className="flex items-center gap-1 px-3 py-1.5 hover:bg-white/10 rounded-lg transition-all text-white/70 hover:text-white text-sm">
          <ChevronLeft className="w-4 h-4" />
          <span className="hidden sm:inline font-sans">Prev</span>
        </button>

        <div className="flex gap-1.5">
          {panels.map((_, idx) => (
            <button key={idx} onClick={() => setCurrentPanel(idx)} className={`h-1.5 rounded-full transition-all ${idx === currentPanel ? 'bg-white w-6' : 'bg-white/30 w-1.5'}`} />
          ))}
        </div>

        <button onClick={nextPanel} className="flex items-center gap-1 px-3 py-1.5 hover:bg-white/10 rounded-lg transition-all text-white/70 hover:text-white text-sm">
          <span className="hidden sm:inline font-sans">Next</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* Header */}
      <div className="bg-transparent px-4 py-4">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-serif text-white tracking-wide">{currentData.title}</h2>
          <div className="flex items-center gap-3">
            <div className="text-xs text-white/50 font-sans">{currentPanel + 1} / {panels.length}</div>
            {onClose && (
              <button onClick={onClose} className="text-white/50 hover:text-white transition-colors p-1">
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="px-4 pb-4 max-h-[50vh] overflow-y-auto scrollbar-hide font-sans">
        <style jsx>{`
          .scrollbar-hide::-webkit-scrollbar { display: none; }
          .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
        `}</style>

        {currentData.content.type === 'vibe' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {currentData.content.options.map((option: any, idx: number) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3 hover:bg-white/10 transition-all">
                  <h3 className="text-white font-serif text-lg mb-1">{option.name}</h3>
                  <div className="text-xs text-white/50 mb-1 font-medium uppercase tracking-wider">{option.keywords.join(", ")}</div>
                  <div className="text-xs text-white/60 italic mb-2">"{option.example}"</div>
                  <div className="text-xs text-white/70">→ {option.result}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'pants' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.options.map((option: any, idx: number) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3 hover:bg-white/10 transition-all">
                  <div className="flex justify-between items-baseline">
                    <h3 className="text-white font-serif text-lg mb-1">{option.name}</h3>
                    {option.warning && <span className="text-xs text-white/70 font-bold uppercase">⚠️ Must Request</span>}
                  </div>
                  <p className="text-xs text-white/70 mb-2">{option.description}</p>
                  <div className="text-xs text-white/50 mb-1 font-medium">Keywords: {option.keywords.join(", ")}</div>
                  <div className={`text-xs ${option.warning ? 'text-white/80' : 'text-white/70'} italic`}>{option.note}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'tops' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.options.map((option: any, idx: number) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3 hover:bg-white/10 transition-all">
                  <h3 className="text-white font-serif text-lg mb-1">{option.name}</h3>
                  <p className="text-xs text-white/70 mb-2">{option.description}</p>
                  <div className="text-xs text-white/50 mb-1 font-medium">Keywords: {option.keywords.join(", ")}</div>
                  <div className="text-xs text-white/70 italic">{option.note}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'bodyTypes' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.bodyTypes.map((bodyType: any, idx: number) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3">
                  <h3 className="text-white font-serif text-lg mb-3 border-b border-white/10 pb-1">{bodyType.name}</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    <div>
                      <div className="text-white/70 font-serif text-sm mb-1">Elegant</div>
                      <div className="text-white/80">{bodyType.rules.elegant}</div>
                    </div>
                    <div>
                      <div className="text-white/70 font-serif text-sm mb-1">Casual</div>
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
              {currentData.content.examples.map((example: any, idx: number) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-white font-serif text-lg">{example.style}</h3>
                  </div>
                  <div className="bg-black/40 border border-white/10 rounded p-2 mb-2 font-mono text-xs text-white overflow-x-auto">{example.input}</div>
                  <div className="text-xs text-white/70">
                    <span className="text-white/50 font-medium">Result:</span> {example.result}
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