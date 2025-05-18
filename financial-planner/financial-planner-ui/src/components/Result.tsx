import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { Box, Typography, Grid } from '@mui/material';
import type { GoalAnalysis, LLMPicks } from '../types/resultsTypes';
import SuggestedGoals from './SuggestedGoals';
import LLMPicks from './LLMPicks';
import GoalAnalysis from './GoalAnalysis';


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
        fetchGoalAnalysis();
      } catch (err) {
        console.error('Error fetching suggested goals:', err);
      } finally {
        setLoadingSuggestions(false);
      }
    };

    const fetchGoalAnalysis = async () => {
      try {
        const res = await api.post('/analyze', formData);
        setGoalAnalysis(res.data || null);
        console.log('Goal Analysis:', res.data);
        fetchLLMPicks();
      } catch (err) {
        console.error('Error fetching analysis:', err);
      } finally {
        setLoadingAnalysis(false);
      }
    };

    const fetchLLMPicks = async () => {
      try {
        const res = await api.post('/get_stock_recommendations/', formData);
        setLlmPicks(res.data.recommendations || null);
      } catch (err) {
        console.error('Error fetching LLM picks:', err);
      } finally {
        setLoadingLLM(false);
      }
    };

    fetchSuggestedGoals();
  }, [formData, navigate]);

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Personalized Financial Plan
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <SuggestedGoals goals={suggestedGoals} loading={loadingSuggestions} />
        </Grid>
        <Grid item xs={12} md={4}>
          <GoalAnalysis analysis={goalAnalysis} loading={loadingAnalysis} />
        </Grid>
        <Grid item xs={12} md={4}>
          <LLMPicks picks={llmPicks} loading={loadingLLM} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default ResultsPage;
