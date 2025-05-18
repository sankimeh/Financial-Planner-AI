import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
} from '@mui/material';

// MUI Icons
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import SavingsIcon from '@mui/icons-material/Savings';
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar';
import HomeIcon from '@mui/icons-material/Home';
import ElderlyIcon from '@mui/icons-material/Elderly';
import TravelExploreIcon from '@mui/icons-material/TravelExplore';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import DoneAllIcon from '@mui/icons-material/DoneAll';
import WarningIcon from '@mui/icons-material/Warning';
import ChecklistIcon from '@mui/icons-material/Checklist';

interface Props {
  suggestedGoals: string[];
  loading: boolean;
  renderLoader: () => JSX.Element;
}

const getIconForGoal = (goal: string) => {
  const lower = goal.toLowerCase();
  if (lower.includes('emergency')) return WarningIcon;
  if (lower.includes('life')) return FamilyRestroomIcon;
  if (lower.includes('health')) return HealthAndSafetyIcon;
  if (lower.includes('auto') || lower.includes('car')) return DirectionsCarIcon;
  if (lower.includes('home') || lower.includes('rent')) return HomeIcon;
  if (lower.includes('disability')) return ElderlyIcon;
  if (lower.includes('long-term care')) return ElderlyIcon;
  if (lower.includes('travel')) return TravelExploreIcon;
  if (lower.includes('retirement')) return SavingsIcon;
  if (lower.includes('debt')) return MonetizationOnIcon;
  if (lower.includes('sip')) return TrendingUpIcon;
  if (lower.includes('review')) return DoneAllIcon;
  return ChecklistIcon;
};

const GoalSuggestions: React.FC<Props> = ({ suggestedGoals, loading, renderLoader }) => (
  <Card elevation={3} sx={{ borderRadius: 3, p: 2, width: '100%' }}>
    <CardContent>
      <Typography variant="h6" gutterBottom>
        Suggested Goals
      </Typography>
      {loading ? (
        renderLoader()
      ) : suggestedGoals.length === 0 ? (
        <Box mt={2}>
          <Typography variant="body2" color="textSecondary">
            No suggested goals found.
          </Typography>
        </Box>
      ) : (
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: 2, // spacing between items
          }}
        >
          {suggestedGoals.map((goal, index) => {
            const Icon = getIconForGoal(goal);
            return (
              <Box
                key={index}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  borderRadius: 2,
                  bgcolor: 'background.paper',
                  boxShadow: 1,
                  px: 2,
                  py: 1,
                  minWidth: 150,
                  maxWidth: 250,
                }}
              >
                <Icon color="primary" sx={{ mr: 1 }} />
                <Typography variant="body1" noWrap>
                  {goal}
                </Typography>
              </Box>
            );
          })}
        </Box>
      )}
    </CardContent>
  </Card>
);

export default GoalSuggestions;
