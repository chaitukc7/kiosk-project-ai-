import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useNavigate, useSearchParams } from "react-router-dom";
import { ArrowLeft, Plus, Search } from "lucide-react";

interface MenuItem {
  id: string;
  name: string;
  price: number;
  description: string;
  image: string;
  category: string;
}

const menuItems: MenuItem[] = [
  {
    id: "1",
    name: "Udon",
    price: 13.80,
    description: "Thick, chewy Japanese wheat noodles often served in a clear broth or stir-fried.",
    image: "/api/placeholder/100/100",
    category: "noodles"
  },
  {
    id: "2", 
    name: "Ramen",
    price: 13.80,
    description: "Thick, chewy Japanese wheat noodles often served in a clear broth or stir-fried.",
    image: "/api/placeholder/100/100",
    category: "noodles"
  },
  {
    id: "3",
    name: "Pad Thai",
    price: 13.80,
    description: "Thick, chewy Japanese wheat noodles often served in a clear broth or stir-fried.",
    image: "/api/placeholder/100/100",
    category: "noodles"
  },
  {
    id: "4",
    name: "Spaghetti Bolognese",
    price: 13.80,
    description: "Thick, chewy Japanese wheat noodles often served in a clear broth or stir-fried.",
    image: "/api/placeholder/100/100",
    category: "noodles"
  },
  {
    id: "5",
    name: "Pho",
    price: 13.80,
    description: "Thick, chewy Japanese wheat noodles often served in a clear broth or stir-fried.",
    image: "/api/placeholder/100/100",
    category: "noodles"
  }
];

const categories = [
  { id: "noodles", name: "Noodles", icon: "🍜", active: true },
  { id: "burgers", name: "Burgers", icon: "🍔", active: false },
  { id: "drinks", name: "Drinks", icon: "🥤", active: false },
  { id: "rice", name: "Rice Bowl", icon: "🍚", active: false }
];

const Menu = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [selectedCategory, setSelectedCategory] = useState("noodles");
  const [cart, setCart] = useState<{[key: string]: number}>({});
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    // Save order type from URL parameter
    const orderType = searchParams.get('type');
    if (orderType) {
      localStorage.setItem("orderType", orderType === 'pickup' ? 'Pick Up' : 'Dine In');
    }
  }, [searchParams]);

  const addToCart = (itemId: string) => {
    setCart(prev => ({
      ...prev,
      [itemId]: (prev[itemId] || 0) + 1
    }));
  };

  const removeFromCart = (itemId: string) => {
    setCart(prev => {
      const newCart = { ...prev };
      if (newCart[itemId] > 1) {
        newCart[itemId]--;
      } else {
        delete newCart[itemId];
      }
      return newCart;
    });
  };

  const getTotalItems = () => {
    return Object.values(cart).reduce((sum, count) => sum + count, 0);
  };

  const getTotalPrice = () => {
    return Object.entries(cart).reduce((sum, [itemId, count]) => {
      const item = menuItems.find(item => item.id === itemId);
      return sum + (item ? item.price * count : 0);
    }, 0);
  };

  const handleCheckout = () => {
    localStorage.setItem("cart", JSON.stringify(cart));
    navigate("/cart");
  };

  const filteredItems = menuItems.filter(item => 
    item.category === selectedCategory &&
    item.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <div className="bg-slate-800 p-4 flex items-center">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => navigate("/home")}
          className="text-orange-500 hover:text-orange-400"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Kiosk
        </Button>
        <span className="text-slate-400 ml-2">Self checkout</span>
      </div>

      <div className="flex h-[calc(100vh-80px)]">
        {/* Left Sidebar - Categories */}
        <div className="w-80 bg-slate-800 p-6">
          <h2 className="text-white text-xl font-semibold mb-6">Categories</h2>
          <div className="space-y-4">
            {categories.map(category => (
              <Button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                variant={selectedCategory === category.id ? "default" : "ghost"}
                className={`w-full p-4 h-auto justify-start ${
                  selectedCategory === category.id 
                    ? "bg-orange-500 hover:bg-orange-600 text-white" 
                    : "text-slate-400 hover:text-white hover:bg-slate-700"
                }`}
              >
                <span className="text-2xl mr-3">{category.icon}</span>
                <span className="text-lg">{category.name}</span>
              </Button>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6">
          <div className="mb-8">
            <h1 className="text-white text-3xl font-bold mb-6">
              What would you like to have today?
            </h1>
            
            {/* Search */}
            <div className="relative max-w-md">
              <Search className="absolute left-3 top-3 w-5 h-5 text-slate-400" />
              <Input
                type="text"
                placeholder="Search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-slate-800 border-slate-600 text-white placeholder-slate-400"
              />
            </div>
          </div>

          {/* Menu Items */}
          <div className="space-y-4">
            {filteredItems.map(item => (
              <div key={item.id} className="bg-slate-800 rounded-lg p-4 flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-16 bg-orange-500 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">🍜</span>
                  </div>
                  <div>
                    <h3 className="text-white text-xl font-semibold">{item.name}</h3>
                    <p className="text-slate-400 text-sm max-w-md">{item.description}</p>
                    <p className="text-orange-500 text-lg font-bold">${item.price.toFixed(2)}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  {cart[item.id] && (
                    <>
                      <Button
                        size="sm"
                        onClick={() => removeFromCart(item.id)}
                        className="w-10 h-10 rounded-full bg-orange-500 hover:bg-orange-600 text-white p-0"
                      >
                        -
                      </Button>
                      <span className="text-white font-semibold min-w-[20px] text-center">
                        {cart[item.id]}
                      </span>
                    </>
                  )}
                  <Button
                    size="sm"
                    onClick={() => addToCart(item.id)}
                    className="w-10 h-10 rounded-full bg-orange-500 hover:bg-orange-600 text-white p-0"
                  >
                    <Plus className="w-5 h-5" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Checkout Button */}
      {getTotalItems() > 0 && (
        <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2">
          <Button
            onClick={handleCheckout}
            className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 text-lg font-semibold rounded-full shadow-lg"
          >
            {getTotalItems()} ITEMS | ${getTotalPrice().toFixed(2)} CHECKOUT
          </Button>
        </div>
      )}
    </div>
  );
};

export default Menu;