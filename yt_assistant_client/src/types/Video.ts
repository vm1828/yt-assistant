export type Video = {
  id: string;
  title: string;
};

export interface VideoState {
  videos: Video[];
  currentVideo: Video | null;
  addVideo: (video: Video) => void;
  setCurrentVideo: (video: Video) => void;
  setVideos: (videos: Video[]) => void;
  reset: () => void;
}
