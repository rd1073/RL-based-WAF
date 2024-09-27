import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const SOCKET_SERVER_URL = 'http://127.0.0.1:5000'; // Ensure this URL is correct

const RealTimeMessage = () => {
  const [message, setMessage] = useState('');

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
      setMessage(data.message);
    });

    // Clean up the socket connection on component unmount
    return () => {
      console.log('Disconnecting from WebSocket server');
      socket.disconnect();
    };
  }, []);

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>Real-Time Message from Flask:</h1>
      <h2>{message ? message : 'No message received yet'}</h2>
    </div>
  );
};

export default RealTimeMessage;
