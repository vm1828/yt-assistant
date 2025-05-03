import React from "react";
import { Sun, Moon } from "lucide-react";

import { useThemeStore } from "@/store";

export const UserButtonThemeSwitcher: React.FC = () => {
  const { theme, toggleTheme } = useThemeStore();

  return (
    <button
      onClick={toggleTheme}
      className="user-dropdown-button"
      aria-label="Toggle theme"
    >
      {theme === "light" ? (
        <Moon size={24} className="text-gray-600 dark:text-white" />
      ) : (
        <Sun size={24} className="text-white dark:text-white" />
      )}
    </button>
  );
};
