import React from "react";
import { useThemeStore } from "@/store/themeStore";
import { Sun, Moon } from "lucide-react"; // Import Sun and Moon icons

const UserButtonThemeSwitcher: React.FC = () => {
  const { theme, toggleTheme } = useThemeStore();

  return (
    <button
      onClick={toggleTheme}
      className="p-3 rounded-lg transition-all"
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

export default UserButtonThemeSwitcher;
