import { useState, useEffect } from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Box, 
  IconButton, 
  Collapse,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Chip
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import OddsHistory from './OddsHistory';

function MatchCard({ match, filters, statusText }) {
  const [expanded, setExpanded] = useState(false);
  const [timeLeft, setTimeLeft] = useState('');

  useEffect(() => {
    const updateCountdown = () => {
      const now = new Date();
      const matchTime = new Date(match.commence_time);
      const diff = matchTime - now;

      if (diff > 0) {
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        setTimeLeft(`${hours}h ${minutes}m`);
      }
    };

    updateCountdown();
    const timer = setInterval(updateCountdown, 60000); // Update every minute

    return () => clearInterval(timer);
  }, [match.commence_time]);

  const getBestOdds = (team) => {
    let bestOdds = 0;
    let bestBookmaker = '';
    
    match.bookmakers.forEach(bookmaker => {
      const outcome = bookmaker.markets[0]?.outcomes.find(o => o.name === team);
      if (outcome && (outcome.price > bestOdds || bestOdds === 0)) {
        bestOdds = outcome.price;
        bestBookmaker = bookmaker.title;
      }
    });
    
    return { odds: bestOdds.toFixed(2), bookmaker: bestBookmaker };
  };

  const homeOdds = getBestOdds(match.home_team);
  const awayOdds = getBestOdds(match.away_team);

  return (
    <Card sx={{ mb: 2, backgroundColor: '#121212' }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h6" gutterBottom>
              {match.home_team} vs {match.away_team}
            </Typography>
            <Typography color="text.secondary" gutterBottom>
              {new Date(match.commence_time).toLocaleString()}
            </Typography>
            {timeLeft && (
              <Typography sx={{ color: '#1a73e8', fontWeight: 'bold', mt: 1 }}>
                Starts in: {timeLeft}
              </Typography>
            )}
          </Box>
          
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
            <Chip 
              label={`${match.home_team}: ${homeOdds.odds}`}
              color="primary"
              variant="outlined"
              sx={{ mb: 1 }}
            />
            <Chip 
              label={`${match.away_team}: ${awayOdds.odds}`}
              color="primary"
              variant="outlined"
            />
          </Box>

          <IconButton 
            onClick={() => setExpanded(!expanded)}
            sx={{ 
              transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
              transition: 'transform 0.3s',
              ml: 2
            }}
          >
            <ExpandMoreIcon />
          </IconButton>
        </Box>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <Divider sx={{ my: 2 }} />
          
          <Typography variant="h6" gutterBottom>
            All Bookmaker Odds
          </Typography>
          
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Bookmaker</TableCell>
                <TableCell align="right">{match.home_team}</TableCell>
                <TableCell align="right">{match.away_team}</TableCell>
                <TableCell align="right">Draw</TableCell>
                <TableCell align="right">Last Updated</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {match.bookmakers.map((bookmaker) => {
                const homeOdds = bookmaker.markets[0]?.outcomes.find(o => o.name === match.home_team)?.price;
                const awayOdds = bookmaker.markets[0]?.outcomes.find(o => o.name === match.away_team)?.price;
                const drawOdds = bookmaker.markets[0]?.outcomes.find(o => o.name === 'Draw')?.price;
                const lastUpdate = new Date(bookmaker.last_update).toLocaleTimeString();

                return (
                  <TableRow key={bookmaker.title}>
                    <TableCell>{bookmaker.title}</TableCell>
                    <TableCell align="right">{homeOdds?.toFixed(2) || 'N/A'}</TableCell>
                    <TableCell align="right">{awayOdds?.toFixed(2) || 'N/A'}</TableCell>
                    <TableCell align="right">{drawOdds?.toFixed(2) || 'N/A'}</TableCell>
                    <TableCell align="right">{lastUpdate}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>

          <Box sx={{ mt: 3 }}>
            {match.bookmakers.map((bookmaker) => (
              <OddsHistory 
                key={bookmaker.key}
                match={match}
                bookmaker={bookmaker}
              />
            ))}
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
}

export default MatchCard;
