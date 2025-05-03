import { useAuth0 } from "@auth0/auth0-react";

import { LoginButton, UserButton } from "@/components/User";
import { useUserStore, useVideoStore } from "@/store";
import { useUserData, useThemeSwitcher, useVideos } from "@/hooks";
import { logger } from "@/utils";
import { Video } from "@/components/Video";
import { QAChat } from "@/components/QAChat";
import { Summary } from "@/components/Summary";

const App = () => {
  const { isAuthenticated, isLoading, user } = useAuth0();

  // Fetch user on login, clear on logout
  useUserData();
  logger.debug({ user: useUserStore.getState().user }, "Store State User");

  // Apply the theme to the body element
  useThemeSwitcher();

  // Fetch user videos, clear on logout
  useVideos();
  logger.debug({ videos: useVideoStore.getState().videos });

  let app;
  if (isLoading) {
    app = <div className="p-4 text-black">Loading...</div>;
  } else if (!isAuthenticated) {
    app = <LoginButton />;
  } else if (isAuthenticated && user) {
    app = (
      <div>
        <UserButton />

        <div className="flex h-screen flex-col px-2 md:flex-row">
          {/* Left side - Video + QAChat */}
          <div className="flex h-full w-full flex-col md:w-1/2">
            <div className="flex-shrink-0">
              <Video />
            </div>
            <div className="flex-1 overflow-hidden pt-2">
              <QAChat />
            </div>
          </div>

          {/* Right side - Summary */}
          <div className="overflow-y-autop-4 w-full flex-shrink-0 pt-2 pl-2 md:h-full md:w-1/2">
            <Summary />
          </div>
        </div>
      </div>
    );
  }

  return <>{app}</>;
};

export default App;
