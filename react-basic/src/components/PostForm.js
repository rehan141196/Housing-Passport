import React, { useState } from "react";
import axios from 'axios';
import '../index.css';

import { useAuth0 } from "@auth0/auth0-react";

export function PostForm(props) {

  // Define the Hooks
  const [address, setAddress] = useState("");
  const [posttown, setPosttown] = useState("");
  const [postcode, setPostcode] = useState("");
  const [residential, setResidential] = useState("");
  const [type, setType] = useState("");
  const [epc, setEpc] = useState("");
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
  const [avgtemp, setAvgtemp] = useState("");
  const [smartmeters, setSmartmeters] = useState("");
  const [smartmeterids, setSmartmeterids] = useState("");
  const [photovoltaics, setPhotovoltaics] = useState("");

  const { user } = useAuth0();
  const { getAccessTokenSilently } = useAuth0();
  
  // Add the data from the fields into the body of the request
  const handleSubmit = async (evt) => {
      evt.preventDefault();

      var bodyFormData = new FormData();
      bodyFormData.append('username', user['email']);
      bodyFormData.append('address', address);
      bodyFormData.append('post_town', posttown);
      bodyFormData.append('postcode', postcode);
      bodyFormData.append('residential', residential);
      bodyFormData.append('type', type);
      bodyFormData.append('EPC_cert_key', epc);
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
      bodyFormData.append('average_temp', avgtemp);
      bodyFormData.append('smart_meters', smartmeters);
      bodyFormData.append('smart_meter_ids', smartmeterids);
      bodyFormData.append('photovoltaics', photovoltaics);

      // Get access token from Auth0 for the request to back end
      const token = await getAccessTokenSilently();
      console.log(token);

      axios.post('http://127.0.0.1:5000/api/addrecord', bodyFormData, {headers: {
          Authorization: `Bearer ${token}`,
        }})
      .then((response) => {
          console.log("Post Response")
          console.log(response);
      });
  	}

  return (
    <>
    <form onSubmit={handleSubmit}>
      <label>
        Address:
        <input
          type="text"
          value={address}
          onChange={e => setAddress(e.target.value)}
        />
      </label>
      <label>
        Post Town:
        <input
          type="text"
          value={posttown}
          onChange={e => setPosttown(e.target.value)}
        />
      </label>
      <label>
        Post Code:
        <input
          type="text"
          value={postcode}
          onChange={e => setPostcode(e.target.value)}
        />
      </label>
      <label>
        Residential:
        <select value={residential} onChange={e => setResidential(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
        </select>
      </label>
      <label>
        Type:
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
        EPC Certificate Key:
        <input
          type="text"
          value={epc}
          onChange={e => setEpc(e.target.value)}
        />
      </label>
      <label>
        Age:
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
        Bedrooms:
        <input
          type="text"
          value={bedrooms}
          onChange={e => setBedrooms(e.target.value)}
        />
      </label>
      <label>
        Floor Type:
        <select value={floortype} onChange={e => setFloortype(e.target.value)}>
            <option value="">Select</option>
            <option value="Suspended">Suspended</option>
            <option value="Solid">Solid</option>
            <option value="(another dwelling below)">Another Dwelling Below</option>
        </select>
      </label>
      <label>
        Floor Insulation:
        <select value={floorinsulation} onChange={e => setFloorinsulation(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
            <option value="Limited">Limited</option>
        </select>
      </label>
      <label>
        Roof Type:
        <select value={rooftype} onChange={e => setRooftype(e.target.value)}>
            <option value="">Select</option>
            <option value="Pitched">Pitched</option>
            <option value="Flat">Flat</option>
            <option value="(another dwelling above)">Another Dwelling Above</option>
        </select>
      </label>
      <label>
        Roof Insulation:
        <select value={roofinsulation} onChange={e => setRoofinsulation(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
            <option value="Limited">Limited</option>
        </select>
      </label>
      <label>
        Wall Type:
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
        Wall Insulation:
        <select value={wallinsulation} onChange={e => setWallinsulation(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
            <option value="Partial">Partial</option>
        </select>
      </label>
      <label>
        Glaze Type:
        <select value={glazetype} onChange={e => setGlazetype(e.target.value)}>
            <option value="">Select</option>
            <option value="Single">Single</option>
            <option value="Double">Double</option>
            <option value="Triple">Triple</option>
            <option value="Unknown">Unknown</option>
        </select>
      </label>
      <label>
        Solar Water Heating:
        <select value={solarwaterheating} onChange={e => setSolarwaterheating(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
        </select>
      </label>
      <label>
        Solar Panel Area:
        <select value={solarpanelarea} onChange={e => setSolarpanelarea(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
        </select>
      </label>
      <label>
        Thermostat:
        <select value={thermostat} onChange={e => setThermostat(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
            <option value="Other">Other</option>
        </select>
      </label>
      <label>
        Heating Type:
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
        Heating Fuel:
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
      <label>
        Gas Connection:
        <select value={gasconnection} onChange={e => setGasconnection(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
        </select>
      </label>
      <label>
        Hotwater Type:
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
      <label>
        Low Energy Light Percentage:
        <input
          type="text"
          value={lowenergylightpct}
          onChange={e => setLowenergylightpct(e.target.value)}
        />
      </label>
      <label>
        Average Temperature:
        <input
          type="text"
          value={avgtemp}
          onChange={e => setAvgtemp(e.target.value)}
        />
      </label>
      <label>
        Number of Smart Meters:
        <input
          type="text"
          value={smartmeters}
          onChange={e => setSmartmeters(e.target.value)}
        />
      </label>
      <label>
        Smart Meter IDs:
        <input
          type="text"
          value={smartmeterids}
          onChange={e => setSmartmeterids(e.target.value)}
        />
      </label>
      <label>
        Photovoltaics:
        <select value={photovoltaics} onChange={e => setPhotovoltaics(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Yes</option>
            <option value="False">No</option>
        </select>
      </label>
      <input type="submit" value="Submit" />
    </form>
    </>
  );
}