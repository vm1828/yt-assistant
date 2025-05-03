import { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useVideoStore } from "@/store";
import { logger } from "@/utils";
import { getUserVideos } from "@/api";

export const useVideos = () => {
  const { isAuthenticated, getAccessTokenSilently } = useAuth0();
  const setVideos = useVideoStore((state) => state.setVideos);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const token = await getAccessTokenSilently();
        const data = await getUserVideos(token);
        setVideos(data);
        logger.debug(data, "Fetched videos");
      } catch (err) {
        logger.error(err, "Failed to fetch videos");
      }
    };

    if (isAuthenticated) fetchVideos();
  }, [isAuthenticated, getAccessTokenSilently, setVideos]);
};
