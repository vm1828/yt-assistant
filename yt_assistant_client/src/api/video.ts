// TODO: refactor

import { apiClient } from "@/api";
import { Video, Transcript, Summary, Conversation } from "@/types";
import { logger } from "@/utils";
import axios from "axios";

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
 * Add new video to the user account
 */
export const postVideo = async (
  video_id: string,
  token: string,
): Promise<Video> => {
  const res = await apiClient.post(
    "/videos/",
    { id: video_id },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );
  return res.data;
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
 * Create a summary for a video
 */
export const postSummary = async (
  videoId: string,
  token: string,
): Promise<Summary> => {
  const { data } = await apiClient.post<Summary>(
    `/summaries/`,
    { video_id: videoId },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );
  return data;
};

/**
 * Fetch existing summary by video ID — if 404, create it
 */
export const getSummaryByVideoId = async (
  videoId: string,
  token: string,
): Promise<Summary> => {
  // 1) Try to GET
  try {
    return await getVideoResource<Summary>(`/summaries/${videoId}`, token);
  } catch (err: unknown) {
    if (!(axios.isAxiosError(err) && err.response?.status === 404)) {
      logger.error(
        { err: err instanceof Error ? err.message : "Unknown error" },
        "Error fetching summary",
      );
      throw new Error("Failed to fetch summary");
    }
  }

  // 2) POST to create
  try {
    return await postSummary(videoId, token);
  } catch (creationErr: unknown) {
    logger.error(
      {
        err:
          creationErr instanceof Error ? creationErr.message : "Unknown error",
      },
      "Error creating summary",
    );
    throw new Error("Failed to create summary");
  }
};

/**
 * Create a conversation for a video
 */
export const postConversation = async (
  videoId: string,
  token: string,
): Promise<Conversation> => {
  const { data } = await apiClient.post<Conversation>(
    `/conversations/`,
    { video_id: videoId },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );
  return data;
};

/**
 * Fetch existing conversation by video ID — if 404, create it
 */
export const getConversationByVideoId = async (
  videoId: string,
  token: string,
): Promise<Conversation> => {
  // 1) Try to GET
  try {
    return await getVideoResource<Conversation>(
      `/conversations/${videoId}`,
      token,
    );
  } catch (err: unknown) {
    if (!(axios.isAxiosError(err) && err.response?.status === 404)) {
      logger.error(
        { err: err instanceof Error ? err.message : "Unknown error" },
        "Error fetching conversation",
      );
      throw new Error("Failed to fetch conversation");
    }
  }

  // 2) POST to create
  try {
    return await postConversation(videoId, token);
  } catch (creationErr: unknown) {
    logger.error(
      {
        err:
          creationErr instanceof Error ? creationErr.message : "Unknown error",
      },
      "Error creating conversation",
    );
    throw new Error("Failed to create conversation");
  }
};
