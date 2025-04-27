import { TEST_STORE_USER } from "@/test-utils/data/user";

export const ACCOUNT_AXIOS_RESPONSE = {
  data: { TEST_STORE_USER },
  status: 200,
  statusText: "OK",
  headers: {
    "content-type": "application/json",
  },
  config: {},
  request: {},
};

export const ACCOUNT_AXIOS_ERROR = {
  response: {
    data: { message: "Error fetching user data" },
    status: 500,
    statusText: "Internal Server Error",
    headers: {},
  },
  message: "Request failed with status code 500",
  config: {},
  code: "ERR_BAD_REQUEST",
};
