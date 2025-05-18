import React from 'react';
import { Typography, Card, CardContent, CircularProgress, Box } from '@mui/material';
import type { GoalAnalysis } from '../types/resultsTypes';

interface Props {
  analysis: GoalAnalysis | null;
  loading: boolean;
}

const GoalAnalysis: React.FC<Props> = ({ analysis, loading }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Goal Analysis & Portfolio</Typography>
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" p={4}>
            <CircularProgress />
          </Box>
        ) : analysis ? (
          <>
            <Typography>Monthly Surplus: ₹{analysis.monthly_surplus}</Typography>
            <Typography>Emergency Fund OK: {analysis.emergency_fund_ok ? 'Yes' : 'No'}</Typography>
            <Typography>Ideal Emergency Fund: ₹{analysis.ideal_emergency_fund}</Typography>
            <Typography>Recommended Allocation:</Typography>
            <ul>
              <li>Equity: {analysis.recommended_allocation.equity}%</li>
              <li>Bonds: {analysis.recommended_allocation.bonds}%</li>
              <li>Commodities: {analysis.recommended_allocation.commodities}%</li>
            </ul>
          </>
        ) : (
          <Typography color="error">Failed to load analysis.</Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default GoalAnalysis;
