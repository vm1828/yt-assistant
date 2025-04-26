import { ThemeState } from "@/types";
import { create } from "zustand";

export const useThemeStore = create<ThemeState>((set) => ({
  theme: "light", // default to light theme
  toggleTheme: () =>
    set((state) => {
      const newTheme = state.theme === "light" ? "dark" : "light";
      // Update the body class globally
      document.body.classList.remove(state.theme);
      document.body.classList.add(newTheme);
      return { theme: newTheme };
    }),
  setTheme: (theme) =>
    set((state) => {
      document.body.classList.remove(state.theme);
      document.body.classList.add(theme);
      return { theme };
    }),
}));
