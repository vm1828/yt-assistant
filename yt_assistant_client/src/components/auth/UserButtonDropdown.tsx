import { User } from "@auth0/auth0-react";
import UserButtonThemeSwitcher from "./UserButtonThemeSwitcher";
import UserButtonLogout from "./UserButtonLogout";

interface UserButtonDropdownProps {
  user: User;
}

const UserButtonDropdown: React.FC<UserButtonDropdownProps> = ({
  user,
}: UserButtonDropdownProps) => {
  return (
    <div className="user-button-dropdown">
      <div className="text-sm truncate">{user?.email}</div>
      <div className="simple-border"></div>

      {/* Buttons */}
      <div className="flex justify-between items-center mt-2">
        <UserButtonThemeSwitcher />
        <UserButtonLogout />
      </div>
    </div>
  );
};

export default UserButtonDropdown;
