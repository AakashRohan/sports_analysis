import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import MatchDetails from './pages/MatchDetails';

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/match/:id" element={<MatchDetails />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
