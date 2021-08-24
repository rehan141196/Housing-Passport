import React, { useState } from "react";
import axios from 'axios';
import '../index.css';

import { useAuth0 } from "@auth0/auth0-react";

export function GetForm(props) {

  // Define Hooks
  const [homes, setHomes] = useState(null);
  const [address, setAddress] = useState(null);
  const [result, setResult] = useState(null);
  const { user } = useAuth0();

  // Get access token from Auth0 for back end request
  const { getAccessTokenSilently } = useAuth0();

  // Get homes for a user
  const handleSubmitUsername = async (evt) => {
      evt.preventDefault();
      const token = await getAccessTokenSilently();
      console.log(token);

      // send request to back end for homes related to the username
      axios.get('http://127.0.0.1:5000/api/getrecord?username=' + user['email'], {headers: {
            Authorization: `Bearer ${token}`,
          }})
        .then((response) => {
          console.log("GET Response")
          console.log(response.data);
          if (response.data["response"] !== "No data found for this user") {
            setHomes(response.data['data']);
          }
          setResult(response.data['response']);
        });
  }

  // Delete home for given user and address
  const handleDelete = async (evt) => {
      evt.preventDefault();

      // Collect the data to be sent in the body
      var bodyFormData = new FormData();
      bodyFormData.append('address', address);
      bodyFormData.append('username', user['email']);

      const token = await getAccessTokenSilently();
      console.log(token);

      setHomes(null);

      // send request to delete property
      axios.post('http://127.0.0.1:5000/api/deleterecord', bodyFormData, {headers: {
          Authorization: `Bearer ${token}`,
        }})
      .then((response) => {
          console.log("POST Response")
          console.log(response);
          setResult(response.data['response']);
      });
      setAddress("");
    }

  return (
    <>
    <form onSubmit={handleSubmitUsername}>
      <input type="submit" value="Get Homes" />
    </form>
    <form onSubmit={handleDelete}>
      <label>
        Address To Remove:
        <input
          type="text"
          value={address}
          onChange={e => setAddress(e.target.value)}
        />
      </label>
      <input type="submit" value="Delete Home" />
    </form>
    <p>User: {user && user['email']}</p>
    <p>Response: {result}</p>

    <div className="homes">
      <ul>
        {homes && homes.map(d => (<ul key={d.address}>
          Property Details:
          <p>
              <li>Username: {d.username}</li>
              <li>Address: {d.address}</li>
              <li>Post Town: {d.post_town}</li>
              <li>Post Code: {d.postcode}</li>
              <li>Residential: {d.residential}</li>
              <li>Type: {d.type}</li>
              <li>EPC: {d.EPC_cert_key}</li>
              <li>Age: {d.age}</li>
              <li>Bedrooms: {d.bedrooms}</li>
              <li>Floor Type: {d.floor_type}</li>
              <li>Floor Insulation: {d.floor_insulation}</li>
              <li>Roof Type: {d.roof_type}</li>
              <li>Roof Insulation: {d.roof_insulation}</li>
              <li>Wall Type: {d.wall_type}</li>
              <li>Wall Insulation: {d.wall_insulation}</li>
              <li>Glaze Type: {d.glaze_type}</li>
              <li>Solar Water Heating: {d.solar_water_heating}</li>
              <li>Solar Panel Area: {d.solar_panel_area}</li>
              <li>Thermostat: {d.thermostat}</li>
              <li>Heating Type: {d.heating_type}</li>
              <li>Heating Fuel: {d.heating_fuel}</li>
              <li>Gas Connection: {d.gas_connection}</li>
              <li>Hotwater Type: {d.hotwater_type}</li>
              <li>Low Energy Light Percentage: {d.low_energy_light_pct}%</li>
              <li>Average Temperature: {d.average_temp}</li>
              <li>Number of Smart Meters: {d.smart_meters}</li>
              <li>Smart Meter IDs: {d.smart_meter_ids}</li>
              <li>Photovoltaics: {d.photovoltaics}</li>
            </p></ul>))} 
      </ul>
    </div>
    </>
  );
}