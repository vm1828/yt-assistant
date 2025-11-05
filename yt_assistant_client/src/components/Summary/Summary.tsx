import { getTranscriptByVideoId, getSummaryByVideoId } from "@/api";
import { useVideoStore } from "@/store";
import { useAuth0 } from "@auth0/auth0-react";
import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

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

  // Show cached summary immediately when currentVideo changes
  useEffect(() => {
    if (!currentVideo) return;
    const cachedSummary = summaryCache[currentVideo.id];
    if (cachedSummary) {
      setContent(cachedSummary.summary_text);
    } else {
      setContent("No summary available yet.");
    }
  }, [currentVideo, summaryCache]);

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
    if (!currentVideo) return;
    return fetchContent(currentVideo.id, {
      cache: summaryCache,
      fetchFn: getSummaryByVideoId,
      setCurrent: setCurrentSummary,
      getText: (s) => s.summary_text,
    });
  };

  const getTranscript = () => {
    if (!currentVideo) return;
    return fetchContent(currentVideo.id, {
      cache: transcriptCache,
      fetchFn: getTranscriptByVideoId,
      setCurrent: setCurrentTranscript,
      getText: (t) => t.transcript_text,
    });
  };

  return (
    <div className="mt-2 flex h-full flex-col overflow-hidden">
      {/* Buttons */}
      <div className="mb-2 flex flex-shrink-0 justify-between">
        <button onClick={getSummary} className="button-action mr-2 w-1/2">
          Summary
        </button>
        <button onClick={getTranscript} className="button-action ml-2 w-1/2">
          Transcript
        </button>
      </div>

      {/* Scrollable content */}
      <div className="hide-scrollbar min-h-0 flex-1 overflow-auto text-xs">
        <div className="w-full">
          <ReactMarkdown
            remarkPlugins={[remarkMath]}
            rehypePlugins={[rehypeKatex]}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
};
