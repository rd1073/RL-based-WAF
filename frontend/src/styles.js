import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
  root: {
    display: 'flex',
    height: '100vh',
  },
  sidebar: {
    width: '250px',
    backgroundColor: '#282c34',
    color: '#ffffff',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
  },
  content: {
    flexGrow: 1,
    padding: '20px',
    backgroundColor: '#f4f4f4',
  },
  navItem: {
    margin: '10px 0',
    cursor: 'pointer',
    '&:hover': {
      backgroundColor: '#3c4043',
      borderRadius: '5px',
    },
  },
  card: {
    padding: '20px',
    margin: '20px',
    textAlign: 'center',
  },
});

export default useStyles;
