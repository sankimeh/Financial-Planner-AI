import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Container,
  Button,
  CircularProgress,
} from '@mui/material';
import { fetchFinancialNews } from '../api/newsAPI';

interface NewsItem {
  title: string;
  image_url?: string;
  description: string;
  link: string;
}

export default function NewsSection() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFinancialNews()
      .then((articles) => {
        setNews(articles.slice(0, 6));
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Box
      sx={{
        py: 10,
        px: 2,
        backgroundColor: '#f6f9fc', // Calm background
      }}
    >
      <Container maxWidth="lg">
        <Typography
          variant="h4"
          gutterBottom
          align="center"
          sx={{
            fontWeight: 'bold',
            mb: 6,
            color: 'primary.main',
            textShadow: '1px 1px rgba(0,0,0,0.05)',
          }}
        >
          📈 Latest Financial News
        </Typography>

        {loading ? (
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={4}>
            {news.map((item, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    borderRadius: 3,
                    boxShadow: 3,
                    transition: 'transform 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                    },
                  }}
                >
                  {item.image_url && (
                    <CardMedia
                      component="img"
                      height="160"
                      image={item.image_url}
                      alt={item.title}
                    />
                  )}
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography
                      variant="h6"
                      gutterBottom
                      sx={{ fontWeight: 600 }}
                    >
                      {item.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {item.description?.slice(0, 120)}...
                    </Typography>
                    <Button
                      size="small"
                      href={item.link}
                      target="_blank"
                      sx={{ mt: 2, textTransform: 'none' }}
                    >
                      Read More →
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Container>
    </Box>
  );
}
