import { Box, Button, Container, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function Hero() {
  const navigate = useNavigate();
  return (
    <Box
      sx={{
        height: '100vh',
        backgroundImage: `linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        color: '#fff',
        textAlign: 'center',
        px: 2,
      }}
    >
      <Container maxWidth="md">
        <Typography
          variant="h2"
          fontWeight="bold"
          sx={{ textShadow: '2px 2px 6px rgba(0,0,0,0.6)' }}
          gutterBottom
        >
          Let’s Make You
        </Typography>
        <Typography
          variant="h2"
          color="primary.light"
          sx={{ textShadow: '2px 2px 6px rgba(0,0,0,0.6)' }}
          gutterBottom
        >
          Financially Independent
        </Typography>
        <Button
      variant="contained"
      size="large"
      sx={{
        mt: 4,
        px: 5,
        py: 1.5,
        fontSize: '1.2rem',
        fontWeight: 600,
        borderRadius: '999px',
        boxShadow: 3,
      }}
      onClick={() => navigate("/plan")}
    >
      Get Started
    </Button>
      </Container>
    </Box>
  );
}
