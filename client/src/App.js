import './App.css';
import Navbar from './components/navbar';
import Home from './Pages/Home';
import Leaderboard from './Pages/Leaderboard';
import { Switch, Route } from 'react-router-dom';
import Login from './Pages/LoginForm';


function App() {
  return (
    <div className="App">
      <Navbar />
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/data_visualization" component={Leaderboard} />
        <Route path="/login" component={Login} />
      </Switch>
    </div>
  );
}

export default App;
