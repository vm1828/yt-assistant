import { render, screen, fireEvent } from "@testing-library/react";
import UserButton from "@/components/User/UserButton";
import { TEST_AUTH0_USER } from "@/test-utils/data/user";

describe("UserButton Component", () => {
  test("renders user's nickname initial if available", () => {
    // ------------- ACT & ASSERT ----------------
    render(<UserButton user={TEST_AUTH0_USER} />);
    const userButton = screen.getByRole("button", { name: /user button/i });
    expect(userButton).toHaveTextContent("T"); // should be capitalized
    expect(userButton).toHaveClass("user-button");
  });

  test("renders 'U' if no nickname is provided", () => {
    // --------------- ARRANGE -------------------
    const user = {};
    // ------------- ACT & ASSERT ----------------
    render(<UserButton user={user} />);
    const userButton = screen.getByRole("button", { name: /user button/i });
    expect(userButton).toHaveTextContent("U");
  });

  test("toggle dropdown visibility on button click", () => {
    // ------------- ACT & ASSERT ----------------
    render(<UserButton user={TEST_AUTH0_USER} />);
    const userButton = screen.getByRole("button", { name: /user button/i });
    fireEvent.click(userButton); // First click - dropdown should appear
    const userButtonDropdown = screen.getByRole("menu", {
      name: /user button dropdown/i,
    });
    expect(userButtonDropdown).toBeInTheDocument();
    expect(userButtonDropdown).toHaveClass("user-button-dropdown");
    fireEvent.click(userButton); // Second click - dropdown should disappear
    expect(userButtonDropdown).not.toBeInTheDocument();
  });
});
