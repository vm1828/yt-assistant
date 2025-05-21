import { getTranscriptByVideoId, getSummaryByVideoId } from "@/api";
import { useVideoStore } from "@/store";
import { useAuth0 } from "@auth0/auth0-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

enum ContentType {
  TRANSCRIPT = "transcript",
  SUMMARY = "summary",
}

type FetchOptions<T> = {
  cache: Record<string, T>;
  fetchFn: (id: string, token: string) => Promise<T | null>;
  setCurrent: (data: T) => void;
  getText: (data: T) => string;
};

export const Summary = () => {
  const [content, setContent] = useState<string>("No summary available yet.");
  const { getAccessTokenSilently } = useAuth0();
  const {
    currentVideo,
    transcriptCache,
    summaryCache,
    setCurrentTranscript,
    setCurrentSummary,
  } = useVideoStore();
  if (!currentVideo) return;

  const fetchContent = async <T,>(
    videoId: string,
    { cache, fetchFn, setCurrent, getText }: FetchOptions<T>,
  ) => {
    // Check cache first
    const cached = cache[videoId];
    if (cached) {
      setCurrent(cached);
      setContent(getText(cached));
      return;
    }

    // If not cached, fetch
    const token = await getAccessTokenSilently();
    const data = await fetchFn(videoId, token);
    if (data) {
      setCurrent(data); // also adds to cache via your store
      setContent(getText(data));
    }
  };

  const getSummary = () => {
    return fetchContent(currentVideo.id, {
      cache: summaryCache,
      fetchFn: getSummaryByVideoId,
      setCurrent: setCurrentSummary,
      getText: (s) => s.summary_text,
    });
  };

  const getTranscript = () => {
    return fetchContent(currentVideo.id, {
      cache: transcriptCache,
      fetchFn: getTranscriptByVideoId,
      setCurrent: setCurrentTranscript,
      getText: (t) => t.transcript_text,
    });
  };

  return (
    <div className="mt-5 flex h-full flex-col">
      <div className="mb-4 flex justify-between">
        <button onClick={getSummary} className="button-action mr-2 w-1/2">
          Summary
        </button>
        <button onClick={getTranscript} className="button-action ml-2 w-1/2">
          Transcript
        </button>
      </div>

      <div className="hide-scrollbar prose prose-sm max-h-[80vh] overflow-auto text-sm">
        <ReactMarkdown
          children={content}
          remarkPlugins={[remarkMath]}
          rehypePlugins={[rehypeKatex]}
        />
      </div>
    </div>
  );
};
