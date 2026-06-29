import { Activity, ChevronLeft, ChevronRight, Sparkles, TrendingUp } from "lucide-react"
import { useEffect, useState } from "react"

const slides = [
    {
        image: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&q=80",
        Icon: Sparkles,
        headline: "AI-Powered Analysis",
        subtext: "Backed by real-time web search",
    },
    {
        image: "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=1200&q=80",
        Icon: TrendingUp,
        headline: "Track Every Bet",
        subtext: "Win rate, P/L, and trends in one place",
    },
    {
        image: "https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=1200&q=80",
        Icon: Activity,
        headline: "Live Odds",
        subtext: "Pulled from real sportsbooks every 12 hours",
    },
]

const INTERVAL_MS = 3000

const FeatureCarousel = () => {
    const [current, setCurrent] = useState(0)
    const [paused, setPaused] = useState(false)

    const prev = () => setCurrent(c => (c - 1 + slides.length) % slides.length)
    const next = () => setCurrent(c => (c + 1) % slides.length)

    useEffect(() => {
        if (paused) return
        const id = setInterval(() => setCurrent(c => (c + 1) % slides.length), INTERVAL_MS)
        return () => clearInterval(id)
    }, [paused])

    return (
        <div
            className="relative rounded-xl overflow-hidden border aspect-[16/10]"
            aria-roledescription="carousel"
            onMouseEnter={() => setPaused(true)}
            onMouseLeave={() => setPaused(false)}
        >
            {/* Slides */}
            {slides.map((slide, i) => (
                <div
                    key={i}
                    className="absolute inset-0 transition-opacity duration-300"
                    style={{ opacity: i === current ? 1 : 0 }}
                    aria-hidden={i !== current}
                >
                    <img
                        src={slide.image}
                        alt=""
                        className="w-full h-full object-cover"
                        loading="lazy"
                    />
                    {/* Gradient overlay */}
                    <div
                        className="absolute inset-0"
                        style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0.25) 0%, rgba(0,0,0,0.82) 100%)" }}
                    />
                    {/* Slide content */}
                    <div className="absolute inset-0 flex flex-col justify-end p-6">
                        <slide.Icon className="h-6 w-6 text-primary mb-3" />
                        <h3
                            className="text-2xl font-bold tracking-tight text-white mb-1"
                            style={{ fontFamily: "'Space Grotesk', sans-serif" }}
                        >
                            {slide.headline}
                        </h3>
                        <p className="text-base text-white/70">{slide.subtext}</p>
                    </div>
                </div>
            ))}

            {/* Left arrow */}
            <button
                onClick={prev}
                aria-label="Previous slide"
                className="absolute left-3 top-1/2 -translate-y-1/2 z-10 h-8 w-8 flex items-center justify-center rounded-full bg-black/40 hover:bg-black/65 text-white transition-colors"
            >
                <ChevronLeft className="h-4 w-4" />
            </button>

            {/* Right arrow */}
            <button
                onClick={next}
                aria-label="Next slide"
                className="absolute right-3 top-1/2 -translate-y-1/2 z-10 h-8 w-8 flex items-center justify-center rounded-full bg-black/40 hover:bg-black/65 text-white transition-colors"
            >
                <ChevronRight className="h-4 w-4" />
            </button>

            {/* Dot indicators */}
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-10 flex items-center gap-1.5">
                {slides.map((_, i) => (
                    <button
                        key={i}
                        onClick={() => setCurrent(i)}
                        aria-label={`Go to slide ${i + 1}`}
                        className="h-1.5 rounded-full transition-all duration-300"
                        style={{
                            width: i === current ? "1.25rem" : "0.375rem",
                            backgroundColor: i === current ? "var(--color-primary)" : "rgba(255,255,255,0.4)",
                        }}
                    />
                ))}
            </div>
        </div>
    )
}

export default FeatureCarousel
