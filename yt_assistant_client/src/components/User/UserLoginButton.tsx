import { LogIn } from "lucide-react";
import { useAuth0 } from "@auth0/auth0-react";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <button onClick={() => loginWithRedirect()} className="user-login-button">
      <LogIn size={20} /> {/* Log In Icon */}
    </button>
  );
};

export default LoginButton;
