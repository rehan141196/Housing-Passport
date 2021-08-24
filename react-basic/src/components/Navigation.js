import React from 'react';
 
import { NavLink } from 'react-router-dom';

// Links to the different parts of the website 
 
const Navigation = () => {
    return (
       <div>
          <NavLink to="/">Home</NavLink>&ensp;
          &ensp;<NavLink to="/GetForm">Get Form</NavLink>&ensp;
          &ensp;<NavLink to="/PostForm">Post Form</NavLink>&ensp;
          &ensp;<NavLink to="/AggregateForm">Aggregate Form</NavLink>&ensp;
          &ensp;<NavLink to="/PredictionForm">Prediction Form</NavLink>&ensp;
       </div>
    );
}
 
export default Navigation;