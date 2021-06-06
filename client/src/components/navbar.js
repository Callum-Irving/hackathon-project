import './navbar.css';
import { Link } from 'react-router-dom';

function Navbar() {
	return (
		<div className="navbar">
			<Link to="/" className="home-link">
				<h1>Name Goes Here</h1>
			</Link>
			<ul className="link-group">
				<Link to="/data_visualization">
					<button className="navlink">View Data</button>
				</Link>
				<Link to="/login">
					<button className="navlink">Login</button>
				</Link>
			</ul>
		</div>
	);
}

// TODO: If logged in, make this say "Logout"

export default Navbar;
