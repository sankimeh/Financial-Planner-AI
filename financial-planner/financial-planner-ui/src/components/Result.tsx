import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { Typography, CircularProgress, Grid, Box } from '@mui/material';

import GoalAnalysisCard from './GoalAnalysisCard';
import GoalSuggestions from './SuggestedGoals';
import type GoalAnalysis from './GoalAnalysis';
import type { LLMPicks } from '../types/resultsTypes';
import LLMPicksCard from './LLMPicks';

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
        <Grid item xs={12} md={4}>
          <GoalSuggestions
            suggestedGoals={suggestedGoals}
            loading={loadingSuggestions}
            renderLoader={renderLoader}
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <GoalAnalysisCard
            analysis={goalAnalysis}
            loading={loadingAnalysis}
            renderLoader={renderLoader}
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <LLMPicksCard
            picks={llmPicks}
            loading={loadingLLM}
            renderLoader={renderLoader}
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default ResultsPage;
