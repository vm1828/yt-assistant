import { create } from "zustand";
import { UserState } from "@/types";

export const useUserStore = create<UserState>((set) => ({
  user: null,
  auth0user: null,
  setUser: (user, auth0user) => set({ user, auth0user }),
  clearUser: () => set({ user: null, auth0user: null }),
}));
