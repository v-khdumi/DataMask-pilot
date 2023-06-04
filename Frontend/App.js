import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';
import RecipeGenerator from './components/RecipeGenerator';

function App() {
  return (
    <Router>
      <div className="App">
        <Route path="/register" component={RegistrationForm} />
        <Route path="/login" component={LoginForm} />
        <Route path="/generate" component={RecipeGenerator} />
      </div>
    </Router>
  );
}

export default App;
