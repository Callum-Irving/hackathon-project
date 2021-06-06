import './App.css';
import Navbar from './components/navbar';
import Home from './Pages/Home';
import Leaderboard from './Pages/Leaderboard';
import { Switch, Route } from 'react-router-dom';
import Login from './Pages/LoginForm';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

const data = [
  {
    name: "Page A",
    Garbage: 4000,
    Recycling: 2400,
    Compost: 2400
  },
  {
    name: "Page B",
    Garbage: 3000,
    Recycling: 1398,
    Compost: 2210
  },
  {
    name: "Page C",
    Garbage: 2000,
    Recycling: 9800,
    Compost: 2290
  },
  {
    name: "Page D",
    Garbage: 2780,
    Recycling: 3908,
    Compost: 2000
  },
  {
    name: "Page E",
    Garbage: 1890,
    Recycling: 4800,
    Compost: 2181
  },
  {
    name: "Page F",
    Garbage: 2390,
    Recycling: 3800,
    Compost: 2500
  },
  {
    name: "Page G",
    Garbage: 3490,
    Recycling: 4300,
    Compost: 2100
  }
];

function App() {
  return (
    <div className="app">
      <Navbar />
      <Switch>
        <Route exact path="/" component={Home} />
				<Route path="/data_visualization" component={Leaderboard} />
				<Route path="/login" component={Login} />
      </Switch>
      <BarChart
        width={1400}
        height={750}
        data={data}
        margin={{
          top: 20,
          right: 30,
          left: 20,
          bottom: 5
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="Garbage" stackId="a" fill="#8884d8" />
        <Bar dataKey="Recycling" stackId="a" fill="#82ca9d" />
        <Bar dataKey="Compost" stackId="a" fill="#c2e0e3" />
      </BarChart>
    </div>
  );
}

export default App;
