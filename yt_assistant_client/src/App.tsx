import { useAuth0 } from "@auth0/auth0-react";
import LoginButton from "./components/User/UserLoginButton";
import UserButton from "./components/User/UserButton";
import { useEffect } from "react";
import { useThemeStore } from "./store/themeStore";
import { getCurrentUser } from "./api/endpoints/account";
import { useUserStore } from "./store/userStore";
import logger from "./utils/logger";

const App = () => {
  const { isAuthenticated, isLoading, user, getAccessTokenSilently } =
    useAuth0();
  const { setUser } = useUserStore();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = await getAccessTokenSilently();
        const userData = await getCurrentUser(token);
        setUser(userData);
        logger.info(
          { userId: userData.id, userData },
          "User fetched successfully"
        );
      } catch (err) {
        logger.error(
          { error: err instanceof Error ? err.message : "Unknown error" },
          "Error fetching user"
        );
      }
    };

    if (isAuthenticated) {
      fetchUser();
    }
  }, [isAuthenticated, getAccessTokenSilently, setUser]);

  logger.debug({ user: useUserStore.getState().user }, "Store State User");

  // Apply the theme to the body element
  const { theme } = useThemeStore();
  useEffect(() => {
    const html = document.documentElement;
    if (theme === "dark") {
      html.classList.add("dark");
      html.classList.remove("light");
    } else {
      html.classList.add("light");
      html.classList.remove("dark");
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
