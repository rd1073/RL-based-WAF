import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import { ToastContainer, toast , Slide} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './toastStyles.css'; // Import the custom styles


const SOCKET_SERVER_URL = 'http://127.0.0.1:5000'; // Ensure this URL is correct

const RealTimeMessage = () => {
  //const [message, setMessage] = useState('');

  useEffect(() => {
    // Establish socket connection to Flask backend
    const socket = io(SOCKET_SERVER_URL);

    // Listen for successful connection
    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    // Listen for error in connection
    socket.on('connect_error', (error) => {
      console.error('Connection Error:', error);
    });

    // Listen for messages from Flask backend
    socket.on('response_message', (data) => {
      console.log('Received message:', data);
      //setMessage(data.message);
      toast.info(data.message, {
        position: "top-center", // Centralize the notification
        className: "custom-toast", // Use the custom CSS class for styling
        bodyClassName: "custom-toast-body", // Style the body separately
        hideProgressBar: false, // Hide the progress bar for a cleaner look
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        autoClose: 5000, // Keep the notification visible for 8 seconds
        transition: Slide, // Use a slide-in animation
      });
    });

    // Clean up the socket connection on component unmount
    return () => {
      console.log('Disconnecting from WebSocket server');
      socket.disconnect();
    };
  }, []);

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
    <h1>Real-Time Firewall Alerts</h1>
    <ToastContainer
      limit={1} // Only show one notification at a time
      closeButton={true} // Show a close button on the notification
      style={{ width: '600px', marginTop: '200px' }} // Custom container styling
    />
  </div>
  );
};

export default RealTimeMessage;
