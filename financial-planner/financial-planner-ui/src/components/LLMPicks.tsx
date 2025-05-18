import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import type { LLMPicks } from '../types/resultsTypes';


interface Props {
  picks: LLMPicks | null;
  loading: boolean;
  renderLoader: () => JSX.Element;
}

const LLMPicksCard: React.FC<Props> = ({ picks, loading, renderLoader }) => (
  <Card>
    <CardContent>
      <Typography variant="h6">Top Picks (LLM)</Typography>
      {loading ? renderLoader() : picks ? (
        <>
          <Typography>{picks.summary}</Typography>

          {picks.equity_picks?.length > 0 && (
            <>
              <Typography variant="subtitle1">Equity:</Typography>
              <ul>
                {picks.equity_picks.map((item, i) => (
                  <li key={i}>{item.ticker} - {item.name} ({item.horizon}): {item.reason}</li>
                ))}
              </ul>
            </>
          )}
          {picks.bond_picks?.length > 0 && (
            <>
              <Typography variant="subtitle1">Bonds:</Typography>
              <ul>
                {picks.bond_picks.map((item, i) => (
                  <li key={i}>{item.ticker} - {item.name} ({item.horizon}): {item.reason}</li>
                ))}
              </ul>
            </>
          )}
          {picks.commodity_picks?.length > 0 && (
            <>
              <Typography variant="subtitle1">Commodities:</Typography>
              <ul>
                {picks.commodity_picks.map((item, i) => (
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
);

export default LLMPicksCard;
