import { create } from "zustand";
import type { VideoState } from "@/types";

export const useVideoStore = create<VideoState>((set) => ({
  videos: [],
  currentVideo: null,
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
  setVideos: (videos) => set({ videos }),
  reset: () => set({ videos: [], currentVideo: null }),
}));
