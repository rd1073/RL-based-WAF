import React from 'react';
import { Table, TableBody, TableCell, TableHead, TableRow, Paper, Typography } from '@mui/material';

const AttackTable = ({ logs }) => {
  return (
    <Paper elevation={3}>
      <Typography variant="h6" align="center" style={{ padding: '20px' }}>Attack Logs</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Time</TableCell>
            <TableCell>Type</TableCell>
            <TableCell>IP Address</TableCell>
            <TableCell>Action Taken</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {logs.map((log, index) => (
            <TableRow key={index}>
              <TableCell>{log.time}</TableCell>
              <TableCell>{log.type}</TableCell>
              <TableCell>{log.ip}</TableCell>
              <TableCell>{log.action}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
};

export default AttackTable;
