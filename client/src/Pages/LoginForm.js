import React, { useState } from 'react';
import './LoginForm.css';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis
} from "recharts";

const data = [
  {
    subject: "Recycle",
    A: 76,
    B: 76,
    fullMark: 150
  },
  {
    subject: "Green Bin",
    A: 28,
    B: 130,
    fullMark: 150
  },
  {
    subject: "Garbage",
    A: 120,
    B: 130,
    fullMark: 150
  }
];

const heroku_url = 'https://hacktheearth-project.herokuapp.com/'

const Login = ({ handleClose }) => {
  // create state variables for each input
  const [address, setAddress] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = e => {
    e.preventDefault();
    console.log(address, password);
    fetch(heroku_url, {
      method: 'POST',
      credentials: 'include',
      body: {
        address: address,
        password: password
      },
      redirect: 'follow',
      mode: 'no-cors'
    }).then((response) => {
      console.log(response);
    })
    // TODO: Send fetch API post request
  };

  return (<>
    <h1>Household Waste Produce</h1>
    <form onSubmit={handleSubmit}>
      <input
        label="Address"
        variant="filled"
        required
        value={address}
        onChange={e => setAddress(e.target.value)}
      />
      <input
        label="Password"
        variant="filled"
        type="password"
        required
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <div>
        <button variant="contained" onClick={handleClose}>
          Cancel
        </button>
        <button type="submit" variant="contained" color="primary">
          Signup
        </button>
        <RadarChart
      cx={300}
      cy={250}
      outerRadius={150}
      width={500}
      height={500}
      data={data}
    >
      <PolarGrid />
      <PolarAngleAxis dataKey="subject" />
      <PolarRadiusAxis />
      <Radar
        name="Mike"
        dataKey="A"
        stroke="#8884d8"
        fill="#8884d8"
        fillOpacity={0.6}
      />
    </RadarChart>
      </div>
    </form>
  </>);
};

export default Login;
