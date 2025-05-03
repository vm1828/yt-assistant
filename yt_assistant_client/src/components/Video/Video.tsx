import { VideoForm, VideoList, VideoPlayer } from "@/components/Video";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

export const Video = () => {
  const [isOpen, setIsOpen] = useState(true);
  return (
    <>
      {/* Collapsible Video Sidebar */}
      <aside className="video-sidebar">
        <VideoList />
      </aside>

      {/* Main Video Panel */}
      <div className="w-full">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="collapsible-toggle"
        >
          <span className="truncate">Video</span>
          {isOpen ? (
            <ChevronUp className="h-5 w-5" />
          ) : (
            <ChevronDown className="h-5 w-5" />
          )}
        </button>
        {isOpen && (
          <div>
            <VideoPlayer />
            <VideoForm />
          </div>
        )}
      </div>
    </>
  );
};
