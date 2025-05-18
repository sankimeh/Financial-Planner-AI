import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Divider,
  Chip,
  Box,
  LinearProgress,
  Stack
} from '@mui/material';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import type GoalAnalysis from './GoalAnalysis';

interface Props {
  analysis: GoalAnalysis | null;
  loading: boolean;
  renderLoader: () => JSX.Element;
}

const formatCurrency = (num: number) =>
  `₹${num.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;

const COLORS = ['#1976d2', '#9c27b0', '#ff9800']; // Equity, Bonds, Commodities

const GoalAnalysisCard: React.FC<Props> = ({ analysis, loading, renderLoader }) => {
  if (loading) return renderLoader();

  if (!analysis) {
    return (
      <Card>
        <CardContent>
          <Typography color="error">Failed to load analysis.</Typography>
        </CardContent>
      </Card>
    );
  }

  const allocationData = [
    { name: 'Equity', value: analysis.recommended_allocation.equity },
    { name: 'Bonds', value: analysis.recommended_allocation.bonds },
    { name: 'Commodities', value: analysis.recommended_allocation.commodities }
  ];

  // Count of goals
  const goalsCount = analysis.goal_analysis.length;

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Goal Analysis & Portfolio
        </Typography>

        <Typography variant="body1">
          <strong>Monthly Surplus:</strong> {formatCurrency(analysis.monthly_surplus)}
        </Typography>

        <Typography variant="body1">
          <strong>Emergency Fund OK:</strong>{' '}
          <Chip
            label={analysis.emergency_fund_ok ? 'Yes' : 'No'}
            color={analysis.emergency_fund_ok ? 'success' : 'warning'}
            size="small"
          />
        </Typography>

        <Typography variant="body1" gutterBottom>
          <strong>Ideal Emergency Fund:</strong> {formatCurrency(analysis.ideal_emergency_fund)}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Typography variant="subtitle1" gutterBottom>
          Recommended Allocation:
        </Typography>

        <Stack direction="row" spacing={2} mb={2}>
          <Chip label={`Equity: ${analysis.recommended_allocation.equity}%`} color="primary" />
          <Chip label={`Bonds: ${analysis.recommended_allocation.bonds}%`} color="secondary" />
          <Chip label={`Commodities: ${analysis.recommended_allocation.commodities}%`} color="warning" />
        </Stack>

        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={allocationData}
              dataKey="value"
              nameKey="name"
              outerRadius={80}
              fill="#8884d8"
              label
            >
              {allocationData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>

        <Divider sx={{ my: 2 }} />

        <Typography variant="subtitle1" gutterBottom>
          Goal Feasibility:
        </Typography>

        {/* Container for goals with flex wrap */}
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            maxWidth: '100%',
            justifyContent: goalsCount % 2 === 1 ? 'center' : 'flex-start',
            gap: 2,
          }}
        >
          {analysis.goal_analysis.map((goal, index) => {
            const progress = Math.min((goal.projected_value / goal.target) * 100, 100);

            // Each goal box takes 48% width approx (50% minus gap)
            // The last odd goal will be centered because justifyContent is center
            return (
              <Box
                key={index}
                sx={{
                  width: '48%',
                  minWidth: 280,
                  border: '1px solid #ddd',
                  borderRadius: 2,
                  p: 2,
                  boxSizing: 'border-box',
                }}
              >
                <Typography variant="h6">{goal.name}</Typography>
                <Stack direction="row" spacing={1} alignItems="center" mt={1}>
                  <Chip
                    label={goal.feasible ? 'Feasible' : 'Needs Adjustment'}
                    color={goal.feasible ? 'success' : 'error'}
                    size="small"
                  />
                </Stack>

                <Typography variant="body2" mt={1}>
                  <strong>Target:</strong> {formatCurrency(goal.target)}
                </Typography>
                <Typography variant="body2">
                  <strong>Projected Value:</strong> {formatCurrency(goal.projected_value)}
                </Typography>

                <Box mt={1}>
                  <LinearProgress
                    variant="determinate"
                    value={progress}
                    sx={{
                      height: 10,
                      borderRadius: 5,
                      backgroundColor: '#f0f0f0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: goal.feasible ? 'green' : 'orange'
                      }
                    }}
                  />
                  <Typography variant="caption">{progress.toFixed(1)}% of goal funded</Typography>
                </Box>

                <Stack direction="row" spacing={2} flexWrap="wrap" mt={1}>
                  <Typography variant="body2" whiteSpace="nowrap" sx={{ flexShrink: 0 }}>
                    <strong>Horizon:</strong> {goal.horizon_months} months
                  </Typography>
                  <Typography variant="body2" whiteSpace="nowrap" sx={{ flexShrink: 0 }}>
                    <strong>Expected Return:</strong> {goal.expected_return_annual}%
                  </Typography>
                </Stack>

                {!goal.feasible && (
                  <Box mt={1}>
                    <Typography variant="body2" color="textSecondary">
                      <strong>Recommended SIP:</strong> {formatCurrency(goal.recommendation.suggested_sip)}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      <strong>Extend By:</strong> {goal.recommendation.extend_by_months} months
                    </Typography>
                  </Box>
                )}
              </Box>
            );
          })}
        </Box>
      </CardContent>
    </Card>
  );
};

export default GoalAnalysisCard;
