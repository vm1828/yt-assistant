import { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";

import { logger } from "@/utils";
import { getCurrentUser, postCurrentUser } from "@/api";
import { useUserStore } from "@/store";

const fetchOrCreateUser = async (token: string) => {
  try {
    const userData = await getCurrentUser(token);
    logger.debug(userData, "Account fetched");
    return userData;
  } catch (err: unknown) {
    if (axios.isAxiosError(err) && err.response?.status === 404) {
      const userData = await postCurrentUser(token);
      logger.debug(userData, "Account created");
      return userData;
    }
    throw err;
  }
};

export const useUserData = () => {
  const { isAuthenticated, getAccessTokenSilently, user } = useAuth0();
  const { setUser, clearUser } = useUserStore();

  useEffect(() => {
    const handleUserFetch = async () => {
      if (!isAuthenticated || !user) {
        clearUser();
        return;
      }

      try {
        const token = await getAccessTokenSilently();
        const userData = await fetchOrCreateUser(token);
        setUser(userData, user);
      } catch (err: unknown) {
        logger.error(
          { err: err instanceof Error ? err.message : "Unknown error" },
          "Error fetching or creating user account",
        );
      }
    };

    handleUserFetch();
  }, [isAuthenticated, getAccessTokenSilently, user, setUser, clearUser]);
};
