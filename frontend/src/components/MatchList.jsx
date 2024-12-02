import { useEffect, useState } from 'react';
import { Container, Typography, CircularProgress, Box } from '@mui/material';
import MatchCard from './MatchCard';
import { fetchMatches } from '../services/api';

function MatchList() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getMatches = async () => {
      try {
        const data = await fetchMatches();
        setMatches(data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch matches');
        setLoading(false);
      }
    };

    getMatches();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Typography color="error" sx={{ mt: 4 }}>
        {error}
      </Typography>
    );
  }

  return (
    <Container>
      <Typography variant="h4" sx={{ mb: 4, mt: 4 }}>
        Upcoming Matches
      </Typography>
      {matches.map((match) => (
        <MatchCard key={match._id} match={match} />
      ))}
    </Container>
  );
}

export default MatchList;
