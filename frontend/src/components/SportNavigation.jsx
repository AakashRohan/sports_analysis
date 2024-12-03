import { 
  Box, 
  Tabs, 
  Tab, 
  ButtonGroup, 
  Button,
  Divider,
  Badge
} from '@mui/material';
import { 
  SportsCricket, 
  SportsSoccer, 
  SportsTennis 
} from '@mui/icons-material';
import { useState } from 'react';

function SportNavigation({ onFilterChange, matchCounts }) {
  const [sport, setSport] = useState('cricket');
  const [format, setFormat] = useState('test');
  const [betType, setBetType] = useState('h2h');

  const handleSportChange = (_, newValue) => {
    setSport(newValue);
    // Reset format when changing sports
    setFormat(newValue === 'cricket' ? 'test' : null);
    onFilterChange({ 
      sport: newValue, 
      format: newValue === 'cricket' ? 'test' : null, 
      betType 
    });
  };

  const handleFormatChange = (newFormat) => {
    setFormat(newFormat);
    onFilterChange({ sport, format: newFormat, betType });
  };

  const handleBetTypeChange = (newBetType) => {
    setBetType(newBetType);
    onFilterChange({ sport, format, betType: newBetType });
  };

  return (
    <Box sx={{ width: '100%', mb: 3 }}>
      {/* Sports Selection */}
      <Tabs 
        value={sport} 
        onChange={handleSportChange}
        sx={{ mb: 2 }}
        centered
      >
        <Tab 
          icon={
            <Badge badgeContent={matchCounts?.cricket || 0} color="primary">
              <SportsCricket />
            </Badge>
          }
          label="Cricket" 
          value="cricket"
          sx={{ '&.Mui-selected': { color: '#1a73e8' } }}
        />
        <Tab 
          icon={
            <Badge badgeContent={matchCounts?.football || 0} color="primary">
              <SportsSoccer />
            </Badge>
          }
          label="Football" 
          value="football"
          sx={{ '&.Mui-selected': { color: '#1a73e8' } }}
        />
        <Tab 
          icon={
            <Badge badgeContent={matchCounts?.tennis || 0} color="primary">
              <SportsTennis />
            </Badge>
          }
          label="Tennis" 
          value="tennis"
          sx={{ '&.Mui-selected': { color: '#1a73e8' } }}
        />
      </Tabs>

      {/* Format Selection (visible only for cricket) */}
      {sport === 'cricket' && (
        <ButtonGroup 
          variant="outlined" 
          sx={{ mb: 2, display: 'flex', justifyContent: 'center' }}
        >
          <Button 
            onClick={() => handleFormatChange('test')}
            variant={format === 'test' ? 'contained' : 'outlined'}
          >
            Test
          </Button>
          <Button 
            onClick={() => handleFormatChange('odi')}
            variant={format === 'odi' ? 'contained' : 'outlined'}
          >
            ODI
          </Button>
          <Button 
            onClick={() => handleFormatChange('t20')}
            variant={format === 't20' ? 'contained' : 'outlined'}
          >
            T20
          </Button>
        </ButtonGroup>
      )}

      <Divider sx={{ my: 2 }} />

      {/* Bet Type Selection */}
      <ButtonGroup 
        variant="outlined" 
        sx={{ display: 'flex', justifyContent: 'center' }}
      >
        <Button 
          onClick={() => handleBetTypeChange('h2h')}
          variant={betType === 'h2h' ? 'contained' : 'outlined'}
        >
          Head to Head
        </Button>
        <Button 
          onClick={() => handleBetTypeChange('session')}
          variant={betType === 'session' ? 'contained' : 'outlined'}
        >
          Session
        </Button>
        <Button 
          onClick={() => handleBetTypeChange('other')}
          variant={betType === 'other' ? 'contained' : 'outlined'}
        >
          Other Markets
        </Button>
      </ButtonGroup>
    </Box>
  );
}

export default SportNavigation;
