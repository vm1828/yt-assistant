import { User } from "@auth0/auth0-react";

export type UserData = {
  id: string;
};

export type UserState = {
  user: UserData | null;
  auth0user: User | null;
  setUser: (user: UserData, auth0user: User) => void;
  clearUser: () => void;
};
