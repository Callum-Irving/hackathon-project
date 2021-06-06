import React, { useState } from 'react';
import './LoginForm.css';

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

  return (
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
      </div>
    </form>
  );
};

export default Login;
