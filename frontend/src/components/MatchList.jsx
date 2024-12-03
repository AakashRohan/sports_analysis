import { useState } from 'react';
import { 
  Box, 
  Typography, 
  Collapse,
  IconButton,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MatchCard from './MatchCard';

function MatchList({ matches, filters }) {
  const [expandedSections, setExpandedSections] = useState({
    live: true,
    today: true,
    tomorrow: true,
    upcoming: true,
    completed: false
  });

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Group matches by their status
  const groupedMatches = {
    live: [],
    today: [],
    tomorrow: [],
    upcoming: [],
    completed: []
  };

  matches.forEach(match => {
    const matchDate = new Date(match.commence_time);
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (matchDate < now) {
      groupedMatches.completed.push(match);
    } else if (matchDate.toDateString() === now.toDateString()) {
      groupedMatches.today.push(match);
    } else if (matchDate.toDateString() === tomorrow.toDateString()) {
      groupedMatches.tomorrow.push(match);
    } else {
      groupedMatches.upcoming.push(match);
    }
  });

  const renderSection = (title, matchList, section) => {
    if (!matchList || matchList.length === 0) return null;
    
    return (
      <Box sx={{ mb: 4 }}>
        <Box 
          sx={{ 
            display: 'flex', 
            alignItems: 'center',
            cursor: 'pointer',
            mb: 2,
            backgroundColor: 'rgba(26, 115, 232, 0.1)',
            padding: '12px 20px',
            borderRadius: '8px'
          }}
          onClick={() => toggleSection(section)}
        >
          <Typography variant="h6" component="h2">
            {title} ({matchList.length})
          </Typography>
          <IconButton
            sx={{
              transform: expandedSections[section] ? 'rotate(180deg)' : 'rotate(0deg)',
              transition: 'transform 0.3s',
              ml: 'auto'
            }}
          >
            <ExpandMoreIcon />
          </IconButton>
        </Box>
        <Collapse in={expandedSections[section]}>
          {matchList.map(match => (
            <MatchCard 
              key={match._id} 
              match={match}
              filters={filters}
            />
          ))}
        </Collapse>
      </Box>
    );
  };

  return (
    <Box>
      {matches.length === 0 ? (
        <Typography 
          variant="h6" 
          sx={{ 
            textAlign: 'center', 
            mt: 4, 
            color: 'text.secondary' 
          }}
        >
          No matches found for the selected filters
        </Typography>
      ) : (
        <>
          {renderSection('Live Matches', groupedMatches.live, 'live')}
          {renderSection("Today's Matches", groupedMatches.today, 'today')}
          {renderSection('Tomorrow', groupedMatches.tomorrow, 'tomorrow')}
          {renderSection('Upcoming', groupedMatches.upcoming, 'upcoming')}
          {renderSection('Completed', groupedMatches.completed, 'completed')}
        </>
      )}
    </Box>
  );
}

export default MatchList;
