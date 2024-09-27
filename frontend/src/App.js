// App.js
import React, { useState } from 'react';
import Notification from './components/Notification';
import RealTimeMessage from './components/Notification';
import StatusDisplay from './components/Status';

const App = () => {
    
    return (
        <div>
          <RealTimeMessage />
          <StatusDisplay />
        </div>
    );
};

export default App;
