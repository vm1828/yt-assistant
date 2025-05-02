import pino from "pino";

const isDev =
  import.meta.env.VITE_ENV === "local" || import.meta.env.VITE_ENV === "dev";
const isTest = import.meta.env.VITE_ENV === "test";

export const logger = pino({
  level: isTest ? "silent" : isDev ? "debug" : "info",
  transport: isDev
    ? {
        target: "pino-pretty",
        options: {
          colorize: true,
        },
      }
    : undefined, // no transport (default transport) in prod and test
});
