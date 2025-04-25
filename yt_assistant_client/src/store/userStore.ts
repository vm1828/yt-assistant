import { create } from "zustand";
import { UserData } from "../interfaces/User";

type UserState = {
  user: UserData | null;
  setUser: (user: UserData) => void;
  clearUser: () => void;
};

export const useUserStore = create<UserState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));
