import { render, screen, fireEvent } from "@testing-library/react";
import { useAuth0 } from "@auth0/auth0-react";
import { Mock } from "vitest";
import UserButtonLogout from "@/components/User/UserButtonLogout";

vi.mock("@auth0/auth0-react");

describe("UserButtonLogout Component", () => {
  test("calls logout function when the button is clicked", () => {
    // --------------- ARRANGE -------------------
    const mockLogout = vi.fn();
    (useAuth0 as unknown as Mock).mockReturnValue({
      logout: mockLogout,
    });
    // ---------------- ACT ----------------------
    render(<UserButtonLogout />);
    const logoutButton = screen.getByRole("button");
    fireEvent.click(logoutButton);
    // --------------- ASSERT --------------------
    expect(mockLogout).toHaveBeenCalledWith({
      logoutParams: { returnTo: window.location.origin },
    });
  });
});
