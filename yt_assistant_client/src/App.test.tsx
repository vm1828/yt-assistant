import App from "@/App";
import { render, screen, waitFor } from "@testing-library/react";

import { TEST_AUTH0_USER, TEST_STORE_USER } from "@/test-utils/data/user";

import { useThemeStore } from "@/store/themeStore";

import { Theme, UserState } from "@/types";
import { act } from "react";
import { useUserStore } from "@/store/userStore";
import { Mock } from "vitest";
import { useAuth0 } from "@auth0/auth0-react";
import { getCurrentUser } from "@/api/endpoints/account";

// -------------------------- SETUP --------------------------

vi.mock("@auth0/auth0-react", () => ({
  useAuth0: vi.fn(),
}));
vi.mock("@/api/endpoints/account", () => ({
  getCurrentUser: vi.fn(),
}));

const mockUserStore = () => {
  const mockSetUser = vi.fn<(user: UserState["user"]) => void>();
  const mockClearUser = vi.fn<() => void>();

  useUserStore.setState({
    user: TEST_STORE_USER,
    setUser: mockSetUser,
    clearUser: mockClearUser,
  });

  return {
    mockSetUser,
    mockClearUser,
  };
};

// ================================ RENDERING ================================

describe("App Component - Rendering", () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  test("renders loading state", () => {
    // --------------- ARRANGE -------------------
    (useAuth0 as Mock).mockReturnValue({ isLoading: true });
    // ------------- ACT & ASSERT ----------------
    render(<App />);
    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  test("renders login button when not authenticated", () => {
    // --------------- ARRANGE -------------------
    (useAuth0 as Mock).mockReturnValue({ isAuthenticated: false });
    // ------------- ACT & ASSERT ----------------
    render(<App />);
    const loginButton = screen.getByRole("button", { name: /login/i });
    expect(loginButton).toBeInTheDocument();
    expect(loginButton).toHaveClass("user-login-button");
  });

  test("render user button when authenticated", () => {
    // --------------- ARRANGE -------------------
    (useAuth0 as Mock).mockReturnValue({
      isAuthenticated: true,
      getAccessTokenSilently: vi.fn(),
      user: TEST_AUTH0_USER,
    });
    // ------------- ACT & ASSERT ----------------
    render(<App />);
    const userButton = screen.getByRole("button", { name: /user button/i });
    expect(userButton).toBeInTheDocument();
    expect(userButton).toHaveClass("user-button");
  });
});

// ================================= AUTH =================================

describe("App Component - User Authentication & Store Management", () => {
  test("fetches user data on login and updates store", async () => {
    // --------------- ARRANGE -------------------
    const { mockSetUser } = mockUserStore();
    (useAuth0 as Mock).mockReturnValue({
      isAuthenticated: true,
      getAccessTokenSilently: vi.fn().mockResolvedValue("mock-token"),
      user: TEST_AUTH0_USER,
    });
    (getCurrentUser as Mock).mockResolvedValue(TEST_STORE_USER);
    // ------------- ACT & ASSERT ----------------
    render(<App />);
    await waitFor(() => {
      expect(mockSetUser).toHaveBeenCalledWith(TEST_STORE_USER);
    });
  });

  test("clears user data from store on logout", async () => {
    // --------------- ARRANGE -------------------
    const { mockClearUser } = mockUserStore();
    (useAuth0 as Mock).mockReturnValue({
      isAuthenticated: false,
      user: null,
    });
    // ------------- ACT & ASSERT ----------------
    render(<App />);
    await waitFor(() => {
      expect(mockClearUser).toHaveBeenCalledTimes(1);
    });
  });
});

// ================================= THEME =================================

describe("App Component - Theme Management", () => {
  test("renders light theme by default", () => {
    // ------------- ACT & ASSERT ----------------
    render(<App />);
    const html = document.documentElement;
    expect(html.classList.contains(Theme.LIGHT)).toBe(true);
    expect(html.classList.contains(Theme.DARK)).toBe(false);
  });

  test("renders dark theme when the theme is set to dark", async () => {
    // --------------- ARRANGE -------------------
    render(<App />); // Initial render, the default theme should be light
    const { setTheme } = useThemeStore.getState();
    // ---------------- ACT ----------------------
    await act(() => {
      setTheme(Theme.DARK);
    });
    // --------------- ASSERT --------------------
    await waitFor(() => {
      const html = document.documentElement;
      expect(html.classList.contains(Theme.DARK)).toBe(true);
      expect(html.classList.contains(Theme.LIGHT)).toBe(false);
    });
  });
});
