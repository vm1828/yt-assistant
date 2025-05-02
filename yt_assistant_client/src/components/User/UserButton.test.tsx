import { Mock } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";

import { UserButton } from "@/components/User";
import { useUserStore } from "@/store";
import { TEST_AUTH0_USER } from "@/test-utils/data";

vi.mock("@/store/userStore", () => ({
  useUserStore: vi.fn(),
}));

describe("UserButton Component", () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  test("renders user's nickname initial if available", () => {
    // --------------- ARRANGE -------------------
    (useUserStore as unknown as Mock).mockReturnValue(TEST_AUTH0_USER);

    // ------------- ACT & ASSERT ----------------
    render(<UserButton />);
    const userButton = screen.getByRole("button", { name: /user button/i });
    expect(userButton).toHaveTextContent("T"); // should be capitalized
    expect(userButton).toHaveClass("user-button");
  });

  test("renders 'U' if no nickname is provided", () => {
    // --------------- ARRANGE -------------------
    (useUserStore as unknown as Mock).mockReturnValue({ username: "" });

    // ------------- ACT & ASSERT ----------------
    render(<UserButton />);
    const userButton = screen.getByRole("button", { name: /user button/i });
    expect(userButton).toHaveTextContent("U");
  });

  test("toggles dropdown visibility on button click", () => {
    // --------------- ARRANGE -------------------
    (useUserStore as unknown as Mock).mockReturnValue(TEST_AUTH0_USER);

    // ------------- ACT & ASSERT ----------------
    render(<UserButton />);
    const userButton = screen.getByRole("button", { name: /user button/i });
    fireEvent.click(userButton); // First click - dropdown should appear
    const userButtonDropdown = screen.getByRole("menu", {
      name: /user button dropdown/i,
    });
    expect(userButtonDropdown).toBeInTheDocument();
    expect(userButtonDropdown).toHaveClass("user-dropdown");
    fireEvent.click(userButton); // Second click - dropdown should disappear
    expect(userButtonDropdown).not.toBeInTheDocument();
  });

  test("does not renders if user data is not available", () => {
    // --------------- ARRANGE -------------------
    (useUserStore as unknown as Mock).mockReturnValue(null); // Simulate no user loaded

    // ------------- ACT ------------------------
    render(<UserButton />);

    // ------------- ASSERT ---------------------
    const userButton = screen.queryByRole("button", { name: /user button/i });
    expect(userButton).toBeNull(); // Ensure no button is rendered
  });
});
