import { User } from "@auth0/auth0-react";

export type UserData = {
  id: string;
};

export type UserState = {
  user: UserData | null;
  setUser: (user: UserData) => void;
  clearUser: () => void;
};

export type UserButtonProps = {
  user: User;
};

export type UserButtonDropdownProps = {
  user: User;
};
