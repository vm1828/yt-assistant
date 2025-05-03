import { useState } from "react";

import { UserButtonDropdown } from "@/components/User";
import { useUserStore } from "@/store";

export const UserButton = () => {
  const [isDropdownVisible, setDropdownVisible] = useState(false);

  const user = useUserStore((state) => state.auth0user);
  if (!user) return null; // Don’t render until user is loaded

  return (
    <div className="absolute top-4 right-4">
      {/* User Button */}
      <button
        className="user-button"
        aria-label="User Button"
        onClick={() => setDropdownVisible(!isDropdownVisible)}
      >
        {user?.nickname?.[0]?.toUpperCase() || "U"}
      </button>

      {/* User Button Dropdown */}
      {isDropdownVisible && <UserButtonDropdown />}
    </div>
  );
};
