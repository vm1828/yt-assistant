import { create } from "zustand";
import type { VideoState } from "@/types";

export const useVideoStore = create<VideoState>((set) => ({
  videos: [],
  currentVideo: null,
  currentTranscript: null,

  addVideo: (video) =>
    set((state) => {
      const videoExists = state.videos.some((v) => v.id === video.id);
      if (videoExists) {
        return { currentVideo: video };
      } else {
        const updatedVideos = [...state.videos, video];
        return { videos: updatedVideos, currentVideo: video };
      }
    }),

  setCurrentVideo: (video) => set({ currentVideo: video }),

  setCurrentTranscript: (transcript) => set({ currentTranscript: transcript }),

  setVideos: (videos) =>
    set(() => ({
      videos,
      currentVideo: videos.length > 0 ? videos[videos.length - 1] : null,
    })),

  reset: () => set({ videos: [], currentVideo: null }),
}));
