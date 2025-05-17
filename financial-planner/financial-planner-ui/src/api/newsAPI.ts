import axios from 'axios';

const API_KEY = 'pub_87605705ed7ca814e3220ece3bf6fc33596fe'; // <-- Replace with your actual key

export const fetchFinancialNews = async () => {
  const response = await axios.get('https://newsdata.io/api/1/news', {
    params: {
      apikey: API_KEY,
      category: 'business',
      language: 'en',
      country: 'us',
    },
  });

  return response.data.results || [];
};
