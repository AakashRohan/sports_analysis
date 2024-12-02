import { Card, CardContent, Typography, Box } from '@mui/material';

function MatchCard({ match }) {
  // Function to find best odds for each team
  const getBestOdds = (team) => {
    let bestOdds = 0;
    let bestBookmaker = '';

    match.bookmakers.forEach(bookmaker => {
      bookmaker.markets.forEach(market => {
        if (market.key === 'h2h') {
          market.outcomes.forEach(outcome => {
            if (outcome.name === team && (outcome.price > bestOdds || bestOdds === 0)) {
              bestOdds = outcome.price;
              bestBookmaker = bookmaker.title;
            }
          });
        }
      });
    });

    return { odds: bestOdds.toFixed(2), bookmaker: bestBookmaker };
  };

  const homeOdds = getBestOdds(match.home_team);
  const awayOdds = getBestOdds(match.away_team);

  return (
    <Card sx={{ minWidth: 275, mb: 2 }}>
      <CardContent>
        <Typography variant="h6" component="div">
          {match.home_team} vs {match.away_team}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          {new Date(match.commence_time).toLocaleString()}
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
          <Typography variant="body2">
            {match.home_team}: {homeOdds.odds} ({homeOdds.bookmaker})
          </Typography>
          <Typography variant="body2">
            {match.away_team}: {awayOdds.odds} ({awayOdds.bookmaker})
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}

export default MatchCard;
