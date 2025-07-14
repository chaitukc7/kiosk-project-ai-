import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router-dom";

const SignIn = () => {
  const [phoneNumber, setPhoneNumber] = useState("");
  const navigate = useNavigate();

  const handleSignIn = () => {
    if (phoneNumber.trim()) {
      // Store user info and navigate to home
      localStorage.setItem("userPhone", phoneNumber);
      navigate("/home");
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-orange-500 mb-2">Kiosk</h1>
          <p className="text-slate-300 text-lg">Self checkout</p>
        </div>
        
        <div className="bg-slate-800 rounded-lg p-8 shadow-xl">
          <h2 className="text-2xl font-semibold text-white text-center mb-6">
            Welcome Back
          </h2>
          <p className="text-slate-400 text-center mb-8">
            Please sign in to continue with your order
          </p>
          
          <div className="space-y-6">
            <div>
              <label className="block text-white mb-2">Phone Number</label>
              <div className="flex">
                <span className="bg-slate-700 text-white px-3 py-3 rounded-l-md border border-slate-600">
                  US +1
                </span>
                <Input
                  type="tel"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="Mobile number"
                  className="flex-1 bg-slate-700 border-slate-600 text-white placeholder-slate-400 rounded-l-none"
                />
              </div>
            </div>
            
            <Button
              onClick={handleSignIn}
              disabled={!phoneNumber.trim()}
              className="w-full bg-orange-500 hover:bg-orange-600 text-white py-4 text-lg font-semibold rounded-lg"
            >
              SIGN IN
            </Button>
          </div>
        </div>
        
        <div className="text-center mt-8">
          <p className="text-slate-500 text-sm flex items-center justify-center gap-1">
            Powered by
            <span className="text-blue-400 font-semibold">NOVA</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignIn;