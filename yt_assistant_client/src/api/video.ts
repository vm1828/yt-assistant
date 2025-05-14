// TODO refactor

import { apiClient } from "@/api";
import { Video, Transcript } from "@/types";

export const getUserVideos = async (token: string): Promise<Video[]> => {
  const res = await apiClient.get("/videos/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data.videos;
};

export const getVideoById = async (
  videoId: string,
  token: string,
): Promise<Video> => {
  const res = await apiClient.get(`/videos/${videoId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data;
};

export const getTranscriptByVideoId = async (
  videoId: string,
  token: string,
): Promise<Transcript> => {
  const res = await apiClient.get(`/transcripts/${videoId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data;
};
