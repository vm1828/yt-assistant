import { useAuth0 } from "@auth0/auth0-react";
import { LogOut } from "lucide-react";

const UserButtonLogout = () => {
  const { logout } = useAuth0();

  const handleLogout = () => {
    logout({ logoutParams: { returnTo: window.location.origin } });
  };

  return (
    <button
      onClick={handleLogout}
      className="user-button-logout flex items-center space-x-2 p-2 rounded-md hover:bg-gray-200 transition-colors"
    >
      <LogOut size={20} />
    </button>
  );
};

export default UserButtonLogout;
