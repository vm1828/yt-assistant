export const extractYouTubeId = (url: string): string | null => {
  const match = url.match(/[?&]v=([^&]+)/) || url.match(/youtu\.be\/([^?&]+)/);
  return match?.[1] || null;
};
