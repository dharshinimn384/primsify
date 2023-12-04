import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Link, Routes, Route } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';
import { TransitionGroup, CSSTransition } from 'react-transition-group';
import { googleLogout, useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import Chatbot from './components/chatbot';
import textimg from './components/textimg'
import './App.css'; // Create a separate CSS file for styling

const App = () => {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);

  const login = useGoogleLogin({
    onSuccess: (codeResponse) => setUser(codeResponse),
    onError: (error) => console.log('Login Failed:', error),
  });

  useEffect(() => {
    if (user) {
      axios
        .get(`https://www.googleapis.com/oauth2/v1/userinfo?access_token=${user.access_token}`, {
          headers: {
            Authorization: `Bearer ${user.access_token}`,
            Accept: 'application/json',
          },
        })
        .then((res) => {
          setProfile(res.data);
        })
        .catch((err) => console.log(err));
    }
  }, [user]);

  const logOut = () => {
    googleLogout();
    setProfile(null);
  };

  const profilePictureAnimation = useSpring({
    opacity: profile ? 1 : 0,
    transform: profile ? 'translateY(0)' : 'translateY(-20px)',
  });

  return (
    <Router>
      <div className="container">
        <nav className="sidebar">
          <Link to="/" className="logo">
            Prismify
          </Link>
          <Link to="/SketchDazzle" className="nav-link">
            SketchDazzle
          </Link>
          <Link to="/VisionScribe" className="nav-link">
            Visionscribe
          </Link>
        </nav>

        <main className="content">
          <TransitionGroup>
            <CSSTransition key={window.location.key} classNames="fade" timeout={300}>
              <animated.div
                style={{
                  ...profilePictureAnimation,
                  position: 'fixed',
                  top: '10px',
                  right: '10px',
                  zIndex: 999,
                }}
              >
                {profile && (
                  <img
                    src={profile.picture}
                    alt="user"
                    className="profile-picture"
                  />
                )}
              </animated.div>
            </CSSTransition>
          </TransitionGroup>

          {profile ? (
            <div className="user-info">
              
              <button className="logout-btn" onClick={logOut}>
                Log out
              </button>
            </div>
          ) : (
            <button className="login-btn" onClick={() => login()}>
              Sign in with Google 🚀
            </button>
          )}

          <h1 className="welcome-message">Hello! 🤖 Let's chat:</h1>
          <Routes>
            <Route path="/SketchDazzle" element={<Chatbot />} />
            <Route path="/VisionScribe" element={<textimg />} />

          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
