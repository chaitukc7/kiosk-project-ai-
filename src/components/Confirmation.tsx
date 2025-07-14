import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const Confirmation = () => {
  const navigate = useNavigate();
  const [countdown, setCountdown] = useState(10);

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          navigate("/");
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [navigate]);

  const handleStartNewOrder = () => {
    // Clear all stored data
    localStorage.removeItem("cart");
    localStorage.removeItem("orderData");
    localStorage.removeItem("personalData");
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
      <div className="w-full max-w-lg text-center">
        <div className="mb-8">
          <h1 className="text-white text-2xl font-bold mb-4">Payment</h1>
          <h2 className="text-orange-500 text-4xl font-bold mb-8">
            Thank you for your order !
          </h2>
          <p className="text-slate-400 text-lg mb-8">
            Your receipt is being printed.....
          </p>
        </div>

        {/* Receipt Icon */}
        <div className="flex justify-center mb-8">
          <div className="w-24 h-32 border-2 border-dashed border-slate-600 rounded-lg flex items-center justify-center">
            <div className="space-y-2">
              <div className="w-12 h-1 bg-slate-600 rounded"></div>
              <div className="w-8 h-1 bg-slate-600 rounded"></div>
              <div className="w-10 h-1 bg-slate-600 rounded"></div>
              <div className="w-4 h-1 bg-slate-600 rounded"></div>
              <div className="w-6 h-1 bg-slate-600 rounded"></div>
              <div className="w-3 h-3 bg-slate-600 rounded-full"></div>
            </div>
          </div>
        </div>

        <Button
          onClick={handleStartNewOrder}
          className="w-full max-w-md bg-orange-500 hover:bg-orange-600 text-white py-4 text-lg font-semibold rounded-lg mb-8"
        >
          Start New Order
        </Button>

        <p className="text-slate-500">
          Redirecting to home page in {countdown} seconds...
        </p>
        
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

export default Confirmation;