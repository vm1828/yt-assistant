import { LogOut } from "lucide-react";
import { useAuth0, User } from "@auth0/auth0-react";

interface DropdownPanelProps {
  user: User;
}

export default function DropdownPanel({ user }: DropdownPanelProps) {
  const { logout } = useAuth0();

  const handleLogout = () => {
    logout({ logoutParams: { returnTo: window.location.origin } });
  };

  return (
    <div className="absolute top-16 right-0 w-40 bg-white shadow-lg rounded-lg p-3 space-y-2 border border-gray-200">
      {/* <div className="text-black text-center font-semibold">
        {user?.nickname}
      </div> */}
      <div className="text-gray-500 text-center text-sm truncate">
        {user?.email}
      </div>

      {/* Border between data and logout */}
      <div className="border-t border-gray-200 pt-2"></div>

      {/* Log Out Button */}
      <button
        onClick={handleLogout}
        className="w-full p-2 flex justify-center items-center bg-transparent text-gray-600 hover:text-gray-900"
      >
        <LogOut size={20} /> {/* Log Out Icon only */}
      </button>
    </div>
  );
}
