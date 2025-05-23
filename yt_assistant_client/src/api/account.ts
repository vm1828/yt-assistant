import { apiClient } from "@/api";
import { UserData } from "@/types";

export const getCurrentUser = async (token: string): Promise<UserData> => {
  const res = await apiClient.get("/accounts/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data;
};

export const postCurrentUser = async (token: string): Promise<UserData> => {
  const res = await apiClient.post("/accounts/", null, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data;
};
