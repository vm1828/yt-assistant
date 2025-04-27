import UserButtonThemeSwitcher from "./UserButtonThemeSwitcher";
import UserButtonLogout from "./UserButtonLogout";
import { UserButtonDropdownProps } from "@/types";

const UserButtonDropdown: React.FC<UserButtonDropdownProps> = ({
  user,
}: UserButtonDropdownProps) => {
  return (
    <div
      role="menu"
      aria-label="User Button Dropdown"
      className="user-button-dropdown"
    >
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
