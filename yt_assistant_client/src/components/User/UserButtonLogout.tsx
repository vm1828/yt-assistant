import { useAuth0 } from "@auth0/auth0-react";
import { LogOut } from "lucide-react";

export const UserButtonLogout = () => {
  const { logout } = useAuth0();

  const handleLogout = () => {
    logout({ logoutParams: { returnTo: window.location.origin } });
  };

  return (
    <button onClick={handleLogout} className="user-dropdown-button">
      <LogOut size={20} />
    </button>
  );
};
