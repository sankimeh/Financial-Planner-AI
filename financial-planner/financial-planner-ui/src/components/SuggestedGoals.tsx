import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  IconButton,
  Collapse,
  Stack,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

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

interface GoalSuggestion {
  goal: string;
  reason: string;
}

interface Props {
  suggestedGoals: GoalSuggestion[];
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

const GoalSuggestions: React.FC<Props> = ({ suggestedGoals, loading, renderLoader }) => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleExplanation = (index: number) => {
    setOpenIndex((prev) => (prev === index ? null : index));
  };

  return (
    <Card elevation={3} sx={{ borderRadius: 3, p: 2, width: '98%' }}>
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
          <Stack spacing={2} mt={2}>
            {suggestedGoals.map((item, index) => {
              const Icon = getIconForGoal(item.goal);
              const isOpen = openIndex === index;

              return (
                <Card
                  key={index}
                  elevation={1}
                  sx={{
                    borderRadius: 2,
                    p: 2,
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Icon color="primary" sx={{ mr: 1 }} />
                    <Typography variant="body1" sx={{ flexGrow: 1 }}>
                      {item.goal}
                    </Typography>
                    <IconButton
                      onClick={() => toggleExplanation(index)}
                      size="small"
                      sx={{
                        transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                        transition: 'transform 0.2s',
                      }}
                    >
                      <ExpandMoreIcon />
                    </IconButton>
                  </Box>
                  <Collapse in={isOpen} unmountOnExit>
                    <Typography variant="body2" color="text.secondary" mt={1}>
                      {item.reason}
                    </Typography>
                  </Collapse>
                </Card>
              );
            })}
          </Stack>
        )}
      </CardContent>
    </Card>
  );
};

export default GoalSuggestions;
