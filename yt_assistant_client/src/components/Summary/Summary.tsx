import { getTranscriptByVideoId } from "@/api";
import { useVideoStore } from "@/store";
import { useAuth0 } from "@auth0/auth0-react";
import { useState } from "react";

export const Summary = () => {
  const [content, setContent] = useState<string | null>(null);
  const { getAccessTokenSilently } = useAuth0();
  const { currentVideo, setCurrentTranscript } = useVideoStore();

  const generateSummary = () => {
    setContent(
      `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
      `.repeat(5),
    );
  };

  const getTranscript = async () => {
    const token = await getAccessTokenSilently();
    const transcript = await getTranscriptByVideoId(currentVideo!.id, token);
    setCurrentTranscript(transcript);
    setContent(transcript.transcript_text);
  };

  return (
    <div className="mt-5 flex h-full flex-col">
      <div className="mb-4 flex justify-between">
        <button onClick={generateSummary} className="button-action mr-2 w-1/2">
          Summary
        </button>

        <button onClick={getTranscript} className="button-action ml-2 w-1/2">
          Transcript
        </button>
      </div>

      <div className="hide-scrollbar max-h-[80vh] overflow-auto">
        <p className="text-justify text-sm">
          {content || "No summary available yet."}
        </p>
      </div>
    </div>
  );
};
