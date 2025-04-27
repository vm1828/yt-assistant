export enum Theme {
  LIGHT = "light",
  DARK = "dark",
}

export type ThemeState = {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
};
