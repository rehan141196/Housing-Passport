import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import ReactDOM from 'react-dom';
import Auth0ProviderWithHistory from './auth/auth0-provider-with-history';

import Home from './components/Home';
import { GetForm } from './components/GetForm';
import { PostForm } from './components/PostForm';
import { AggregateForm } from './components/AggregateForm';
import Error from './components/Error';
import Navigation from './components/Navigation';
import ProtectedRoute from './auth/protected-route';

ReactDOM.render((
  <BrowserRouter>
    <Auth0ProviderWithHistory>
    <div>
      <Navigation />
        <Switch>
          <Route path="/" component={Home} exact/>
          <ProtectedRoute path="/GetForm" component={GetForm}/>
          <ProtectedRoute path="/PostForm" component={PostForm}/>
          <ProtectedRoute path="/AggregateForm" component={AggregateForm}/>
        <Route component={Error}/>
        </Switch>
    </div> 
    </Auth0ProviderWithHistory>
  </BrowserRouter>),
document.getElementById('root')
);