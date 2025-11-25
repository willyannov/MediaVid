import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import Home from './pages/Home'
import Terms from './pages/Terms'
import Privacy from './pages/Privacy'
// import Batch from './pages/Batch' // Desativado temporariamente

// Keep-alive para prevenir hibernação do backend
import './services/keepAlive'

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="min-h-screen">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/terms" element={<Terms />} />
            <Route path="/privacy" element={<Privacy />} />
            {/* Rota de batch desativada temporariamente */}
            {/* <Route path="/batch" element={<Batch />} /> */}
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App
