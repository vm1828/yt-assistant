export type Video = {
  id: string;
  title: string;
};

export type Transcript = {
  transcript_text: string;
};

export type Summary = {
  summary_text: string;
};

export interface VideoState {
  videos: Video[];
  transcriptCache: Record<string, Transcript>;
  summaryCache: Record<string, Summary>;

  currentVideo: Video | null;
  currentTranscript: Transcript | null;
  currentSummary: Summary | null;

  addVideo: (video: Video) => void;

  setCurrentVideo: (video: Video) => void;
  setCurrentTranscript: (transcript: Transcript) => void;
  setCurrentSummary: (summary: Summary) => void;
  setVideos: (videos: Video[]) => void;

  reset: () => void;
}
