import React, { useEffect, useState } from 'react';
import { Snackbar, Alert } from '@mui/material';

const Notification = ({ message }) => {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (message) setOpen(true);
  }, [message]);

  const handleClose = () => setOpen(false);

  return (
    <Snackbar open={open} autoHideDuration={3000} onClose={handleClose}>
      <Alert onClose={handleClose} severity="warning">
        {message}
      </Alert>
    </Snackbar>
  );
};

export default Notification;
