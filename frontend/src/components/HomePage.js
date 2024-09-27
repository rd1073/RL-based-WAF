// AttackLogs.js
import React, { useState, useEffect } from 'react';

const AttackLogs = () => {
  const [attackCounts, setAttackCounts] = useState({ sql: 0, xss: 0, ddos: 0 });
  const [attackLogs, setAttackLogs] = useState([]);

  // Fetch the status and logs from the backend
  const fetchAttackData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/status');
      const data = await response.json();

      setAttackCounts(data.counts);
      setAttackLogs(data.logs);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  // Fetch data when the component loads
  useEffect(() => {
    fetchAttackData();
  }, []);

  return (
    <div>
      {/* Attack Count Overview */}
      <div className="attack-counters">
        <h2>Attack Counts</h2>
        <div>
          <p><strong>SQL Injection Attacks:</strong> {attackCounts.sql}</p>
          <p><strong>XSS Attacks:</strong> {attackCounts.xss}</p>
          <p><strong>DDoS Attacks:</strong> {attackCounts.ddos}</p>
        </div>
      </div>

      {/* Attack Logs */}
      <div className="attack-log">
        <h2>Attack Logs</h2>
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Type</th>
              <th>Source IP</th>
              <th>Action Taken</th>
            </tr>
          </thead>
          <tbody>
            {attackLogs.map((log, index) => (
              <tr key={index}>
                <td>{log.time}</td>
                <td>{log.type}</td>
                <td>{log.ip}</td>
                <td>{log.action}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AttackLogs;
