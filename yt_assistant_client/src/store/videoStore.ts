import { create } from "zustand";
import type { VideoState } from "@/types";

const MAX_CACHE_SIZE = 10;

// Utility to keep only the latest N keys
function trimCache<T>(cache: Record<string, T>): Record<string, T> {
  const entries = Object.entries(cache);
  if (entries.length <= MAX_CACHE_SIZE) return cache;

  return Object.fromEntries(entries.slice(-MAX_CACHE_SIZE));
}

export const useVideoStore = create<VideoState>((set, get) => ({
  videos: [],
  transcriptCache: {},
  summaryCache: {},

  currentVideo: null,
  currentTranscript: null,
  currentSummary: null,

  addVideo: (video) =>
    set((state) => {
      const videoExists = state.videos.some((v) => v.id === video.id);
      const updatedVideos = videoExists
        ? state.videos
        : [...state.videos, video];

      return {
        videos: updatedVideos,
        currentVideo: video,
        currentTranscript: get().transcriptCache[video.id] || null,
        currentSummary: get().summaryCache[video.id] || null,
      };
    }),

  setCurrentVideo: (video) =>
    set({
      currentVideo: video,
      currentTranscript: get().transcriptCache[video.id] || null,
      currentSummary: get().summaryCache[video.id] || null,
    }),
  setCurrentTranscript: (transcript) => {
    const videoId = get().currentVideo?.id;
    if (!videoId) return;

    const cache = { ...get().transcriptCache, [videoId]: transcript };
    const trimmed = trimCache(cache);
    set({ currentTranscript: transcript, transcriptCache: trimmed });
  },
  setCurrentSummary: (summary) => {
    const videoId = get().currentVideo?.id;
    if (!videoId) return;

    const cache = { ...get().summaryCache, [videoId]: summary };
    const trimmed = trimCache(cache);
    set({ currentSummary: summary, summaryCache: trimmed });
  },

  setVideos: (videos) =>
    set(() => ({
      videos,
      currentVideo: videos.length > 0 ? videos[videos.length - 1] : null,
    })),

  reset: () =>
    set({
      videos: [],
      currentVideo: null,
      currentTranscript: null,
      currentSummary: null,
      transcriptCache: {},
      summaryCache: {},
    }),
}));
