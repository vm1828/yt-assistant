import { LogIn } from "lucide-react";
import { useAuth0 } from "@auth0/auth0-react";

export default function LoginButton() {
  const { loginWithRedirect } = useAuth0();

  return (
    <button
      onClick={() => loginWithRedirect()}
      className="absolute top-4 right-4 px-6 py-3 bg-gray-600 text-white rounded-xl shadow-md hover:bg-gray-700 transition"
    >
      <LogIn size={20} /> {/* Log In Icon */}
    </button>
  );
}
