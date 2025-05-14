export type Video = {
  id: string;
  title: string;
};

export type Transcript = {
  transcript_text: string;
};

export interface VideoState {
  videos: Video[];
  currentVideo: Video | null;
  currentTranscript: Transcript | null;
  addVideo: (video: Video) => void;
  setCurrentVideo: (video: Video) => void;
  setCurrentTranscript: (transcript: Transcript) => void;
  setVideos: (videos: Video[]) => void;
  reset: () => void;
}
