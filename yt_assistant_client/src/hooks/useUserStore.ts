import { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";

import { logger } from "@/utils";
import { getCurrentUser } from "@/api";
import { useUserStore } from "@/store";

export const useUserData = () => {
  const { isAuthenticated, getAccessTokenSilently, user } = useAuth0();
  const { setUser, clearUser } = useUserStore();

  useEffect(() => {
    const fetchUser = async () => {
      if (isAuthenticated && user) {
        try {
          const token = await getAccessTokenSilently();
          const userData = await getCurrentUser(token);
          setUser(userData, user);
        } catch (err: unknown) {
          logger.error(
            { err: err instanceof Error ? err.message : "Unknown error" },
            "Error fetching user data",
          );
        }
      } else {
        clearUser();
      }
    };

    fetchUser();
  }, [isAuthenticated, getAccessTokenSilently, user, setUser, clearUser]);
};
