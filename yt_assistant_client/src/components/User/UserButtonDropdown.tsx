import { UserButtonLogout, UserButtonThemeSwitcher } from "@/components/User";
import { useUserStore } from "@/store";

export const UserButtonDropdown = () => {
  const user = useUserStore((state) => state.auth0user);
  return (
    <div
      role="menu"
      aria-label="User Button Dropdown"
      className="user-dropdown"
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
