import { create } from "zustand";
import { Theme, ThemeState } from "@/types";

const updateTheme = (theme: Theme) => {
  document.body.classList.remove(Theme.LIGHT, Theme.DARK);
  document.body.classList.add(theme);
  return { theme };
};

const getInitialTheme = (): Theme => {
  const stored = localStorage.getItem("theme");
  return stored === Theme.DARK ? Theme.DARK : Theme.LIGHT;
};

export const useThemeStore = create<ThemeState>((set) => ({
  theme: getInitialTheme(),

  toggleTheme: () =>
    set((state) => {
      const newTheme = state.theme === Theme.LIGHT ? Theme.DARK : Theme.LIGHT;
      localStorage.setItem("theme", newTheme);
      updateTheme(newTheme);
      return { theme: newTheme };
    }),

  setTheme: (theme) =>
    set(() => {
      localStorage.setItem("theme", theme);
      updateTheme(theme);
      return { theme };
    }),
}));
