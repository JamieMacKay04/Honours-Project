import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Landing from './Landing';
import Login from './Login';
import Signup from './Signup';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
            </Routes>
        </Router>
    );
}

export default App;
