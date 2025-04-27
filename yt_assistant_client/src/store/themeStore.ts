import { create } from "zustand";
import { Theme, ThemeState } from "@/types";

const updateTheme = (theme: Theme) => {
  document.body.classList.remove(Theme.LIGHT, Theme.DARK);
  document.body.classList.add(theme);
  return { theme };
};

export const useThemeStore = create<ThemeState>((set) => ({
  theme: Theme.LIGHT,
  toggleTheme: () =>
    set((state) =>
      updateTheme(state.theme === Theme.LIGHT ? Theme.DARK : Theme.LIGHT)
    ),
  setTheme: (theme) => set(() => updateTheme(theme)),
}));
