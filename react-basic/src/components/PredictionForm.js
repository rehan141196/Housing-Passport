import React, { useState } from "react";
import axios from 'axios';
import '../index.css';

export function PredictionForm(props) {

  // Define Hooks
  const [posttown, setPosttown] = useState("");
  const [type, setType] = useState("");
  const [age, setAge] = useState("");
  const [bedrooms, setBedrooms] = useState("");
  const [floortype, setFloortype] = useState("");
  const [floorinsulation, setFloorinsulation] = useState("");
  const [rooftype, setRooftype] = useState("");
  const [roofinsulation, setRoofinsulation] = useState("");
  const [walltype, setWalltype] = useState("");
  const [wallinsulation, setWallinsulation] = useState("");
  const [glazetype, setGlazetype] = useState("");
  const [solarwaterheating, setSolarwaterheating] = useState("");
  const [solarpanelarea, setSolarpanelarea] = useState("");
  const [thermostat, setThermostat] = useState("");
  const [heatingtype, setHeatingtype] = useState("");
  const [heatingfuel, setHeatingfuel] = useState("");
  const [gasconnection, setGasconnection] = useState("");
  const [hotwatertype, setHotwatertype] = useState("");
  const [lowenergylightpct, setLowenergylightpct] = useState("");

  const [response, setResponse] = useState(null);
  const [result, setResult] = useState(null);
  
  
  const handleSubmit = async (evt) => {
      evt.preventDefault();

      // Collect the data to be sent in the body
      var bodyFormData = new FormData();
      bodyFormData.append('post_town', posttown);
      bodyFormData.append('type', type);
      bodyFormData.append('age', age);
      bodyFormData.append('bedrooms', bedrooms);
      bodyFormData.append('floor_type', floortype);
      bodyFormData.append('floor_insulation', floorinsulation);
      bodyFormData.append('roof_type', rooftype);
      bodyFormData.append('roof_insulation', roofinsulation);
      bodyFormData.append('wall_type', walltype);
      bodyFormData.append('wall_insulation', wallinsulation);
      bodyFormData.append('glaze_type', glazetype);
      bodyFormData.append('solar_water_heating', solarwaterheating);
      bodyFormData.append('solar_panel_area', solarpanelarea);
      bodyFormData.append('thermostat', thermostat);
      bodyFormData.append('heating_type', heatingtype);
      bodyFormData.append('heating_fuel', heatingfuel);
      bodyFormData.append('gas_connection', gasconnection);
      bodyFormData.append('hotwater_type', hotwatertype);
      bodyFormData.append('low_energy_light_pct', lowenergylightpct);

      // Send the request for prediction to back end
      axios.post('http://127.0.0.1:5000/api/predictefficiency', bodyFormData)
      .then((response) => {
          console.log("Post Response")
          console.log(response);
          setResponse(response.data['response']);
          setResult(response.data['efficiency_score']);
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
      </label><br />
      <br />
      <label>
        Type:&ensp;
        <select value={type} onChange={e => setType(e.target.value)}>
            <option value="">Select</option>
            <option value="Flat">Flat</option>
            <option value="House">House</option>
            <option value="Bungalow">Bungalow</option>
            <option value="Maisonette">Maisonette</option>
            <option value="Park home">Park Home</option>
        </select>
      </label>
      <label>
        &emsp;Age:&ensp;
        <select value={age} onChange={e => setAge(e.target.value)}>
            <option value="">Select</option>
            <option value="before 1900">Before 1900</option>
            <option value="1900-1929">1900-1929</option>
            <option value="1930-1949">1930-1949</option>
            <option value="1950-1966">1950-1966</option>
            <option value="1967-1975">1967-1975</option>
            <option value="1976-1982">1976-1982</option>
            <option value="1983-1990">1983-1990</option>
            <option value="1991-1995">1991-1995</option>
            <option value="1996-2002">1996-2002</option>
            <option value="2003-2006">2003-2006</option>
            <option value="2007 onwards">2007 onwards</option>
            <option value="unknown">Unknown</option>
        </select>
      </label>
      <label>
        &emsp;Bedrooms:&ensp;
        <input
          type="text"
          value={bedrooms}
          onChange={e => setBedrooms(e.target.value)}
        />
      </label><br />
      <br />
      <label>
        Floor Type:&ensp;
        <select value={floortype} onChange={e => setFloortype(e.target.value)}>
            <option value="">Select</option>
            <option value="Suspended">Suspended</option>
            <option value="Solid">Solid</option>
            <option value="(another dwelling below)">Another Dwelling Below</option>
        </select>
      </label>
      <label>
        &emsp;Floor Insulation:&ensp;
        <select value={floorinsulation} onChange={e => setFloorinsulation(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
            <option value="Limited">Limited</option>
        </select>
      </label>
      <label><br />
      <br />
        Roof Type:&ensp;
        <select value={rooftype} onChange={e => setRooftype(e.target.value)}>
            <option value="">Select</option>
            <option value="Pitched">Pitched</option>
            <option value="Flat">Flat</option>
            <option value="(another dwelling above)">Another Dwelling Above</option>
        </select>
      </label>
      <label>
        &emsp;Roof Insulation:&ensp;
        <select value={roofinsulation} onChange={e => setRoofinsulation(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
            <option value="Limited">Limited</option>
        </select>
      </label>
      <label><br />
      <br />
        Wall Type:&ensp;
        <select value={walltype} onChange={e => setWalltype(e.target.value)}>
            <option value="">Select</option>
            <option value="Cavity">Cavity</option>
            <option value="Solid brick">Solid Brick</option>
            <option value="Timber">Timber</option>
            <option value="Sandstone">Sandstone</option>
            <option value="System built">System Built</option>
        </select>
      </label>
      <label>
        &emsp;Wall Insulation:&ensp;
        <select value={wallinsulation} onChange={e => setWallinsulation(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
            <option value="Partial">Partial</option>
        </select>
      </label>
      <label><br />
      <br />
        Glaze Type:&ensp;
        <select value={glazetype} onChange={e => setGlazetype(e.target.value)}>
            <option value="">Select</option>
            <option value="Single">Single</option>
            <option value="Double">Double</option>
            <option value="Triple">Triple</option>
            <option value="Unknown">Unknown</option>
        </select>
      </label>
      <label><br />
      <br />
        Solar Water Heating:&ensp;
        <select value={solarwaterheating} onChange={e => setSolarwaterheating(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
        </select>
      </label>
      <label>
        &emsp;Solar Panel Area:&ensp;
        <select value={solarpanelarea} onChange={e => setSolarpanelarea(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
        </select>
      </label>
      <label><br />
      <br />
        Thermostat:&ensp;
        <select value={thermostat} onChange={e => setThermostat(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
            <option value="Other">Other</option>
        </select>
      </label>
      <label>
        &emsp;Heating Type:&ensp;
        <select value={heatingtype} onChange={e => setHeatingtype(e.target.value)}>
            <option value="">Select</option>
            <option value="Boiler">Boiler</option>
            <option value="Electric">Electric</option>
            <option value="Community scheme">Community Scheme</option>
            <option value="Room heaters">Room Heaters</option>
            <option value="Air">Air</option>
            <option value="Heat pump">Heat Pump</option>
            <option value="Underfloor">Underfloor</option>
            <option value="No system">No System</option>
        </select>
      </label>
      <label>
        &emsp;Heating Fuel:&ensp;
        <select value={heatingfuel} onChange={e => setHeatingfuel(e.target.value)}>
            <option value="">Select</option>
            <option value="Mains gas">Mains Gas</option>
            <option value="Electric">Electric</option>
            <option value="Oil">Oil</option>
            <option value="LPG">LPG</option>
            <option value="Dual">Dual</option>
            <option value="Coal">Coal</option>
            <option value="Wood">Wood</option>
            <option value="Bio">Bio</option>
            <option value="Community heating schemes">Community Heating Schemes</option>
            <option value="No heating">No Heating</option>
            <option value="Unknown">Unknown</option>
        </select>
      </label>
      <label><br />
      <br />
        Gas Connection:&ensp;
        <select value={gasconnection} onChange={e => setGasconnection(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
        </select>
      </label>
      <label>
        &emsp;Hotwater Type:&ensp;
        <select value={hotwatertype} onChange={e => setHotwatertype(e.target.value)}>
            <option value="">Select</option>
            <option value="From main">From Main</option>
            <option value="Electric">Electric</option>
            <option value="Community scheme">Community Scheme</option>
            <option value="Gas">Gas</option>
            <option value="Secondary system">Secondary System</option>
            <option value="No system">No System</option>
        </select>
      </label>
      <label><br />
      <br />
        Low Energy Light Percentage:&ensp;
        <input
          type="text"
          value={lowenergylightpct}
          onChange={e => setLowenergylightpct(e.target.value)}
        />
      </label><br />
      <br />
      <input type="submit" value="Submit" />
    </form>
    <div className="result">
    <p>Response: {response}</p>
    <p>Predicted Energy Efficiency Score: {result}</p>
    </div>
    </>
  );
}