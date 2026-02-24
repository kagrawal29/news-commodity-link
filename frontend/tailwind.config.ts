import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        cyber: {
          cyan: "#00FFFF",
          magenta: "#FF00FF",
          green: "#00FF88",
          red: "#FF4444",
          gold: "#FFD700",
          blue: "#00d4ff",
          purple: "#8338ec",
          amber: "#ffbe0b",
        },
        bg: {
          dark: "#0a0a0f",
          card: "#1a1a2e",
          highlight: "#16213E",
        },
      },
      fontFamily: {
        mono: ["Share Tech Mono", "Fira Code", "monospace"],
        display: ["Orbitron", "monospace"],
      },
      animation: {
        "glow-pulse": "glowPulse 3s ease-in-out infinite",
        "border-glow": "borderGlow 4s ease-in-out infinite",
        "float": "float 6s ease-in-out infinite",
      },
      keyframes: {
        glowPulse: {
          "0%, 100%": { textShadow: "0 0 10px rgba(0,255,255,0.4)" },
          "50%": { textShadow: "0 0 25px rgba(0,255,255,0.7), 0 0 50px rgba(0,255,255,0.3)" },
        },
        borderGlow: {
          "0%, 100%": { borderColor: "rgba(0,255,255,0.2)", boxShadow: "0 0 10px rgba(0,255,255,0.06)" },
          "50%": { borderColor: "rgba(255,0,255,0.25)", boxShadow: "0 0 20px rgba(255,0,255,0.1)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
