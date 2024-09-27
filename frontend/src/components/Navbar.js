import React from 'react';
import useStyles from '../styles';
import { Typography } from '@mui/material';

const Navbar = ({ onMenuSelect }) => {
  const classes = useStyles();

  return (
    <div className={classes.sidebar}>
      <Typography variant="h5" gutterBottom>Firewall Dashboard</Typography>
      <div className={classes.navItem} onClick={() => onMenuSelect('home')}>
        Home
      </div>
      <div className={classes.navItem} onClick={() => onMenuSelect('status')}>
        System Status
      </div>
      <div className={classes.navItem} onClick={() => onMenuSelect('attacks')}>
        Attack Logs
      </div>
      <div className={classes.navItem} onClick={() => onMenuSelect('settings')}>
        Settings
      </div>
    </div>
  );
};

export default Navbar;
