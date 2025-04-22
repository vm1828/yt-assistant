import { useState } from "react";
import DropdownPanel from "./DropdownPanel";
import { User } from "@auth0/auth0-react";

interface UserButtonProps {
  user: User;
}

export default function UserButton({ user }: UserButtonProps) {
  const [isDropdownVisible, setDropdownVisible] = useState(false);

  return (
    <div className="absolute top-4 right-4">
      <button
        onClick={() => setDropdownVisible(!isDropdownVisible)}
        className="flex items-center justify-center w-12 h-12 bg-gray-600 text-white rounded-full shadow-md"
      >
        {user?.nickname?.[0]?.toUpperCase() || "U"}
      </button>

      {/* Dropdown Panel */}
      {isDropdownVisible && <DropdownPanel user={user} />}
    </div>
  );
}
