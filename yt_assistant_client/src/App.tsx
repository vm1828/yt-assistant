import { useAuth0 } from "@auth0/auth0-react";

import { LoginButton, UserButton } from "@/components/User";
import { useUserStore } from "@/store";
import { useUserData, useThemeSwitcher } from "@/hooks";
import { logger } from "@/utils";

const App = () => {
  const { isAuthenticated, isLoading, user } = useAuth0();

  // Fetch user on login, clear on logout
  useUserData();

  logger.debug({ user: useUserStore.getState().user }, "Store State User");

  // Apply the theme to the body element
  useThemeSwitcher();

  let app;
  if (isLoading) {
    app = <div className="p-4 text-black">Loading...</div>;
  } else if (!isAuthenticated) {
    app = <LoginButton />;
  } else if (isAuthenticated && user) {
    app = (
      <>
        <UserButton />
      </>
    );
  }

  return <>{app}</>;
};

export default App;
