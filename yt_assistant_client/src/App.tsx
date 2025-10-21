import { useAuth0 } from "@auth0/auth0-react";

import { LoginButton, UserButton } from "@/components/User";
import { useUserStore, useVideoStore } from "@/store";
import { useUserData, useThemeSwitcher, useVideos } from "@/hooks";
import { logger } from "@/utils";
import { Video } from "@/components/Video";
import { QAChat } from "@/components/QAChat";
import { Summary } from "@/components/Summary";
import { useState } from "react";
import { ChevronRight, ChevronLeft } from "lucide-react";

const App = () => {
  const [isSummaryOpen, setIsSummaryOpen] = useState(true);
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
    app = (
      <>
        <LoginButton />
        <div className="mt-4 text-center text-sm text-gray-600">
          Access is granted after admin approval. Please log in or register to
          begin.
          <br />
          Newly registered users are typically approved within 24 hours. If not,
          please contact the administration.
        </div>
      </>
    );
  } else if (isAuthenticated && user) {
    app = (
      <div>
        <UserButton />

        <div className="scroll-hidden mr-4 flex h-screen flex-col pl-6 md:flex-row">
          {/* Left side - Video + QAChat */}
          <div
            className={`mr-4 flex h-full flex-col overflow-hidden pl-6 md:w-full md:flex-col ${isSummaryOpen ? "md:w-1/2" : "md:w-full"}`}
          >
            <div className="flex-shrink-0">
              <Video />
            </div>
            <div className="flex-1 overflow-hidden pt-2">
              <QAChat />
            </div>
          </div>

          {/* Right side - Summary */}
          {isSummaryOpen && (
            <div className="w-full flex-shrink-0 overflow-hidden p-4 pt-2 pl-4 shadow-lg transition-all md:h-full md:w-1/2">
              <Summary />
            </div>
          )}

          {/* Toggle button */}
          <button
            onClick={() => setIsSummaryOpen(!isSummaryOpen)}
            className="collapsible-toggle collapsible-toggle-summary"
          >
            {isSummaryOpen ? (
              <ChevronRight className="h-5 w-5" />
            ) : (
              <ChevronLeft className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>
    );
  }

  return <>{app}</>;
};

export default App;
