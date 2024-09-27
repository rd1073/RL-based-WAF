import React, { useEffect, useState } from 'react';
import { FaShieldAlt, FaExclamationTriangle, FaClipboardList } from 'react-icons/fa';
import './StatusDisplay.css'; // Ensure this CSS file is created for styles

const StatusDisplay = () => {
  const [status, setStatus] = useState({
    counts: { ddos: 0, sql: 0, xss: 0 },
    logs: [],
    settings: {
      ddos_detection_enabled: false,
      ddos_sensitivity_threshold: 0,
      ip_allowlist: [],
      ip_denylist: [],
      sql_detection_enabled: false,
      xss_detection_enabled: false,
    },
  });

  // Function to fetch the status from the backend
  const fetchStatus = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/status');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error('Error fetching status:', error);
    }
  };

  useEffect(() => {
    // Fetch status immediately on component mount
    fetchStatus();

    // Set up interval to fetch status every 5 seconds
    const intervalId = setInterval(() => {
      fetchStatus();
    }, 5000);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="status-display">
      <h1>Firewall Status</h1>

      <div className="card">
        <h2>
          <FaShieldAlt /> Attack Counts
        </h2>
        <div className="count-container">
          <div className="count-item">
            <span>DDoS Attacks:</span>
            <span className="count">{status.counts.ddos}</span>
          </div>
          <div className="count-item">
            <span>SQL Injection Attacks:</span>
            <span className="count">{status.counts.sql}</span>
          </div>
          <div className="count-item">
            <span>XSS Attacks:</span>
            <span className="count">{status.counts.xss}</span>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>
          <FaClipboardList /> Logs
        </h2>
        <div className="log-list">
          {status.logs.map((log, index) => (
            <div key={index} className="log-item">
              <strong>{log.time}</strong> - {log.type} - {log.action} from IP: {log.ip}
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h2>
          <FaExclamationTriangle /> Firewall Settings
        </h2>
        <div className="settings-list">
          <div className="settings-item">
            <span>DDoS Detection Enabled:</span>
            <span>{status.settings.ddos_detection_enabled ? 'Yes' : 'No'}</span>
          </div>
          <div className="settings-item">
            <span>DDoS Sensitivity Threshold:</span>
            <span>{status.settings.ddos_sensitivity_threshold}</span>
          </div>
          <div className="settings-item">
            <span>IP Allowlist:</span>
            <span>{status.settings.ip_allowlist.length > 0 ? status.settings.ip_allowlist.join(', ') : 'None'}</span>
          </div>
          <div className="settings-item">
            <span>IP Denylist:</span>
            <span>{status.settings.ip_denylist.length > 0 ? status.settings.ip_denylist.join(', ') : 'None'}</span>
          </div>
          <div className="settings-item">
            <span>SQL Detection Enabled:</span>
            <span>{status.settings.sql_detection_enabled ? 'Yes' : 'No'}</span>
          </div>
          <div className="settings-item">
            <span>XSS Detection Enabled:</span>
            <span>{status.settings.xss_detection_enabled ? 'Yes' : 'No'}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatusDisplay;
