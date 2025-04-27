import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/test-utils/setup.ts"],
    coverage: {
      exclude: [
        "**/node_modules/**",
        "**/dist/**",
        "**/coverage/**",
        "**.config.**",
        "**/__mocks__/**",
        "__tests__/**",
        "**/tests/**",
        "**/logger.ts",
        "**/vite-env.**",
        "src/main.tsx",
        "test-utils/**",
      ],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"), // Resolve `@` to `src/`
    },
  },
});
