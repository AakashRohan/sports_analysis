import { useState, useEffect } from 'react';
import { Container } from '@mui/material';
import MatchList from '../components/MatchList';
import SportNavigation from '../components/SportNavigation';
import { fetchMatches } from '../services/api';

function Home() {
  const [filters, setFilters] = useState(() => {
    const savedFilters = localStorage.getItem('sportFilters');
    return savedFilters ? JSON.parse(savedFilters) : {
      sport: 'cricket',
      format: 'test',
      betType: 'h2h'
    };
  });

  const [matches, setMatches] = useState([]);
  const [matchCounts, setMatchCounts] = useState({
    cricket: 0,
    football: 0,
    tennis: 0
  });

  useEffect(() => {
    localStorage.setItem('sportFilters', JSON.stringify(filters));
  }, [filters]);

  useEffect(() => {
    const getMatches = async () => {
      try {
        const data = await fetchMatches();
        setMatches(data);
        
        const counts = {
          cricket: data.filter(m => m.sport_key.includes('cricket')).length,
          football: data.filter(m => m.sport_key.includes('soccer')).length,
          tennis: data.filter(m => m.sport_key.includes('tennis')).length
        };
        
        setMatchCounts(counts);
      } catch (error) {
        console.error('Error fetching matches:', error);
      }
    };

    getMatches();
  }, []);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const filteredMatches = matches.filter(match => {
    if (filters.sport === 'cricket' && !match.sport_key.includes('cricket')) {
      return false;
    }
    if (filters.sport === 'football' && !match.sport_key.includes('soccer')) {
      return false;
    }
    if (filters.sport === 'tennis' && !match.sport_key.includes('tennis')) {
      return false;
    }

    if (filters.sport === 'cricket' && filters.format) {
      if (filters.format === 'test' && !match.sport_key.includes('test_match')) {
        return false;
      }
      if (filters.format === 'odi' && !match.sport_key.includes('odi')) {
        return false;
      }
      if (filters.format === 't20' && !match.sport_key.includes('t20')) {
        return false;
      }
    }

    if (filters.betType === 'h2h') {
      return match.bookmakers.some(b => 
        b.markets.some(m => m.key === 'h2h')
      );
    }
    if (filters.betType === 'session') {
      return match.bookmakers.some(b => 
        b.markets.some(m => m.key === 'session')
      );
    }

    return true;
  });

  return (
    <Container>
      <SportNavigation 
        onFilterChange={handleFilterChange}
        matchCounts={matchCounts}
        currentFilters={filters}
      />
      <MatchList 
        matches={filteredMatches}
        filters={filters}
      />
    </Container>
  );
}

export default Home;
