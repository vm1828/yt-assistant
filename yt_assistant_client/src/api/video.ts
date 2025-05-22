import { apiClient } from "@/api";
import { Video, Transcript, Summary } from "@/types";

/**
 * Generic helper to fetch video resources with Bearer token auth
 */
async function getVideoResource<R>(path: string, token: string): Promise<R> {
  const { data } = await apiClient.get<R>(path, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return data;
}

/**
 * Fetch the list of user videos
 */
export const getUserVideos = async (token: string): Promise<Video[]> => {
  const { videos } = await getVideoResource<{ videos: Video[] }>(
    "/videos/",
    token,
  );
  return videos;
};

/**
 * Fetch a single video by ID
 */
export const getVideoById = async (
  videoId: string,
  token: string,
): Promise<Video> => {
  return getVideoResource<Video>(`/videos/${videoId}`, token);
};

/**
 * Fetch a transcript by video ID
 */
export const getTranscriptByVideoId = async (
  videoId: string,
  token: string,
): Promise<Transcript> => {
  return getVideoResource<Transcript>(`/transcripts/${videoId}`, token);
};

/**
 * Fetch a summary by video ID
 */
export const getSummaryByVideoId = async (
  videoId: string,
  token: string,
): Promise<Summary> => {
  return getVideoResource<Summary>(`/summaries/${videoId}`, token);
};
