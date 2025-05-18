import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/axios'; // Removed .ts
import {
  Typography, CircularProgress, Grid, Box, Card, CardContent
} from '@mui/material';

interface Allocation {
  equity: number;
  bonds: number;
  commodities: number;
}

interface GoalAnalysis {
  monthly_surplus: number;
  emergency_fund_ok: boolean;
  ideal_emergency_fund: number;
  recommended_allocation: Allocation;
}

interface PickItem {
  ticker: string;
  name: string;
  horizon: string;
  reason: string;
}

interface LLMPicks {
  summary: string;
  equity_picks?: PickItem[];
  bond_picks?: PickItem[];
  commodity_picks?: PickItem[];
}

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const formData = location.state;

  const [suggestedGoals, setSuggestedGoals] = useState<string[]>([]);
  const [goalAnalysis, setGoalAnalysis] = useState<GoalAnalysis | null>(null);
  const [llmPicks, setLlmPicks] = useState<LLMPicks | null>(null);

  const [loadingSuggestions, setLoadingSuggestions] = useState(true);
  const [loadingAnalysis, setLoadingAnalysis] = useState(true);
  const [loadingLLM, setLoadingLLM] = useState(true);

  useEffect(() => {
    if (!formData) {
      navigate('/');
      return;
    }

    const fetchSuggestedGoals = async () => {
      try {
        const res = await api.post('/suggest-goals/', formData);
        setSuggestedGoals(res.data.suggested_goals || []);
      } catch (err) {
        console.error('Error fetching suggested goals:', err);
      } finally {
        setLoadingSuggestions(false);
      }
    };

    const fetchGoalAnalysis = async () => {
      try {
        const res = await api.post('/analyze', formData);
        console.log('Analysis response:', res.data);
        setGoalAnalysis(res.data || null);
      } catch (err) {
        console.error('Error fetching analysis:', err);
      } finally {
        setLoadingAnalysis(false);
      }
    };

    const fetchLLMPicks = async () => {
      try {
        const res = await api.post('/get_stock_recommendations/', formData);
        console.log('LLM picks response:', res.data);
        setLlmPicks(res.data.recommendations || null);
      } catch (err) {
        console.error('Error fetching LLM picks:', err);
      } finally {
        setLoadingLLM(false);
      }
    };

    fetchSuggestedGoals();
    fetchGoalAnalysis();
    fetchLLMPicks();
  }, [formData, navigate]);

  const renderLoader = () => (
    <Box display="flex" justifyContent="center" alignItems="center" p={4}>
      <CircularProgress />
    </Box>
  );

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Personalized Financial Plan
      </Typography>

      <Grid container spacing={3}>
        {/* Suggested Goals */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Suggested Goals</Typography>
              {loadingSuggestions ? renderLoader() : (
                <ul>
                  {suggestedGoals.map((goal, i) => (
                    <li key={i}>{goal}</li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Goal Analysis */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Goal Analysis & Portfolio</Typography>
              {loadingAnalysis ? renderLoader() : goalAnalysis ? (
                <>
                  <Typography>Monthly Surplus: ₹{goalAnalysis.monthly_surplus}</Typography>
                  <Typography>
                    Emergency Fund OK: {goalAnalysis.emergency_fund_ok ? 'Yes' : 'No'}
                  </Typography>
                  <Typography>Ideal Emergency Fund: ₹{goalAnalysis.ideal_emergency_fund}</Typography>
                  <Typography>Recommended Allocation:</Typography>
                  <ul>
                    <li>Equity: {goalAnalysis.recommended_allocation?.equity}%</li>
                    <li>Bonds: {goalAnalysis.recommended_allocation?.bonds}%</li>
                    <li>Commodities: {goalAnalysis.recommended_allocation?.commodities}%</li>
                  </ul>
                </>
              ) : (
                <Typography color="error">Failed to load analysis.</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* LLM Picks */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Top Picks (LLM)</Typography>
              {loadingLLM ? renderLoader() : llmPicks ? (
                <>
                  <Typography>{llmPicks.summary}</Typography>

                  {llmPicks.equity_picks?.length > 0 && (
                    <>
                      <Typography variant="subtitle1">Equity:</Typography>
                      <ul>
                        {llmPicks.equity_picks.map((item, i) => (
                          <li key={i}>{item.ticker} - {item.name} ({item.horizon}): {item.reason}</li>
                        ))}
                      </ul>
                    </>
                  )}

                  {llmPicks.bond_picks?.length > 0 && (
                    <>
                      <Typography variant="subtitle1">Bonds:</Typography>
                      <ul>
                        {llmPicks.bond_picks.map((item, i) => (
                          <li key={i}>{item.ticker} - {item.name} ({item.horizon}): {item.reason}</li>
                        ))}
                      </ul>
                    </>
                  )}

                  {llmPicks.commodity_picks?.length > 0 && (
                    <>
                      <Typography variant="subtitle1">Commodities:</Typography>
                      <ul>
                        {llmPicks.commodity_picks.map((item, i) => (
                          <li key={i}>{item.ticker} - {item.name} ({item.horizon}): {item.reason}</li>
                        ))}
                      </ul>
                    </>
                  )}
                </>
              ) : (
                <Typography color="error">Failed to load recommendations.</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ResultsPage;
