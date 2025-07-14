import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { ShoppingBag, UtensilsCrossed } from "lucide-react";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
      <div className="w-full max-w-4xl text-center">
        <div className="mb-12">
          <h1 className="text-6xl font-bold text-orange-500 mb-4">Kiosk</h1>
          <p className="text-slate-300 text-2xl mb-4">Self checkout</p>
          <p className="text-slate-400 text-lg mb-2">Empower Your Checkout Experience</p>
          <p className="text-slate-400 text-lg">Seamless Self-Checkout at Your Fingertip</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          <div className="bg-slate-800 rounded-lg p-8 hover:bg-slate-700 transition-colors">
            <div className="flex justify-center mb-6">
              <div className="flex gap-2">
                <div className="w-8 h-8 bg-blue-500 rounded"></div>
                <div className="w-8 h-8 bg-orange-500 rounded"></div>
              </div>
            </div>
            <h3 className="text-2xl font-semibold text-white mb-4">Pickup</h3>
            <p className="text-slate-400 mb-8">
              User scanner to scan and add items to cart
            </p>
            <Button
              onClick={() => navigate("/menu?type=pickup")}
              className="w-full bg-orange-500 hover:bg-orange-600 text-white py-4 text-lg font-semibold rounded-lg"
            >
              Get Started
            </Button>
          </div>
          
          <div className="bg-slate-800 rounded-lg p-8 hover:bg-slate-700 transition-colors">
            <div className="flex justify-center mb-6">
              <div className="flex gap-2">
                <div className="w-8 h-8 bg-pink-400 rounded-full"></div>
                <div className="w-8 h-8 bg-orange-500 rounded"></div>
              </div>
            </div>
            <h3 className="text-2xl font-semibold text-white mb-4">Dine In</h3>
            <p className="text-slate-400 mb-8">
              Select items from menu and add to cart
            </p>
            <Button
              onClick={() => navigate("/menu?type=dinein")}
              className="w-full bg-orange-500 hover:bg-orange-600 text-white py-4 text-lg font-semibold rounded-lg"
            >
              Get Started
            </Button>
          </div>
        </div>
        
        <div className="text-center mt-12">
          <p className="text-slate-500 text-sm flex items-center justify-center gap-1">
            Powered by
            <span className="text-blue-400 font-semibold">NOVA</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;