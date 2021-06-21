import React, { useState } from "react";
import axios from 'axios';
import '../index.css';

export function GetForm(props) {
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [homes, setHomes] = useState(null);
  
  const handleSubmitUsername = (evt) => {
      evt.preventDefault();
      axios.get('http://127.0.0.1:5000/api/getrecord?username=' + name)
        .then((response) => {
          console.log("GET Response")
          console.log(response.data);
          setHomes(response.data);
          setName("");
        })
  }

  const handleSubmitAddress = (evt) => {
      evt.preventDefault();
      axios.get('http://127.0.0.1:5000/api/getrecordbyaddress?address=' + address)
        .then((response) => {
          console.log("GET Response")
          console.log(response.data);
          setHomes(response.data);
          setAddress("");
        })
  }

  return (
    <>
    <form onSubmit={handleSubmitUsername}>
      <label>
        Username:
        <input
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
        />
      </label>
      <input type="submit" value="Submit" />
    </form>
    <form onSubmit={handleSubmitAddress}>
      <label>
        Address:
        <input
          type="text"
          value={address}
          onChange={e => setAddress(e.target.value)}
        />
      </label>
      <input type="submit" value="Submit" />
    </form>
    <div className="homes">
          <div className="details">
                  <p>Username: {homes && homes['data']['username']}</p>
                  <p>Address: {homes && homes['data']['address']}</p>
                  <p>Post Town: {homes && homes['data']['post_town']}</p>
                  <p>Post Code: {homes && homes['data']['postcode']}</p>
                  <p>Residential: {homes && homes['data']['residential']}</p>
                  <p>Type: {homes && homes['data']['type']}</p>
                  <p>EPC: {homes && homes['data']['EPC_cert_key']}</p>
                  <p>Age: {homes && homes['data']['age']}</p>
                  <p>Bedrooms: {homes && homes['data']['bedrooms']}</p>
                  <p>Floor Type: {homes && homes['data']['floor_type']}</p>
                  <p>Floor Insulation: {homes && homes['data']['floor_insulation']}</p>
                  <p>Roof Type: {homes && homes['data']['roof_type']}</p>
                  <p>Roof Insulation: {homes && homes['data']['roof_insulation']}</p>
                  <p>Wall Type: {homes && homes['data']['wall_type']}</p>
                  <p>Wall Insulation: {homes && homes['data']['wall_insulation']}</p>
                  <p>Glaze Type: {homes && homes['data']['glaze_type']}</p>
                  <p>Solar Water Heating: {homes && homes['data']['solar_water_heating']}</p>
                  <p>Solar Panel Area: {homes && homes['data']['solar_panel_area']}</p>
                  <p>Thermostat: {homes && homes['data']['thermostat']}</p>
                  <p>Heating Type: {homes && homes['data']['heating_type']}</p>
                  <p>Heating Fuel: {homes && homes['data']['heating_fuel']}</p>
                  <p>Gas Connection: {homes && homes['data']['gas_connection']}</p>
                  <p>Hotwater Type: {homes && homes['data']['hotwater_type']}</p>
                  <p>Low Energy Light Percentage: {homes && homes['data']['low_energy_light_pct']}%</p>
                  <p>Average Temperature: {homes && homes['data']['average_temp']}</p>
                  <p>Number of Smart Meters: {homes && homes['data']['smart_meters']}</p>
                  <p>Smart Meter IDs: {homes && homes['data']['smart_meter_ids']}</p>
                  <p>Photovoltaics: {homes && homes['data']['photovoltaics']}</p>     
          </div>
    </div>
    </>
  );
}