import './Home.css';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

function LeaderBoard() {
	return (
        <div class="header">
			<h1>myWaste</h1>
        </div>
    )
}

const data = [
  {
    name: "Laurelwood",
    Garbage: 4000,
    Recycling: 2400,
    Compost: 2400
  },
  {
    name: "Westvale",
    Garbage: 3000,
    Recycling: 1398,
    Compost: 2210
  },
  {
    name: "Beechwood",
    Garbage: 2000,
    Recycling: 9800,
    Compost: 2290
  },
  {
    name: "Westmount",
    Garbage: 2780,
    Recycling: 3908,
    Compost: 2000
  },
  {
    name: "Vista Hills",
    Garbage: 1890,
    Recycling: 4800,
    Compost: 2181
  },
  {
    name: "Lakeshore",
    Garbage: 2390,
    Recycling: 3800,
    Compost: 2500
  },
  {
    name: "Eastbridge",
    Garbage: 3490,
    Recycling: 4300,
    Compost: 2100
  }
];

function Home() {
	return (
		<div className="app">
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

export default Home;
