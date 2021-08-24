import React, { useState } from "react";
import axios from 'axios';
import '../index.css';

import { useAuth0 } from "@auth0/auth0-react";

export function AggregateForm(props) {

  // Define Hooks
  const [posttown, setPosttown] = useState("");
  const [field, setField] = useState("type");
  const [result, setResult] = useState(null);
  const [response, setResponse] = useState(null);

  const { getAccessTokenSilently } = useAuth0();
  
  // Get access token from Auth0 for back end request
  const handleSubmit = async (evt) => {
      evt.preventDefault();
      const token = await getAccessTokenSilently();
      console.log(token);

      // Send request to backend with appropriate parameters
      axios.get('http://127.0.0.1:5000/api/aggregate/by_field?post_town=' + posttown.toUpperCase() + '&field=' + field, {headers: {
            Authorization: `Bearer ${token}`,
          }})
        .then((response) => {
          console.log("GET Response")
          console.log(response.data);
          setResponse(response.data['response']);
          setResult(response.data['results']);
        });
  }

  return (
    <>
    <br />
    <form onSubmit={handleSubmit}>
      <label>
        Post Town:&ensp;
        <input
          type="text"
          value={posttown}
          onChange={e => setPosttown(e.target.value)}
        />
      </label>
      <label><br />
      <br />
        Field:&ensp;
        <select value={field} onChange={e => setField(e.target.value)}>
            <option value="type">Type</option>
            <option value="age">Age</option>
            <option value="floor_type">Floor Type</option>
            <option value="floor_insulation">Floor Insulation</option>
            <option value="roof_type">Roof Type</option>
            <option value="roof_insulation">Roof Insulation</option>
            <option value="wall_type">Wall Type</option>
            <option value="wall_insulation">Wall Insulation</option>
            <option value="glaze_type">Glaze Type</option>
            <option value="solar_water_heating">Solar Water Heating</option>
            <option value="solar_panel_area">Solar Panel Area</option>
            <option value="thermostat">Thermostat</option>
            <option value="heating_type">Heating Type</option>
            <option value="heating_fuel">Heating Fuel</option>
            <option value="gas_connection">Gas Connection</option>
            <option value="hotwater_type">Hotwater Type</option>
            <option value="photovoltaics">Photovoltaics</option>
        </select>
      </label><br />
      <br />
      <input type="submit" value="Submit" />
    </form>
    <div className="result">
    <p>Response: {response}</p>
    <p>Homes in Post Town: {result && result['Homes in Post Town']}</p>
    {result && delete result['Homes in Post Town']}
      <ul>
      {result && Object.entries(result).map(([key, value]) => {
            return <li key={key}>{key.replace(/\(|\)/g, '').slice(0,1).toUpperCase() + key.replace(/\(|\)/g, '').slice(1, key.length)}: {value}</li> 
          })}
      </ul>
    </div>
    </>
  );
}