import { useEffect } from "react";

import { useThemeStore } from "@/store/themeStore";
import { Theme } from "@/types";

export const useThemeSwitcher = () => {
  const { theme } = useThemeStore();
  useEffect(() => {
    const html = document.documentElement;
    if (theme === Theme.DARK) {
      html.classList.add(Theme.DARK);
      html.classList.remove(Theme.LIGHT);
    } else {
      html.classList.add(Theme.LIGHT);
      html.classList.remove(Theme.DARK);
    }
  }, [theme]);
};
