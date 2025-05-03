import { getVideoById } from "@/api";
import { useVideoStore } from "@/store";
import { extractYouTubeId, logger } from "@/utils";
import { useAuth0 } from "@auth0/auth0-react";
import { Play } from "lucide-react";
import { useState } from "react";

export const VideoForm = () => {
  const [url, setUrl] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);
  const { getAccessTokenSilently } = useAuth0();
  const { addVideo, setCurrentVideo } = useVideoStore();
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(e.target.value);
    setValidationError(null);
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();

    const videoId = extractYouTubeId(url);
    if (!videoId) {
      setValidationError("Please enter a valid YouTube URL.");
      return;
    }

    try {
      const token = await getAccessTokenSilently();
      const video = await getVideoById(videoId, token);
      addVideo(video);
      setCurrentVideo(video);
      setUrl("");
    } catch (err: unknown) {
      logger.error(
        { err: err instanceof Error ? err.message : "Unknown error" },
        "Failed to fetch video",
      );
      setValidationError("Failed to load video. Please try again.");
    }
  };

  return (
    <div className="pt-2">
      <form onSubmit={handleSubmit} className="relative">
        <input
          id="video-url"
          type="url"
          placeholder="https://www.youtube.com/watch?v=..."
          value={url}
          onChange={handleChange}
          className="input-field"
          required
        />
        <Play
          size={24}
          strokeWidth={2}
          className="video-submit-button"
          onClick={handleSubmit}
          aria-label="Submit video URL"
        />
      </form>
      {validationError && (
        <p className="mt-2 text-sm text-red-500">{validationError}</p>
      )}
    </div>
  );
};
