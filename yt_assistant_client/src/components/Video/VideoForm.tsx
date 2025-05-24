import { getVideoById, postVideo } from "@/api";
import { useVideoStore } from "@/store";
import { extractYouTubeId, logger } from "@/utils";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";
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

  const showValidationError = (message: string, timeout = 4000) => {
    setValidationError(message);
    setTimeout(() => setValidationError(null), timeout);
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();

    const videoId = extractYouTubeId(url);
    if (!videoId) {
      showValidationError("Please enter a valid YouTube URL");
      return;
    }

    const token = await getAccessTokenSilently();

    try {
      const video = await postVideo(videoId, token);
      addVideo(video);
      setCurrentVideo(video);
      setUrl("");
      showValidationError("");
    } catch (err) {
      logger.error(err, "Failed to add video");

      if (axios.isAxiosError(err) && err.response?.status === 409) {
        try {
          const video = await getVideoById(videoId, token);
          setCurrentVideo(video);
          showValidationError("Video already added to your account");
        } catch {
          showValidationError("Video already added, but failed to load");
        }
      } else {
        showValidationError("Failed to add video");
      }
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
