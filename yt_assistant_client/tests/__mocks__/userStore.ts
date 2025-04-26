import { vi } from "vitest";
import { UserData } from "@/types/User";

export type MockUser = UserData | null;
let mockUser: MockUser = null;
export const __setMockUser = (user: MockUser) => {
  mockUser = user;
};

export const useUserStore = Object.assign(
  vi.fn(() => ({
    setUser: vi.fn(),
  })),
  {
    getState: () => ({
      user: mockUser,
    }),
  }
);
