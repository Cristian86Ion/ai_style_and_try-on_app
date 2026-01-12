import { useState } from 'react'
import { ChevronLeft, ChevronRight, X } from 'lucide-react'

interface StyleGuideProps {
  onClose?: () => void
}

export default function StyleGuide({ onClose }: StyleGuideProps) {
  const [currentPanel, setCurrentPanel] = useState(0)

  const panels = [
    {
      title: "Brand Categories",
      content: {
        type: 'brands' as const,
        description: "Choose brands to define your outfit style automatically",
        categories: [
          {
            name: "Flashy Streetwear",
            brands: ["yeezy", "off-white", "supreme", "rick-owens", "balenciaga", "commes-de-garcon"],
            style: "Swag streetwear",
            features: ["OVERSIZED", "Bold colorful patterns", "Jorts (S/S), tech pants (F/W)", "Tank tops + caps (S/S)", "Multi-pattern layering (F/W)"],
            example: "male, 180, 75, 24, 43, yeezy supreme, style: streetwear with oversized pieces"
          },
          {
            name: "Timeless Old Money",
            brands: ["tom-ford", "chanel", "balmain", "polo-ralph-lauren"],
            style: "Italian Riviera Elegance",
            features: ["REGULAR clean cut", "Oxford/leather shoes", "Minimal patterns", "Impeccable tailoring"],
            example: "male, 182, 78, 35, 44, tom-ford polo-ralph-lauren, style: elegant timeless"
          },
          {
            name: "Streetwear/Fast Fashion",
            brands: ["zara", "hm", "uniqlo", "massimo-dutti", "tommy-hilfiger", "hugo-boss", "stussy"],
            style: "Modern accessible fashion with interesting details",
            features: ["Regular/loose cuts", "Focus on color harmony", "Chest pockets, arm details", "Balanced wearable"],
            example: "female, 165, 58, 26, 38, zara massimo-dutti, style: casual modern with darker colors"
          },
          {
            name: "Avant-Garde/Runway",
            brands: ["dior", "ysl", "prada", "maison-margiela", "gucci", "louis-vuitton", "valentino"],
            style: "High-end runway OR extreme formality",
            features: ["Asymmetrical cuts", "Multiple zippers", "Leather pieces", "Long coats", "Architectural shapes"],
            example: "female, 175, 60, 26, 39, dior ysl, style: avant-garde runway model",
            note: "Runway style only if: male >185cm OR female >172cm + 'runway/avant-garde' keywords"
          },
          {
            name: "Sporty/Athletic",
            brands: ["nike", "adidas", "jordan", "puma", "lululemon"],
            style: "Performance sportswear for gym/training",
            features: ["Training pants/joggers", "Athletic tees", "NO formal outerwear", "Athletic sneakers", "Functional comfort"],
            example: "male, 178, 80, 28, 43, nike adidas, style: sporty gym training"
          }
        ]
      }
    },
    {
      title: "Color Palettes",
      content: {
        type: 'colors' as const,
        description: "Mention color tones to get specific palettes (40+ keywords detected)",
        options: [
          {
            name: "Dark/Darker Tones",
            keywords: ["darker colors", "dark palette", "dark tone"],
            colors: ["Midnight Blue", "Charcoal", "Espresso"],
            example: "style: casual evening with darker colors"
          },
          {
            name: "Bright/Brighter Tones",
            keywords: ["brighter colors", "bright palette", "vibrant"],
            colors: ["Sky Blue", "Coral", "Lemon Yellow"],
            example: "style: summer outfit with brighter colors"
          },
          {
            name: "Earthy Tones",
            keywords: ["earthy tone", "earthy colors", "earth palette"],
            colors: ["Terracotta", "Clay Brown", "Camel"],
            example: "style: casual with earthy tone"
          },
          {
            name: "Specific Colors",
            keywords: ["navy", "burgundy", "espresso", "camel", "olive", "charcoal"],
            colors: ["Use specific color name"],
            example: "style: elegant with navy palette"
          },
          {
            name: "Warm/Cool Tones",
            keywords: ["warm colors", "cool colors", "warm palette"],
            colors: ["Warm: Terracotta, Burnt Orange", "Cool: Sky Blue, Mint, Lavender"],
            example: "style: spring with cool colors"
          },
          {
            name: "Neutral/Monochrome",
            keywords: ["neutral", "monochrome", "black palette", "white palette"],
            colors: ["Neutral: Camel, Beige", "Monochrome: Black, White, Gray"],
            example: "style: minimalist with monochrome"
          }
        ]
      }
    },
    {
      title: "F/W Outerwear",
      content: {
        type: 'outerwear' as const,
        description: "Fall/Winter outerwear automatically selected based on style keywords",
        rules: [
          {
            keywords: "rock, cowboy, leather, bold, biker",
            garment: "Leather Jacket",
            colors: "Brown, Black, Red",
            example: "style: rock bold with leather jacket"
          },
          {
            keywords: "vintage, semiformal, retro",
            garment: "Trenchcoat or Overshirt",
            colors: "Beige, Brown, Navy",
            example: "style: vintage semiformal"
          },
          {
            keywords: "timeless, classic, elegant, clean, formal",
            garment: "Wool Coat",
            colors: "Black, Navy, Charcoal",
            example: "style: timeless elegant"
          },
          {
            keywords: "streetwear, casual, urban, comfortable",
            garment: "Puffer Jacket",
            colors: "Any color (bold encouraged)",
            example: "style: streetwear casual urban"
          },
          {
            keywords: "punk, grunge, emo, indie, alternative",
            garment: "Oversized Overshirt",
            colors: "Khaki, Dark Blue",
            extras: "+ Ripped loose jeans, long sleeve, dark accessories",
            example: "style: punk grunge indie"
          }
        ]
      }
    },
    {
      title: "Body Type Sizing",
      content: {
        type: 'bodyTypes' as const,
        description: "How garments are automatically sized based on body type",
        bodyTypes: [
          {
            name: "Slim",
            description: "Lean frame, thin limbs",
            rules: "Comfortable drape, regular fits work best"
          },
          {
            name: "Average",
            description: "Balanced proportions",
            rules: "Versatile - regular (elegant) or loose (casual)"
          },
          {
            name: "Athletic",
            description: "Toned muscles, V-shape",
            rules: "Extra room for shoulders/chest, loose pants for casual"
          },
          {
            name: "Muscular",
            description: "Developed muscle mass",
            rules: "Significant room for chest/thighs, avoid tight fits"
          },
          {
            name: "Stocky",
            description: "Solid frame, muscle + fat",
            rules: "Straight/relaxed fits, generous proportions"
          },
          {
            name: "Plus-Size",
            description: "Fuller figure, soft contours",
            rules: "Flowing comfortable fits, wide-leg pants, relaxed tops",
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
            style: "Flashy Streetwear Male",
            input: "male, 180, 75, 24, 43, yeezy supreme, style: streetwear oversized with brighter colors",
            result: "Oversized graphic pieces, bold colors, statement sneakers, cap"
          },
          {
            style: "Old Money Male",
            input: "male, 182, 78, 35, 44, tom-ford, style: timeless elegant",
            result: "Navy wool coat, tailored trousers, oxford shoes, refined aesthetic"
          },
          {
            style: "Casual Female Dark Tones",
            input: "female, 165, 58, 26, 38, zara massimo-dutti, style: casual evening with darker colors",
            result: "Midnight Blue/Charcoal palette, modern cuts, balanced style"
          },
          {
            style: "Runway Female (Tall)",
            input: "female, 175, 60, 26, 39, dior ysl, style: avant-garde runway model",
            result: "Asymmetrical cuts, leather pieces, architectural silhouette, zippers"
          },
          {
            style: "Sporty Male",
            input: "male, 178, 80, 28, 43, nike adidas, style: sporty gym training",
            result: "Training pants, athletic tee, performance sneakers, no formal wear"
          },
          {
            style: "Winter Leather Jacket",
            input: "male, 175, 70, 29, 42, zara, style: rock bold leather",
            result: "Brown/Black leather jacket, bold cuts, edgy aesthetic"
          },
          {
            style: "Punk/Grunge Winter",
            input: "male, 170, 65, 22, 41, carhartt, style: punk grunge indie",
            result: "Oversized khaki overshirt, ripped jeans, dark accessories"
          },
          {
            style: "Summer Earthy Tones",
            input: "female, 168, 62, 27, 38, mango cos, style: summer casual with earthy tone",
            result: "Terracotta/Camel colors, breathable fabrics, relaxed summer fit"
          },
          {
            style: "Plus-Size Female Formal",
            input: "female, 160, 85, 30, 38, massimo-dutti, style: formal elegant",
            result: "Long dress (silk S/S, wool F/W), flowing fit, 3.0x sizing"
          },
          {
            style: "Multi-Brand Mix",
            input: "male, 178, 75, 26, 43, zara hm uniqlo, style: casual comfortable modern",
            result: "Balanced streetwear, color harmony, interesting details"
          }
        ]
      }
    },
    {
      title: "Input Format",
      content: {
        type: 'format' as const,
        description: "Standard input structure and rules",
        sections: [
          {
            title: "Required Format",
            content: "sex, height(cm), weight(kg), age, shoe_size(EU), brands, style: description",
            example: "male, 178, 75, 26, 43, zara hm, style: casual modern"
          },
          {
            title: "Brand Names",
            content: "Single-word brands: zara, hm, nike, uniqlo\nMulti-word brands with hyphens: massimo-dutti, tommy-hilfiger, polo-ralph-lauren",
            example: "Correct: massimo-dutti, tom-ford\nIncorrect: massimo dutti, tom ford"
          },
          {
            title: "Body Type",
            content: "Selected from dropdown: slim, athletic, average, muscular, stocky, plus-size",
            note: "Don't write body type in chat - use dropdown only"
          },
          {
            title: "Style Keywords",
            content: "Vibe: casual, elegant, streetwear, minimalist, bold\nColors: darker colors, navy palette, earthy tone, brighter colors\nOuterwear: rock leather, vintage, timeless, punk grunge",
            example: "style: casual modern with darker colors and navy palette"
          },
          {
            title: "Formal Outfits",
            content: "Male: Complete suit with tie, NO visible ankles\nFemale: Long dress (silk S/S, thick cotton/wool F/W)",
            example: "style: formal business meeting"
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

        {currentData.content.type === 'brands' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.categories.map((cat: any, idx: number) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3 hover:bg-white/10 transition-all">
                  <h3 className="text-white font-serif text-lg mb-1">{cat.name}</h3>
                  <div className="text-xs text-white/50 mb-2 font-medium">{cat.brands.join(", ")}</div>
                  <div className="text-xs text-white/70 mb-2 italic">{cat.style}</div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-1 mb-2">
                    {cat.features.map((feature: string, i: number) => (
                      <div key={i} className="text-xs text-white/60">• {feature}</div>
                    ))}
                  </div>
                  <div className="bg-black/40 border border-white/10 rounded p-2 font-mono text-xs text-white/80 overflow-x-auto">{cat.example}</div>
                  {cat.note && <div className="text-xs text-white/50 mt-1 italic">Note: {cat.note}</div>}
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'colors' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {currentData.content.options.map((option: any, idx: number) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3 hover:bg-white/10 transition-all">
                  <h3 className="text-white font-serif text-base mb-1">{option.name}</h3>
                  <div className="text-xs text-white/50 mb-1 font-medium">{option.keywords.join(", ")}</div>
                  <div className="text-xs text-white/60 mb-2">→ {option.colors.join(", ")}</div>
                  <div className="text-xs text-white/70 italic">"{option.example}"</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'outerwear' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.rules.map((rule: any, idx: number) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="text-white font-serif text-base">{rule.garment}</h3>
                      <div className="text-xs text-white/50 font-medium">Keywords: {rule.keywords}</div>
                    </div>
                    <div className="text-xs text-white/60">{rule.colors}</div>
                  </div>
                  {rule.extras && <div className="text-xs text-white/60 mb-2">{rule.extras}</div>}
                  <div className="bg-black/40 border border-white/10 rounded p-2 font-mono text-xs text-white/80">"{rule.example}"</div>
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
                  <h3 className="text-white font-serif text-lg mb-1">{bodyType.name}</h3>
                  <div className="text-xs text-white/60 mb-2">{bodyType.description}</div>
                  <div className="text-xs text-white/70 mb-1">{bodyType.rules}</div>
                  {bodyType.note && <div className="text-xs text-white/50 italic">{bodyType.note}</div>}
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
                  <h3 className="text-white font-serif text-base mb-2">{example.style}</h3>
                  <div className="bg-black/40 border border-white/10 rounded p-2 mb-2 font-mono text-xs text-white overflow-x-auto">{example.input}</div>
                  <div className="text-xs text-white/70">
                    <span className="text-white/50 font-medium">Result:</span> {example.result}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentData.content.type === 'format' && (
          <div className="space-y-3">
            <p className="text-white/80 text-sm font-light italic">{currentData.content.description}</p>
            <div className="space-y-2">
              {currentData.content.sections.map((section: any, idx: number) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-sm p-3">
                  <h3 className="text-white font-serif text-base mb-2">{section.title}</h3>
                  <div className="text-xs text-white/70 mb-2 whitespace-pre-line">{section.content}</div>
                  {section.example && (
                    <div className="bg-black/40 border border-white/10 rounded p-2 font-mono text-xs text-white/80 whitespace-pre-line">{section.example}</div>
                  )}
                  {section.note && <div className="text-xs text-white/50 italic mt-2">{section.note}</div>}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}