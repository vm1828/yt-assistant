import { useState } from "react";
import UserButtonDropdown from "./UserButtonDropdown";
import { User } from "@auth0/auth0-react";

interface UserButtonProps {
  user: User;
}

const UserButton = ({ user }: UserButtonProps) => {
  const [isDropdownVisible, setDropdownVisible] = useState(false);

  return (
    <div className="absolute top-4 right-4">
      {/* User Button */}
      <button
        className="user-button"
        onClick={() => setDropdownVisible(!isDropdownVisible)}
      >
        {user?.nickname?.[0]?.toUpperCase() || "U"}
      </button>

      {/* User Button Dropdown */}
      {isDropdownVisible && <UserButtonDropdown user={user} />}
    </div>
  );
};

export default UserButton;
