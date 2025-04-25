import apiClient from "../apiClient";

export const getCurrentUser = async (token: string) => {
  const res = await apiClient.get("/accounts/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data;
};
