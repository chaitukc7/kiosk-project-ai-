import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router-dom";

const PersonalDetails = () => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");

  // Clear old data when component loads
  useEffect(() => {
    console.log("Clearing old personal data from localStorage");
    localStorage.removeItem("personalData");
    localStorage.removeItem("userName");
    localStorage.removeItem("userPhone");
  }, []);

  const handleContinue = () => {
    // Clear any old data first
    localStorage.removeItem("personalData");
    localStorage.removeItem("userName");
    localStorage.removeItem("userPhone");
    
    const personalData = { name, phone };
    console.log("Saving personal data:", personalData);
    localStorage.setItem("personalData", JSON.stringify(personalData));
    console.log("Saved to localStorage:", localStorage.getItem("personalData"));
    
    // Also set individual fields as backup
    localStorage.setItem("userName", name);
    localStorage.setItem("userPhone", phone);
    
    navigate("/payment");
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-white text-3xl font-bold mb-4">Personal Details</h1>
          <p className="text-slate-400">
            By providing this information you will receive exciting offers & discounts.
          </p>
        </div>
        
        <div className="space-y-6">
          <div>
            <label className="block text-white mb-2 font-medium">Please enter your name</label>
            <Input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="John Doe"
              className="bg-slate-800 border-slate-600 text-white placeholder-slate-400"
            />
          </div>
          
          <div>
            <label className="block text-white mb-2 font-medium">Please enter your mobile number</label>
            <div className="flex">
              <span className="bg-slate-800 text-white px-3 py-3 rounded-l-md border border-slate-600">
                US +1
              </span>
              <Input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="Mobile number"
                className="flex-1 bg-slate-800 border-slate-600 text-white placeholder-slate-400 rounded-l-none"
              />
            </div>
          </div>
          
          <Button
            onClick={handleContinue}
            className="w-full bg-orange-500 hover:bg-orange-600 text-white py-4 text-lg font-semibold rounded-lg mt-8"
          >
            CONTINUE
          </Button>
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

export default PersonalDetails;