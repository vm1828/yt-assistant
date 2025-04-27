import { Mock } from "vitest";
import apiClient from "@/api/apiClient";
import { getCurrentUser } from "@/api/endpoints/account";
import {
  ACCOUNT_AXIOS_ERROR,
  ACCOUNT_AXIOS_RESPONSE,
} from "@/test-utils/data/endpointAccount";

vi.mock("@/api/apiClient", () => ({
  default: {
    get: vi.fn(),
  },
}));

describe("getCurrentUser", () => {
  test("returns user data when API call is successful", async () => {
    // --------------- ARRANGE -------------------
    const mockToken = "mockToken123";
    (apiClient.get as Mock).mockResolvedValueOnce(ACCOUNT_AXIOS_RESPONSE);

    // ------------- ACT & ASSERT ----------------
    const result = await getCurrentUser(mockToken);
    expect(apiClient.get).toHaveBeenCalledWith("/accounts/me", {
      headers: { Authorization: `Bearer ${mockToken}` },
    });
    expect(result).toEqual(ACCOUNT_AXIOS_RESPONSE.data);
  });

  test("throws an error when API call fails", async () => {
    // --------------- ARRANGE -------------------
    const mockToken = "mockToken123";
    (apiClient.get as Mock).mockRejectedValueOnce(ACCOUNT_AXIOS_ERROR);

    // ------------- ACT & ASSERT ----------------
    await expect(getCurrentUser(mockToken)).rejects.toThrowError(
      ACCOUNT_AXIOS_ERROR.message
    );
  });
});
