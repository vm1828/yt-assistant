// tailwind.config.ts
import { defineConfig } from "vite-plugin-windicss";

export default defineConfig({
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#4F46E5",     // Indigo
          secondary: "#22C55E",   // Green
          accent: "#F97316",      // Orange
          bg: "#F9FAFB",          // Light background
          surface: "#FFFFFF",     // Card background
          border: "#E5E7EB",      // Light border
          text: "#111827",        // Almost black
          subtext: "#6B7280",     // Muted
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
      borderRadius: {
        xl: "1rem",
      },
      boxShadow: {
        card: "0 4px 12px rgba(0, 0, 0, 0.06)",
      },
    },
  },
});
