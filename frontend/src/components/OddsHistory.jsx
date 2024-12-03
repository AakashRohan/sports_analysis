import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend,
  ResponsiveContainer 
} from 'recharts';
import { Box, Typography, Paper } from '@mui/material';

function OddsHistory({ match, bookmaker }) {
  // Normally this would come from your API/database
  // For now, we'll simulate historical data
  const generateHistoricalData = () => {
    const data = [];
    const baseHomeOdds = parseFloat(bookmaker.markets[0]?.outcomes.find(o => o.name === match.home_team)?.price || 2);
    const baseAwayOdds = parseFloat(bookmaker.markets[0]?.outcomes.find(o => o.name === match.away_team)?.price || 2);
    
    // Generate last 24 hours of data
    for (let i = 24; i >= 0; i--) {
      const time = new Date();
      time.setHours(time.getHours() - i);
      
      // Add some random variation to odds
      const variation = Math.sin(i * 0.5) * 0.1;
      
      data.push({
        time: time.toLocaleTimeString(),
        homeOdds: (baseHomeOdds + variation).toFixed(2),
        awayOdds: (baseAwayOdds - variation).toFixed(2),
      });
    }
    
    return data;
  };

  const data = generateHistoricalData();

  return (
    <Paper 
      sx={{ 
        p: 2, 
        mt: 2, 
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderRadius: 2
      }}
    >
      <Typography variant="h6" gutterBottom>
        Odds Movement ({bookmaker.title})
      </Typography>
      
      <Box sx={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
            <XAxis 
              dataKey="time" 
              stroke="#fff"
              tick={{ fill: '#fff' }}
              interval={4}
            />
            <YAxis 
              stroke="#fff"
              tick={{ fill: '#fff' }}
              domain={['auto', 'auto']}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#121212',
                border: '1px solid #333',
                borderRadius: '4px'
              }}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="homeOdds" 
              stroke="#1a73e8" 
              name={match.home_team}
              dot={false}
            />
            <Line 
              type="monotone" 
              dataKey="awayOdds" 
              stroke="#dc3545" 
              name={match.away_team}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </Box>
      
      <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
        * Historical data shown for the last 24 hours
      </Typography>
    </Paper>
  );
}

export default OddsHistory;
