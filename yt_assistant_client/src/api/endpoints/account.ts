import apiClient from "@/api/apiClient";
import { UserData } from "@/types";

export const getCurrentUser = async (token: string): Promise<UserData> => {
  const res = await apiClient.get("/accounts/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data;
};
