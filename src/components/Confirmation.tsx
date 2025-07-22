import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { Printer } from "lucide-react";

const Confirmation = () => {
  const navigate = useNavigate();
  const [countdown, setCountdown] = useState(10);
  const [orderData, setOrderData] = useState<any>(null);

  useEffect(() => {
    // Load order data from localStorage
    const savedOrderData = localStorage.getItem("orderData");
    const savedCart = localStorage.getItem("cart");
    const customerName = localStorage.getItem("userName"); // Changed from customerName to userName
    const seatNumber = localStorage.getItem("seatNumber");
    const orderType = localStorage.getItem("orderType");
    const paymentData = localStorage.getItem("paymentData");
    
    if (savedOrderData) {
      const data = JSON.parse(savedOrderData);
      setOrderData({
        ...data,
        cart: savedCart ? JSON.parse(savedCart) : {},
        customerName: customerName || "Guest",
        seatNumber: seatNumber || "N/A",
        orderType: orderType || "Pick Up",
        payment: paymentData ? JSON.parse(paymentData) : null
      });
    } else {
      setOrderData({
        cart: savedCart ? JSON.parse(savedCart) : {},
        customerName: customerName || "Guest",
        seatNumber: seatNumber || "N/A",
        orderType: orderType || "Pick Up",
        payment: paymentData ? JSON.parse(paymentData) : null
      });
    }

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

  const handlePrintReceipt = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;

    const menuItems = [
      { id: "1", name: "Udon", price: 13.80 },
      { id: "2", name: "Ramen", price: 13.80 },
      { id: "3", name: "Pad Thai", price: 13.80 },
      { id: "4", name: "Spaghetti Bolognese", price: 13.80 },
      { id: "5", name: "Pho", price: 13.80 }
    ];

    let orderItems = '';
    
    // Use payment amount instead of recalculating
    const total = orderData?.payment?.amount || 0;
    const discount = orderData?.discount || 0;
    const subtotal = total / 1.1; // Remove GST to get subtotal
    const tax = total - subtotal;
    
    if (orderData?.cart) {
      Object.entries(orderData.cart).forEach(([itemId, quantity]: [string, any]) => {
        const menuItem = menuItems.find(item => item.id === itemId);
        if (menuItem) {
          const itemTotal = menuItem.price * quantity;
          orderItems += `
            <tr>
              <td style="padding: 8px 0;">${menuItem.name}</td>
              <td style="text-align: center;">${quantity}</td>
              <td style="text-align: right;">$${menuItem.price.toFixed(2)}</td>
              <td style="text-align: right;">$${itemTotal.toFixed(2)}</td>
            </tr>
          `;
        }
      });
    }

    const receiptHTML = `
      <!DOCTYPE html>
      <html>
        <head>
          <title>Receipt</title>
          <style>
            body {
              font-family: 'Courier New', monospace;
              max-width: 400px;
              margin: 0 auto;
              padding: 20px;
              background: white;
            }
            .header {
              text-align: center;
              border-bottom: 2px solid #000;
              padding-bottom: 10px;
              margin-bottom: 20px;
            }
            .order-info {
              margin-bottom: 20px;
            }
            table {
              width: 100%;
              border-collapse: collapse;
            }
            .totals {
              border-top: 1px solid #000;
              margin-top: 10px;
              padding-top: 10px;
            }
            .total-line {
              font-weight: bold;
              border-top: 2px solid #000;
              border-bottom: 2px solid #000;
            }
            @media print {
              body { margin: 0; padding: 10px; }
            }
          </style>
        </head>
        <body>
          <div class="header">
            <h2>NOVA RESTAURANT</h2>
            <p>Order Receipt</p>
          </div>
          
          <div class="order-info">
            <p><strong>Customer:</strong> ${orderData?.customerName || 'Guest'}</p>
            ${orderData?.orderType === 'Dine In' ? `<p><strong>Seat Number:</strong> ${orderData?.seatNumber || 'N/A'}</p>` : ''}
            <p><strong>Date:</strong> ${new Date().toLocaleDateString()}</p>
            <p><strong>Time:</strong> ${new Date().toLocaleTimeString()}</p>
            <p><strong>Order Type:</strong> ${orderData?.orderType || 'Pick Up'}</p>
          </div>

          <table>
            <thead>
              <tr style="border-bottom: 1px solid #000;">
                <th style="text-align: left; padding: 8px 0;">Item</th>
                <th style="text-align: center; padding: 8px 0;">Qty</th>
                <th style="text-align: right; padding: 8px 0;">Price</th>
                <th style="text-align: right; padding: 8px 0;">Total</th>
              </tr>
            </thead>
            <tbody>
              ${orderItems}
            </tbody>
          </table>

          <div class="totals">
            <table>
              <tr>
                <td>Subtotal:</td>
                <td style="text-align: right;">$${subtotal.toFixed(2)}</td>
              </tr>
              <tr>
                <td>Discount:</td>
                <td style="text-align: right;">-$${discount.toFixed(2)}</td>
              </tr>
              <tr>
                <td>Tax (10%):</td>
                <td style="text-align: right;">$${tax.toFixed(2)}</td>
              </tr>
              <tr class="total-line">
                <td><strong>TOTAL:</strong></td>
                <td style="text-align: right;"><strong>$${total.toFixed(2)}</strong></td>
              </tr>
            </tbody>
          </div>

          <div style="text-align: center; margin-top: 30px; border-top: 1px solid #000; padding-top: 10px;">
            <p>Thank you for dining with us!</p>
            <p style="font-size: 12px;">Powered by NOVA</p>
          </div>
        </body>
      </html>
    `;

    printWindow.document.write(receiptHTML);
    printWindow.document.close();
    printWindow.print();
  };

  const handleStartNewOrder = () => {
    // Clear all stored data
    localStorage.removeItem("cart");
    localStorage.removeItem("orderData");
    localStorage.removeItem("personalData");
    localStorage.removeItem("userName");
    localStorage.removeItem("userPhone");
    localStorage.removeItem("seatNumber");
    localStorage.removeItem("orderType");
    localStorage.removeItem("paymentData");
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

        <div className="space-y-4 mb-8 max-w-md mx-auto">
          <Button
            onClick={handlePrintReceipt}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 text-lg font-semibold rounded-lg flex items-center justify-center gap-2"
          >
            <Printer size={20} />
            Print Receipt
          </Button>
          
          <Button
            onClick={handleStartNewOrder}
            className="w-full bg-orange-500 hover:bg-orange-600 text-white py-4 text-lg font-semibold rounded-lg"
          >
            Start New Order
          </Button>
        </div>

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