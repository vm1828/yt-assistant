import { useVideoStore } from "@/store";

export const VideoList = () => {
  const { videos, currentVideo, setCurrentVideo } = useVideoStore();

  return (
    <>
      {videos.length > 0 && (
        <div className="mt-5">
          <ul className="video-list-title">
            {[...videos].reverse().map((video) => (
              <li
                key={video.id}
                onClick={() => setCurrentVideo(video)}
                className={`my-2 cursor-pointer rounded-md px-2 py-1 transition-colors ${
                  video.id === currentVideo?.id ? "font-semibold" : ""
                }`}
              >
                {video.title}
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
};
