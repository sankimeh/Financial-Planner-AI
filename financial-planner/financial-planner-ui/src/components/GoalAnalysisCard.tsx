import React, { type JSX } from "react";
import {
  Card,
  CardContent,
  Typography,
  Divider,
  Chip,
  Box,
  LinearProgress,
  Stack,
  Accordion,
  AccordionDetails,
  AccordionSummary,
} from "@mui/material";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import type GoalAnalysis from "./GoalAnalysis";

interface Props {
  analysis: GoalAnalysis | null;
  loading: boolean;
  renderLoader: () => JSX.Element;
}

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const formatCurrency = (num: number) =>
  `₹${num.toLocaleString("en-IN", { maximumFractionDigits: 0 })}`;

const COLORS = ["#1976d2", "#9c27b0", "#ff9800"]; // Equity, Bonds, Commodities

const GoalAnalysisCard: React.FC<Props> = ({
  analysis,
  loading,
  renderLoader,
}) => {
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
    { name: "Equity", value: analysis.recommended_allocation.equity },
    { name: "Bonds", value: analysis.recommended_allocation.bonds },
    { name: "Commodities", value: analysis.recommended_allocation.commodities },
  ];

  const goalsCount = analysis.goal_analysis.length;

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Goal Analysis & Portfolio Recommendation
        </Typography>

        <Typography variant="body1">
          <strong>Monthly Surplus:</strong>{" "}
          {formatCurrency(analysis.monthly_surplus)}
        </Typography>

        <Typography variant="body1">
          <strong>Emergency Fund Status:</strong>{" "}
          <Chip
            label={analysis.emergency_fund_ok ? "Sufficient" : "Needs More"}
            color={analysis.emergency_fund_ok ? "success" : "warning"}
            size="small"
          />
        </Typography>

        <Typography variant="body1" gutterBottom>
          <strong>Ideal Emergency Fund:</strong>{" "}
          {formatCurrency(analysis.ideal_emergency_fund)}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Typography variant="subtitle1" gutterBottom>
          Recommended Portfolio Allocation
        </Typography>

        <Stack direction="row" spacing={2} mb={2}>
          <Chip
            label={`Equity: ${analysis.recommended_allocation.equity}%`}
            color="primary"
          />
          <Chip
            label={`Bonds: ${analysis.recommended_allocation.bonds}%`}
            color="secondary"
          />
          <Chip
            label={`Commodities: ${analysis.recommended_allocation.commodities}%`}
            color="warning"
          />
        </Stack>

        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={allocationData}
              dataKey="value"
              nameKey="name"
              outerRadius={80}
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

        {/* 🔽 Allocation Explanation Plain Text */}
        {analysis.allocation_explanation && (
          <>
            <Divider sx={{ my: 2 }} />
            <Accordion>
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="allocation-content"
                id="allocation-header"
              >
                <Typography variant="subtitle1">
                  Allocation Rationale
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ whiteSpace: "pre-line" }}
                >
                  {analysis.allocation_explanation}
                </Typography>
              </AccordionDetails>
            </Accordion>
          </>
        )}
        <Divider sx={{ my: 2 }} />

        <Typography variant="subtitle1" gutterBottom>
          Goal Status
        </Typography>

        <Box
          sx={{
            display: "flex",
            flexWrap: "wrap",
            maxWidth: "100%",
            justifyContent: goalsCount % 2 === 1 ? "center" : "flex-start",
            gap: 2,
          }}
        >
          {analysis.goal_analysis.map((goal, index) => {
            const progress = Math.min(
              (goal.projected_value / goal.target) * 100,
              100
            );

            return (
              <Box
                key={index}
                sx={{
                  width: "48%",
                  minWidth: 280,
                  border: "1px solid #ddd",
                  borderRadius: 2,
                  p: 2,
                  boxSizing: "border-box",
                }}
              >
                <Typography variant="h6" gutterBottom>
                  {goal.name}
                </Typography>

                <Stack direction="row" spacing={1} alignItems="center" mt={1}>
                  <Chip
                    label={goal.feasible ? "On Track" : "Needs Attention"}
                    color={goal.feasible ? "success" : "error"}
                    size="small"
                  />
                </Stack>

                <Typography variant="body2" mt={1}>
                  <strong>Target:</strong> {formatCurrency(goal.target)}
                </Typography>
                <Typography variant="body2">
                  <strong>Projected:</strong>{" "}
                  {formatCurrency(goal.projected_value)}
                </Typography>

                <Box mt={1}>
                  <LinearProgress
                    variant="determinate"
                    value={progress}
                    sx={{
                      height: 10,
                      borderRadius: 5,
                      backgroundColor: "#f0f0f0",
                      "& .MuiLinearProgress-bar": {
                        backgroundColor: goal.feasible ? "green" : "orange",
                      },
                    }}
                  />
                  <Typography variant="caption">
                    {progress.toFixed(1)}% funded
                  </Typography>
                </Box>

                <Stack direction="row" spacing={2} flexWrap="wrap" mt={1}>
                  <Typography variant="body2" whiteSpace="nowrap">
                    <strong>Horizon:</strong> {goal.horizon_months} months
                  </Typography>
                  <Typography variant="body2" whiteSpace="nowrap">
                    <strong>Return Rate:</strong> {goal.expected_return_annual}%
                  </Typography>
                </Stack>

                {!goal.feasible && (
                  <Box mt={2}>
                    <Typography variant="subtitle2" gutterBottom>
                      Suggestions to Meet Goal:
                    </Typography>
                    {goal.recommendation?.suggested_sip && (
                      <Typography variant="body2" color="textSecondary">
                        Increase SIP to{" "}
                        <strong>
                          {formatCurrency(goal.recommendation.suggested_sip)}
                        </strong>{" "}
                        per month.
                      </Typography>
                    )}
                    {goal.recommendation?.extend_by_months && (
                      <Typography variant="body2" color="textSecondary">
                        Or extend goal by{" "}
                        <strong>
                          {goal.recommendation.extend_by_months} months
                        </strong>
                        .
                      </Typography>
                    )}
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
