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

export type Message = {
  id?: string;
  conversation_id?: string;
  user_message: string;
  ai_response: string;
};

export type Conversation = {
  id: string;
  video_id: string;
  messages: Message[];
};

export interface VideoState {
  videos: Video[];
  transcriptCache: Record<string, Transcript>;
  summaryCache: Record<string, Summary>;
  conversationCache: Record<string, Conversation>;
  // TODO handle long conversations (create separate cache for messages ??)

  currentVideo: Video | null;
  currentTranscript: Transcript | null;
  currentSummary: Summary | null;
  currentConversation: Conversation | null;

  addVideo: (video: Video) => void;

  setCurrentVideo: (video: Video) => void;
  setCurrentTranscript: (transcript: Transcript) => void;
  setCurrentSummary: (summary: Summary) => void;
  setCurrentConversation: (conversation: Conversation) => void;
  setVideos: (videos: Video[]) => void;

  reset: () => void;
}
