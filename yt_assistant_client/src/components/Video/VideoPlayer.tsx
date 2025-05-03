import { useVideoStore } from "@/store";

export const VideoPlayer = () => {
  const { currentVideo } = useVideoStore();

  return (
    <>
      {currentVideo && (
        <div className="mx-auto w-full max-w-4xl pt-2">
          <div className="relative w-full" style={{ paddingTop: "56.25%" }}>
            <iframe
              className="absolute top-0 left-0 h-full w-full"
              src={`https://www.youtube.com/embed/${currentVideo.id}`}
              title={currentVideo.title}
              allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        </div>
      )}
    </>
  );
};
