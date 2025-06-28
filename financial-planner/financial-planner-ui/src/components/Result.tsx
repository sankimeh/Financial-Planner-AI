import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import {
  Typography,
  CircularProgress,
  Grid,
  Box,
  Divider,
  Fade,
  Paper,
} from '@mui/material';

import GoalAnalysisCard from './GoalAnalysisCard';
import GoalSuggestions from './SuggestedGoals';
import type GoalAnalysis from './GoalAnalysis';
import type { LLMPicks } from '../types/resultsTypes';
import LLMPicksCard from './LLMPicks';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const formData = location.state;
  const [suggestedGoals, setSuggestedGoals] = useState<{ goal: string; reason: string }[]>([]);
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
        const suggested = res.data.suggested_goals || [];

        // Each item has shape: { goal: string, reason: string }
        setSuggestedGoals(suggested);

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

  useEffect(() => {
    console.log("Analysis data:", goalAnalysis);}
  , [goalAnalysis]);

  const renderLoader = () => (
    <Box display="flex" justifyContent="center" alignItems="center" p={4}>
      <CircularProgress />
    </Box>
  );

  return (
    <Box p={{ xs: 2, sm: 4 }} bgcolor="#f9f9f9" minHeight="100vh">
      <Typography variant="h4" gutterBottom fontWeight="bold">
        🎯 Personalized Financial Plan
      </Typography>

      <Divider sx={{ mb: 3 }} />

      <Grid container spacing={4} direction="column">
        {/* Suggested Goals */}
        <Grid item xs={12}>
          <Fade in timeout={600}>
            <Paper elevation={4} sx={{ borderRadius: 3, p: 2, height: '100%' }}>
              <GoalSuggestions
                suggestedGoals={suggestedGoals}
                loading={loadingSuggestions}
                renderLoader={renderLoader}
              />
            </Paper>
          </Fade>
        </Grid>

        {/* Goal Analysis */}
        <Grid item xs={12}>
          <Fade in timeout={800}>
            <Paper elevation={4} sx={{ borderRadius: 3, p: 2, height: '100%' }}>
              <GoalAnalysisCard
                analysis={goalAnalysis}
                loading={loadingAnalysis}
                renderLoader={renderLoader}
              />
            </Paper>
          </Fade>
        </Grid>

        {/* LLM Picks */}
        <Grid item xs={12}>
          <Fade in timeout={1000}>
            <Paper elevation={4} sx={{ borderRadius: 3, p: 2, height: '100%' }}>
              <LLMPicksCard
                picks={llmPicks}
                loading={loadingLLM}
                renderLoader={renderLoader}
              />
            </Paper>
          </Fade>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ResultsPage;
