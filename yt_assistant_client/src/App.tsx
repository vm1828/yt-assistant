import { useAuth0 } from "@auth0/auth0-react";
import LoginButton from "./components/USER/LoginButton";
import UserButton from "./components/USER/UserButton";

export default function App() {
  const {
    isAuthenticated,
    isLoading,
    user,
    // getAccessTokenSilently
  } = useAuth0();

  // const handleToken = async () => {
  //   const token = await getAccessTokenSilently();
  //   console.log("Token:", token);
  // };
  // const token = await handleToken(); // handleToken encapsulates the logic
  // fetch("your-api-endpoint", { headers: { Authorization: `Bearer ${token}` } });

  if (isLoading) return <div className="p-4 text-black">Loading...</div>;

  return (
    <div className="min-h-screen bg-white text-black p-6 relative">
      {/* Login Button */}
      {!isAuthenticated && <LoginButton />}

      {/* User Button and Dropdown */}
      {isAuthenticated && user && <UserButton user={user} />}
    </div>
  );
}
