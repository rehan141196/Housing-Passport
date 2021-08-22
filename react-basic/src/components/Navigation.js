import React from 'react';
 
import { NavLink } from 'react-router-dom';

// Links to the different parts of the website 
 
const Navigation = () => {
    return (
       <div>
          <NavLink to="/">Home</NavLink>
          <NavLink to="/GetForm">Get Form</NavLink>
          <NavLink to="/PostForm">Post Form</NavLink>
          <NavLink to="/AggregateForm">Aggregate Form</NavLink>
          <NavLink to="/PredictionForm">Prediction Form</NavLink>
       </div>
    );
}
 
export default Navigation;