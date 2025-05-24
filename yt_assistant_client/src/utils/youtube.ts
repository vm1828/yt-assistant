export const extractYouTubeId = (url: string): string | null => {
  const match =
    url.match(/[?&]v=([a-zA-Z0-9_-]{11})/) ||
    url.match(/youtu\.be\/([a-zA-Z0-9_-]{11})/);
  return match?.[1] || null;
};
