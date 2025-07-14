import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Plus, Minus } from "lucide-react";

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  size: string;
  addons: string[];
}

interface AddOn {
  id: string;
  name: string;
  price: number;
}

const addOns: AddOn[] = [
  { id: "pepsi", name: "Pepsi", price: 3.00 },
  { id: "fries", name: "Fries", price: 5.00 },
  { id: "sauce", name: "Sauce", price: 8.00 },
  { id: "cocacola", name: "CocaCola", price: 8.00 }
];

const Cart = () => {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [selectedAddOns, setSelectedAddOns] = useState<{[key: string]: number}>({});

  useEffect(() => {
    const savedCart = localStorage.getItem("cart");
    if (savedCart) {
      const cart = JSON.parse(savedCart);
      // Convert to cart items format
      const items: CartItem[] = [];
      Object.entries(cart).forEach(([itemId, quantity]) => {
        if (itemId === "2") { // Ramen
          items.push({
            id: itemId,
            name: "Ramen",
            price: 13.80,
            quantity: quantity as number,
            size: "Large",
            addons: ["Beef", "Chilly Sauce x1", "Chilly flakes x1"]
          });
        }
      });
      setCartItems(items);
    }
  }, []);

  const updateAddOn = (addOnId: string, change: number) => {
    setSelectedAddOns(prev => ({
      ...prev,
      [addOnId]: Math.max(0, (prev[addOnId] || 0) + change)
    }));
  };

  const getSubtotal = () => {
    const itemsTotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const addOnsTotal = Object.entries(selectedAddOns).reduce((sum, [addOnId, quantity]) => {
      const addOn = addOns.find(ao => ao.id === addOnId);
      return sum + (addOn ? addOn.price * quantity : 0);
    }, 0);
    return itemsTotal + addOnsTotal;
  };

  const getDiscount = () => 2.00;
  const getTaxAndFees = () => 0.50;
  const getTotal = () => getSubtotal() - getDiscount() + getTaxAndFees();

  const handleCheckout = () => {
    const orderData = {
      items: cartItems,
      addOns: selectedAddOns,
      subtotal: getSubtotal(),
      discount: getDiscount(),
      taxAndFees: getTaxAndFees(),
      total: getTotal()
    };
    localStorage.setItem("orderData", JSON.stringify(orderData));
    navigate("/payment");
  };

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <div className="bg-slate-800 p-4 flex items-center justify-center">
        <h1 className="text-white text-2xl font-bold">Cart Details</h1>
      </div>

      <div className="p-6 max-w-4xl mx-auto">
        {/* Order Icon */}
        <div className="flex justify-center mb-8">
          <div className="w-16 h-16 bg-orange-500 rounded-lg flex items-center justify-center">
            <span className="text-white text-2xl">📦</span>
          </div>
        </div>

        {/* Cart Items */}
        <div className="space-y-6">
          {cartItems.map(item => (
            <div key={item.id} className="bg-slate-800 rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-16 bg-orange-500 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">🍜</span>
                  </div>
                  <div>
                    <h3 className="text-white text-xl font-semibold">{item.name}</h3>
                    <p className="text-slate-400">{item.size} • {item.addons.join(" • ")}</p>
                    <p className="text-orange-500 text-lg font-bold">${item.price.toFixed(2)}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <Button
                    variant="outline"
                    className="text-slate-400 border-slate-600 hover:text-white hover:border-slate-400"
                  >
                    EDIT
                  </Button>
                  <div className="flex items-center space-x-3">
                    <Button
                      size="sm"
                      className="w-10 h-10 rounded-full bg-orange-500 hover:bg-orange-600 text-white p-0"
                    >
                      <Minus className="w-4 h-4" />
                    </Button>
                    <span className="text-white font-semibold text-xl">{item.quantity}</span>
                    <Button
                      size="sm"
                      className="w-10 h-10 rounded-full bg-orange-500 hover:bg-orange-600 text-white p-0"
                    >
                      <Plus className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Add more items */}
          <div className="border-2 border-dashed border-slate-600 rounded-lg p-6 text-center">
            <Button
              variant="ghost"
              className="text-slate-400 hover:text-white"
              onClick={() => navigate("/menu")}
            >
              <Plus className="w-5 h-5 mr-2" />
              Add more items
            </Button>
          </div>
        </div>

        {/* Add-ons */}
        <div className="mt-8">
          <h2 className="text-white text-xl font-semibold mb-6">ADD-ONS</h2>
          <div className="grid grid-cols-2 gap-4">
            {addOns.map(addOn => (
              <div key={addOn.id} className="bg-slate-800 rounded-lg p-6 text-center">
                <h3 className="text-white text-lg font-semibold mb-2">{addOn.name}</h3>
                <p className="text-orange-500 text-lg font-bold mb-4">${addOn.price.toFixed(2)}</p>
                <div className="flex items-center justify-center space-x-3">
                  <Button
                    size="sm"
                    onClick={() => updateAddOn(addOn.id, -1)}
                    className="w-10 h-10 rounded-full bg-orange-500 hover:bg-orange-600 text-white p-0"
                  >
                    <Minus className="w-4 h-4" />
                  </Button>
                  <span className="text-white font-semibeld text-xl min-w-[20px] text-center">
                    {selectedAddOns[addOn.id] || 0}
                  </span>
                  <Button
                    size="sm"
                    onClick={() => updateAddOn(addOn.id, 1)}
                    className="w-10 h-10 rounded-full bg-orange-500 hover:bg-orange-600 text-white p-0"
                  >
                    <Plus className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bill Details */}
        <div className="mt-8 bg-slate-800 rounded-lg p-6">
          <h2 className="text-white text-xl font-semibold mb-6">BILL DETAILS</h2>
          <div className="space-y-4">
            <div className="flex justify-between text-slate-400">
              <span>Total</span>
              <span>${getSubtotal().toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-green-400">
              <span>Discounts</span>
              <span>-${getDiscount().toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Tax and fees</span>
              <span>${getTaxAndFees().toFixed(2)}</span>
            </div>
            <div className="border-t border-slate-600 pt-4">
              <div className="flex justify-between text-white text-lg font-semibold">
                <span>To pay</span>
                <span className="text-orange-500">${getTotal().toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Checkout Button */}
        <div className="mt-8">
          <Button
            onClick={handleCheckout}
            className="w-full bg-orange-500 hover:bg-orange-600 text-white py-4 text-lg font-semibold rounded-lg"
          >
            1 ITEMS | ${getTotal().toFixed(2)} CHECKOUT
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

export default Cart;