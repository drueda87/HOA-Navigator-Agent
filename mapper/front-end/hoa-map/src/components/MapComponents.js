import React, { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

mapboxgl.accessToken = "pk.eyJ1IjoiZHJ1ZWRhODciLCJhIjoiY203ZjVnZ3FnMG1pajJxb2g5YmZnY3BjNCJ9.fpQgwsSJLvoE2es3SeYLqQ"; // 🔥 Replace with your token

const MapComponent = () => {
  // 🔥 Hooks must be declared inside the function component
  const mapContainerRef = useRef(null);
  const [map, setMap] = useState(null);
  const [properties, setProperties] = useState([]);
  const [selectedMarker, setSelectedMarker] = useState(null); // ✅ Placed correctly inside function
  const [selectedProperty, setSelectedProperty] = useState(null); // ✅ For side panel
  const markerElement = document.createElement("div");
  markerElement.className = "custom-marker"; // This should match your CSS class
  const selectedMarkerRef = useRef(null); // 🔥 Use a ref to track the selected marker
  const [selectedHOA, setSelectedHOA] = useState(null); 
  console.log(selectedHOA);


  // Fetch property data
  useEffect(() => {
    fetch("http://127.0.0.1:5000/properties") // 🔥 Ensure API is running
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched Properties:", data);
        setProperties(data);
      })
      .catch((error) => console.error("Error fetching properties:", error));
  }, []);

  // Initialize Mapbox map
  useEffect(() => {
    if (!mapContainerRef.current) return;

    const newMap = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [-94.67, 38.99],
      zoom: 10,
    });

    setMap(newMap);
    
    console.log("Map instance:", newMap); // 🔥 Debugging map instance


    return () => newMap.remove();
  }, []);

  // Add markers when properties are available
  useEffect(() => {
      if (!map || properties.length === 0) return;
  
      properties.forEach((property) => {
        const lat = parseFloat(property.latitude);
        const lng = parseFloat(property.longitude);
  
        if (!isNaN(lat) && !isNaN(lng)) {
          const markerElement = document.createElement("div");
          markerElement.className = "custom-marker"; // Style in CSS
  
          const marker = new mapboxgl.Marker({ element: markerElement })
            .setLngLat([lng, lat])
            .setPopup(new mapboxgl.Popup().setHTML(`<h3>${property.address_line1}</h3>`))
            .addTo(map);
  
          // 🔥 Click event to change marker color & open side panel
          markerElement.addEventListener("click", () => {
            if (selectedMarkerRef.current && selectedMarkerRef.current !== markerElement) {
              selectedMarkerRef.current.style.backgroundColor = "blue"; // Reset previous marker to default
            }
            markerElement.style.backgroundColor = "red"; // Highlight selected marker
            selectedMarkerRef.current = markerElement; // Update ref without re-rendering
            setSelectedProperty(property); // Show property details
          });
        } else {
          console.error("Invalid coordinates for property:", property);
        }
      });
    }, [map, properties]);

    
    // 🔥 Add HOA boundary when properties are available
    useEffect(() => {
      console.log("Running HOA Boundary useEffect");
      if (!map || properties.length === 0 || !selectedHOA) return;
    
      const hoaProperties = properties.filter(prop => prop.subdivision === selectedHOA);
    
      if (hoaProperties.length === 0) return;
    
      const latitudes = hoaProperties.map(p => parseFloat(p.latitude));
      const longitudes = hoaProperties.map(p => parseFloat(p.longitude));
    
      const minLat = Math.min(...latitudes);
      const maxLat = Math.max(...latitudes);
      const minLng = Math.min(...longitudes);
      const maxLng = Math.max(...longitudes);
    
      console.log("Latitudes:", latitudes);
      console.log("Longitudes:", longitudes);
      console.log("Min/Max Values:", minLat, maxLat, minLng, maxLng);
    
      const hoaBoundary = {
        type: "Feature",
        geometry: {
          type: "Polygon",
          coordinates: [[
            [minLng, minLat], [maxLng, minLat], [maxLng, maxLat], [minLng, maxLat], [minLng, minLat]
          ]]
        }
      };
    
      console.log("HOA Boundary Data:", hoaBoundary);
    
      // 🛑 REMOVE EXISTING SOURCE & LAYERS BEFORE ADDING NEW ONES
      if (map.getSource("hoa-boundary")) {
        console.log("Removing existing HOA boundary...");
        map.removeLayer("hoa-outline");
        map.removeLayer("hoa-fill");
        map.removeSource("hoa-boundary");
      }
    
      // ✅ ADD UPDATED SOURCE & LAYERS
      map.addSource("hoa-boundary", { type: "geojson", data: hoaBoundary });
    
      map.addLayer({
        id: "hoa-fill",
        type: "fill",
        source: "hoa-boundary",
        layout: {},
        paint: {
          "fill-color": "#0080ff",
          "fill-opacity": 0.2
        }
      });
    
      map.addLayer({
        id: "hoa-outline",
        type: "line",
        source: "hoa-boundary",
        layout: {},
        paint: {
          "line-color": "#0000ff",
          "line-width": 2
        }
      });
    
      console.log("Source Exists:", map.getSource("hoa-boundary"));
      console.log("Layer Exists:", map.getLayer("hoa-outline"));
    
    }, [map, properties, selectedHOA]); // 👈 Runs when `map`, `properties`, or `selectedHOA` changes
    


return (
  <div>
    {/* HOA Dropdown - Allows selection of an HOA */}
    <select onChange={(e) => setSelectedHOA(e.target.value)}>
      <option value="">Select HOA</option>
      {[...new Set(properties.map(p => p.subdivision))].map((hoa, index) => (
        <option key={index} value={hoa}>{hoa || "Unknown HOA"}</option>
      ))}
    </select>

    {/* Map Container */}
    <div ref={mapContainerRef} style={{ width: "100%", height: "500px" }} />

    {/* Side Panel for Selected Property */}
    {selectedProperty && (
      <div className="side-panel">
        <h3>Property Details</h3>
        <p><strong>Address:</strong> {selectedProperty.address_line1}</p>
        <p><strong>City:</strong> {selectedProperty.city}, {selectedProperty.state}</p>
        <p><strong>Zip Code:</strong> {selectedProperty.zip_code}</p>
      </div>
    )}
  </div>
);
;
};

export default MapComponent;
