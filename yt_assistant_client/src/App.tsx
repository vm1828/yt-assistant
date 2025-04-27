import { useAuth0 } from "@auth0/auth0-react";
import LoginButton from "./components/User/UserLoginButton";
import UserButton from "./components/User/UserButton";
import { useEffect } from "react";
import { useThemeStore } from "./store/themeStore";
import { getCurrentUser } from "./api/endpoints/account";
import { useUserStore } from "./store/userStore";
import logger from "./utils/logger";
import { Theme } from "@/types";

const App = () => {
  const { isAuthenticated, isLoading, user, getAccessTokenSilently } =
    useAuth0();

  // Fetch user on login, clear on logout ------- TODO: move to hooks/useUserData.ts
  const { setUser, clearUser } = useUserStore();
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = await getAccessTokenSilently();
        const userData = await getCurrentUser(token);
        setUser(userData);
      } catch (err: unknown) {
        logger.error(
          { err: err instanceof Error ? err.message : "Unknown error" },
          "Error fetching user data"
        );
      }
    };
    if (isAuthenticated) {
      fetchUser();
    } else {
      clearUser();
    }
  }, [isAuthenticated, getAccessTokenSilently, setUser, clearUser]);

  logger.debug({ user: useUserStore.getState().user }, "Store State User");

  // Apply the theme to the body element ------- TODO: move to hooks/useThemeSwitcher.ts
  const { theme } = useThemeStore();
  useEffect(() => {
    const html = document.documentElement;
    if (theme === Theme.DARK) {
      html.classList.add(Theme.DARK);
      html.classList.remove(Theme.LIGHT);
    } else {
      html.classList.add(Theme.LIGHT);
      html.classList.remove(Theme.DARK);
    }
  }, [theme]);

  let app;
  if (isLoading) {
    app = <div className="p-4 text-black">Loading...</div>;
  } else if (!isAuthenticated) {
    app = <LoginButton />;
  } else if (isAuthenticated && user) {
    app = (
      <>
        <UserButton user={user} />
      </>
    );
  }

  return <>{app}</>;
};

export default App;
