import React from 'react';
import {
  Typography,
  Card,
  CardContent,
  CircularProgress,
  Box,
  Chip,
  Stack,
  Divider,
} from '@mui/material';
import type { GoalAnalysis } from '../types/resultsTypes';

interface Props {
  analysis: GoalAnalysis | null;
  loading: boolean;
}

const formatCurrency = (num: number) =>
  `₹${num.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;

const GoalAnalysis: React.FC<Props> = ({ analysis, loading }) => {
  return (
    <Card
      sx={{
        maxWidth: 400, // keep card compact, adjust as needed
        mx: 'auto', // center horizontally if parent is wide
      }}
      elevation={1}
    >
      <CardContent sx={{ padding: '12px 16px' }}>
        <Typography variant="h6" mb={1}>
          Goal Analysis & Portfolio
        </Typography>

        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" py={3}>
            <CircularProgress size={24} />
          </Box>
        ) : analysis ? (
          <>
            <Typography variant="body2" mb={0.5}>
              <strong>Monthly Surplus:</strong> {formatCurrency(analysis.monthly_surplus)}
            </Typography>

            <Typography variant="body2" mb={0.5} display="flex" alignItems="center" gap={1}>
              <strong>Emergency Fund OK:</strong>{' '}
              <Chip
                label={analysis.emergency_fund_ok ? 'Yes' : 'No'}
                color={analysis.emergency_fund_ok ? 'success' : 'warning'}
                size="small"
                sx={{ height: 20, fontSize: 12 }}
              />
            </Typography>

            <Typography variant="body2" mb={1}>
              <strong>Ideal Emergency Fund:</strong> {formatCurrency(analysis.ideal_emergency_fund)}
            </Typography>

            <Divider sx={{ my: 1 }} />

            <Typography variant="subtitle2" mb={1}>
              Recommended Allocation:
            </Typography>

            <Stack direction="row" spacing={1} mb={0}>
              <Chip label={`Equity: ${analysis.recommended_allocation.equity}%`} color="primary" size="small" />
              <Chip label={`Bonds: ${analysis.recommended_allocation.bonds}%`} color="secondary" size="small" />
              <Chip label={`Commodities: ${analysis.recommended_allocation.commodities}%`} color="warning" size="small" />
            </Stack>
          </>
        ) : (
          <Typography color="error" variant="body2" py={1}>
            Failed to load analysis.
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default GoalAnalysis;
