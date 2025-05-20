import React, { useState } from 'react';
import {
  Card, CardContent, Typography, Tabs, Tab, Grid, Chip, Box, Divider
} from '@mui/material';
import { TrendingUp, AttachMoney, EmojiEvents } from '@mui/icons-material';
import type { LLMPicks } from '../types/resultsTypes';

interface Props {
  picks: LLMPicks | null;
  loading: boolean;
  renderLoader: () => JSX.Element;
}

const categoryIcons = {
  equity: <TrendingUp color="primary" />,
  bond: <AttachMoney color="secondary" />,
  commodity: <EmojiEvents sx={{ color: '#d4af37' }} />,
};

const LLMPicksCard: React.FC<Props> = ({ picks, loading, renderLoader }) => {
  const [tabIndex, setTabIndex] = useState(0);

  const handleTabChange = (_: any, newValue: number) => setTabIndex(newValue);

  const categories = [
    { key: 'equity_picks', label: 'Equity', icon: categoryIcons.equity },
    { key: 'bond_picks', label: 'Bonds', icon: categoryIcons.bond },
    { key: 'commodity_picks', label: 'Commodities', icon: categoryIcons.commodity },
  ];

  const renderItems = (items: typeof picks.equity_picks) => (
    <Grid container spacing={2} mt={1}>
      {items?.map((item, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <Card variant="outlined" sx={{ borderRadius: 3, p: 2, boxShadow: 1 }}>
            <Typography variant="subtitle1" fontWeight="bold">{item.ticker} - {item.name}</Typography>
            <Chip label={item.horizon} variant="outlined" size="small" sx={{ mt: 1, mb: 1 }} />
            <Typography variant="body2" color="text.secondary">{item.reason}</Typography>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  return (
    <Card sx={{ borderRadius: 4, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>🔍 Top Investment Picks (LLM)</Typography>
        {loading ? (
          renderLoader()
        ) : picks ? (
          <>
            <Tabs value={tabIndex} onChange={handleTabChange} variant="fullWidth" sx={{ mb: 2 }}>
              {categories.map((cat, i) => (
                <Tab key={cat.key} label={
                  <Box display="flex" alignItems="center" gap={1}>
                    {cat.icon} {cat.label}
                  </Box>
                } />
              ))}
            </Tabs>
            <Divider />
            <Box mt={2}>
              {tabIndex === 0 && renderItems(picks.equity_picks)}
              {tabIndex === 1 && renderItems(picks.bond_picks)}
              {tabIndex === 2 && renderItems(picks.commodity_picks)}
            </Box>
          </>
        ) : (
          <Typography color="error">⚠️ Failed to load recommendations.</Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default LLMPicksCard;