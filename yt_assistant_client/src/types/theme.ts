export enum Theme {
  LIGHT = "light",
  DARK = "dark",
}

export interface ThemeState {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}
