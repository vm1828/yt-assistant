import { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";

import { logger } from "@/utils";
import { getCurrentUser } from "@/api";
import { useUserStore } from "@/store";

export const useUserData = () => {
  const { isAuthenticated, getAccessTokenSilently, user } = useAuth0();
  const { setUser, clearUser } = useUserStore();

  useEffect(() => {
    if (isAuthenticated && user) {
      getAccessTokenSilently()
        .then((token) => getCurrentUser(token))
        .then((userData) => {
          setUser(userData, user);
        })
        .catch((err: unknown) => {
          logger.error(
            { err: err instanceof Error ? err.message : "Unknown error" },
            "Error fetching user data"
          );
        });
    } else {
      clearUser();
    }
  }, [isAuthenticated, getAccessTokenSilently, user, setUser, clearUser]);
};
