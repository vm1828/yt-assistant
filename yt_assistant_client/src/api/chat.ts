import { apiClient } from "@/api";
import { Message } from "@/types";
import { logger } from "@/utils";

/**
 * Send user message and get AI response
 */
export const postChatMessage = async (
  conversationId: string,
  userMessage: string,
  token: string,
): Promise<Message> => {
  try {
    const { data } = await apiClient.post<Message>(
      "/messages/",
      {
        conversation_id: conversationId,
        user_message: userMessage,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    return data;
  } catch (err: unknown) {
    logger.error(
      { err: err instanceof Error ? err.message : "Unknown error" },
      "Error posting message",
    );
    throw new Error("Failed to send message");
  }
};
