import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { ArrowRight, CreditCard, Banknote, Utensils } from "lucide-react";

interface PaymentOption {
  id: string;
  name: string;
  icon: JSX.Element;
  amount: string;
}

const Payment = () => {
  const navigate = useNavigate();
  const [orderTotal, setOrderTotal] = useState(13.80);
  const [selectedPayment, setSelectedPayment] = useState("");

  useEffect(() => {
    const orderData = localStorage.getItem("orderData");
    if (orderData) {
      const data = JSON.parse(orderData);
      setOrderTotal(data.total);
    }
  }, []);

  const paymentOptions: PaymentOption[] = [
    {
      id: "credit",
      name: "Credit",
      icon: <CreditCard className="w-6 h-6 text-blue-500" />,
      amount: `$${orderTotal.toFixed(2)}`
    },
    {
      id: "debit",
      name: "Debit",
      icon: <CreditCard className="w-6 h-6 text-purple-500" />,
      amount: `$${orderTotal.toFixed(2)}`
    }
  ];

  const handlePayment = async () => {
    if (selectedPayment) {
      // Save payment details for receipt
      const paymentData = {
        amount: orderTotal,
        method: selectedPayment,
        timestamp: new Date().toISOString()
      };
      localStorage.setItem("paymentData", JSON.stringify(paymentData));

      // Gather all data for backend
      let user = JSON.parse(localStorage.getItem("personalData") || '{}');
      
      // Debug: Log what we're reading from localStorage
      console.log("Personal data from localStorage:", localStorage.getItem("personalData"));
      console.log("Parsed user data:", user);
      
      // Ensure we have valid user data
      if (!user.name || user.name === "Test User") {
        user.name = localStorage.getItem("userName") || "Guest";
        console.log("Using userName from localStorage:", user.name);
      }
      if (!user.phone || user.phone === "1234567890") {
        user.phone = localStorage.getItem("userPhone") || "";
        console.log("Using userPhone from localStorage:", user.phone);
      }
      
      // Debug: Log final user data
      console.log("Final user data being sent:", user);

      // Fix order/addOns structure
      let order = JSON.parse(localStorage.getItem("orderData") || '{}');
      
      // Ensure order.items is an array of objects with id, name, quantity, price
      if (order.items && Array.isArray(order.items)) {
        order.items = order.items.map(item => ({
          id: item.id,
          name: item.name,
          quantity: item.quantity,
          price: item.price
        }));
      } else {
        order.items = [];
      }
      
      // Convert addOns from {id: quantity} to array of objects
      if (order.addOns && typeof order.addOns === 'object' && !Array.isArray(order.addOns)) {
        const addOnDefs = [
          { id: "pepsi", name: "Pepsi", price: 3.00 },
          { id: "fries", name: "Fries", price: 5.00 },
          { id: "sauce", name: "Sauce", price: 8.00 },
          { id: "cocacola", name: "CocaCola", price: 8.00 }
        ];
        order.addOns = Object.entries(order.addOns)
          .filter(([id, quantity]) => Number(quantity) > 0)
          .map(([id, quantity]) => {
            const def = addOnDefs.find(a => a.id === id) || { id, name: id, price: 0 };
            return {
              id,
              name: def.name,
              quantity: Number(quantity),
              price: def.price
            };
          });
      } else if (!Array.isArray(order.addOns)) {
        order.addOns = [];
      }

      let seatNumber = localStorage.getItem("seatNumber");
      let orderType = localStorage.getItem("orderType");
      
      // Set default values if not present (for testing)
      if (!orderType) {
        orderType = "Pick Up"; // Default to Pick Up
        localStorage.setItem("orderType", orderType);
      }
      
      // Only include seatNumber for Dine In
      if (orderType !== 'Dine In') {
        seatNumber = null;
      } else if (!seatNumber) {
        seatNumber = "A1"; // Default seat for Dine In
        localStorage.setItem("seatNumber", seatNumber);
      }
      
      // Prepare the order data in the correct structure for backend
      const orderData = {
        items: order.items,
        addOns: order.addOns,
        total: orderTotal,
        orderType: orderType,
        seatNumber: seatNumber
      };
      
      const payload = { 
        user, 
        order: orderData, 
        paymentTime: new Date().toISOString()
      };
      
      console.log("Sending payment data to backend");

      try {
        const res = await fetch("/api/order/transaction", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        
        if (res.ok) {
          navigate("/confirmation");
        } else {
          alert("Failed to save transaction. Please try again.");
        }
      } catch (err) {
        alert("Error connecting to backend.");
      }
    }
  };



  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Bill Details */}
        <div className="bg-slate-800 rounded-lg p-6 mb-8">
          <h2 className="text-white text-xl font-semibold mb-6">BILL DETAILS</h2>
          <div className="space-y-4">
            <div className="flex justify-between text-slate-400">
              <span>Sub Total</span>
              <span>${orderTotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-white text-lg font-semibold">
              <span>Due Amount</span>
              <span>${orderTotal.toFixed(2)}</span>
            </div>
          </div>
        </div>

        <div className="text-center mb-8">
          <p className="text-slate-400">
            You can choose any payment mode and proceed to pay. You can split the bill using 'Split' mode.
          </p>
        </div>

        {/* Payment Options */}
        <div className="space-y-4 mb-8">
          {paymentOptions.map(option => (
            <Button
              key={option.id}
              onClick={() => setSelectedPayment(option.id)}
              variant="ghost"
              className={`w-full p-4 h-auto justify-between text-left ${
                selectedPayment === option.id
                  ? "bg-slate-700 border border-orange-500"
                  : "bg-slate-800 hover:bg-slate-700"
              }`}
            >
              <div className="flex items-center space-x-3">
                {option.icon}
                <span className="text-white text-lg">{option.name}</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-white font-semibold">{option.amount}</span>
                <ArrowRight className="w-5 h-5 text-slate-400" />
              </div>
            </Button>
          ))}
        </div>

        {/* Pay Button */}
        <Button
          onClick={handlePayment}
          disabled={!selectedPayment}
          className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-slate-600 text-white py-4 text-lg font-semibold rounded-lg"
        >
          PAY ${orderTotal.toFixed(2)}
        </Button>
        
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

export default Payment;