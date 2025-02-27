import React, { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { TextField, Button, Select, MenuItem, Card, CardContent, CardHeader, Typography } from "@mui/material";
import Autocomplete from "@mui/material/Autocomplete";
import { FormControl, InputLabel } from "@mui/material";


mapboxgl.accessToken = "pk.eyJ1IjoiZHJ1ZWRhODciLCJhIjoiY203ZjVnZ3FnMG1pajJxb2g5YmZnY3BjNCJ9.fpQgwsSJLvoE2es3SeYLqQ"; // Replace with your actual token

const MapComponent = () => {
  const mapContainerRef = useRef(null);
  const [map, setMap] = useState(null);
  const [properties, setProperties] = useState([]);
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [selectedHOA, setSelectedHOA] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [message, setMessage] = useState("");
  const selectedMarkerRef = useRef(null); // 🔹 FIX: Added useRef to track selected marker
  const [filteredProperties, setFilteredProperties] = useState([]);

  // Handle search input change
  const handleSearchChange = (event, value) => {
    setSearchQuery(value);

    // Filter properties based on input
    if (value.length > 1) {
      const results = properties.filter((prop) =>
        prop.address_line1.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredProperties(results);
    } else {
      setFilteredProperties([]);
    }
  };

  // Zoom to selected property
  const handleSelectProperty = (event, value) => {
    if (!value) return;
    const selected = properties.find((prop) => prop.address_line1 === value);
    if (selected) {
      map.flyTo({
        center: [parseFloat(selected.longitude), parseFloat(selected.latitude)],
        zoom: 16
      });
    }
  };

  // Fetch property data
  useEffect(() => {
    fetch("http://127.0.0.1:5000/properties")
      .then((response) => response.json())
      .then((data) => {
        setProperties(data);
      })
      .catch((error) => console.error("Error fetching properties:", error));
  }, []);

  // Initialize Mapbox
  useEffect(() => {
    if (!mapContainerRef.current) return;

    const newMap = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [-94.67, 38.99],
      zoom: 10,
    });

    setMap(newMap);
    return () => newMap.remove();
  }, []);

// Add markers and HOA boundary
useEffect(() => {
  if (!map || properties.length === 0) return;

  // Remove previous HOA boundary (optional, ensures it updates correctly)
  if (map.getLayer("hoa-outline")) {
    map.removeLayer("hoa-outline");
  }
  if (map.getSource("hoa-boundary")) {
    map.removeSource("hoa-boundary");
  }

  // 🔹 Filter properties for the selected HOA
  if (selectedHOA) {
    const hoaProperties = properties.filter(prop => prop.subdivision === selectedHOA);

    if (hoaProperties.length > 0) {
      const latitudes = hoaProperties.map(p => parseFloat(p.latitude));
      const longitudes = hoaProperties.map(p => parseFloat(p.longitude));

      const minLat = Math.min(...latitudes);
      const maxLat = Math.max(...latitudes);
      const minLng = Math.min(...longitudes);
      const maxLng = Math.max(...longitudes);

      const hoaBoundary = {
        type: "Feature",
        geometry: {
          type: "Polygon",
          coordinates: [[
            [minLng, minLat], [maxLng, minLat], [maxLng, maxLat], [minLng, maxLat], [minLng, minLat]
          ]]
        }
      };

      // Add HOA boundary source and layer with blue background fill
      map.addSource("hoa-boundary", { type: "geojson", data: hoaBoundary });
        map.addLayer({
          id: "hoa-fill",
          type: "fill",
          source: "hoa-boundary",
          layout: {},
          paint: {
            "fill-color": "#0000ff", // Blue background
            "fill-opacity": 0.2 // Adjust opacity for visibility
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

    }
  }

  // 🔹 Add custom markers for each property
  properties.forEach((property) => {
    const lat = parseFloat(property.latitude);
    const lng = parseFloat(property.longitude);

    if (!isNaN(lat) && !isNaN(lng)) {
      // Create a custom marker element
      const markerElement = document.createElement("div");
      markerElement.className = "custom-marker"; // 🔹 Uses your index.css class

      // Create a Mapbox marker with the custom element (NO POPUP)
      const marker = new mapboxgl.Marker({ element: markerElement })
        .setLngLat([lng, lat])
        .addTo(map);

      // 🔥 Click event to change marker color & open details
      markerElement.addEventListener("click", () => {
        if (selectedMarkerRef.current && selectedMarkerRef.current !== markerElement) {
          selectedMarkerRef.current.style.backgroundColor = "blue"; // Reset previous marker
        }
        markerElement.style.backgroundColor = "red"; // Highlight selected marker
        selectedMarkerRef.current = markerElement; // Update ref without re-rendering
        setSelectedProperty(property); // Show property details
      });
    }
  });

}, [map, properties, selectedHOA]); // Runs when map, properties, or HOA changes

const [chatInput, setChatInput] = useState("");

return (
  <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
    {/* Header Section */}
    <header style={{ padding: "16px", borderBottom: "1px solid #ccc", display: "flex", alignItems: "center", gap: "10px" }}>
    </header>

    {/* Main Content Section */}
    <main style={{ display: "flex", gap: "16px", flex: 1, padding: "16px" }}>
      {/* Left Section: Map and Filters */}
      <div style={{ flex: 2, display: "flex", flexDirection: "column" }}>
        {/* Search & HOA Dropdown */}
        <div style={{ display: "flex", gap: "16px", marginBottom: "16px" }}>
          <Autocomplete
            options={properties}
            getOptionLabel={(option) => option.address_line1 || ""}
            renderInput={(params) => <TextField {...params} label="Search Property" variant="outlined" fullWidth />}
            value={searchQuery}
            onChange={(event, newValue) => setSearchQuery(newValue)}
            style={{ flex: 1 }}
          />
          <Select value={selectedHOA} onChange={(e) => setSelectedHOA(e.target.value)} displayEmpty>
            <MenuItem value="">Select HOA</MenuItem>
            {[...new Set(properties.map(p => p.subdivision))].map((hoa, index) => (
              <MenuItem key={index} value={hoa}>{hoa || "Unknown HOA"}</MenuItem>
            ))}
          </Select>
        </div>

        {/* Map Section */}
        <div ref={mapContainerRef} style={{ width: "100%", height: "550px", borderRadius: "8px", background: "#eee" }} />
      </div>

      {/* Right Section: Property Details and Chat */}
      <div style={{ flex: 1.2, display: "flex", flexDirection: "column", maxHeight: "600px", gap: "16px" }}>
        {/* Property Details */}
        <Card style={{ flex: 0.6 }}>
          <CardHeader title="Property Details" />
          <CardContent>
            {selectedProperty ? (
              <>
                <Typography variant="subtitle2">Address</Typography>
                <Typography>{selectedProperty.address_line1}</Typography>
                <Typography>{selectedProperty.city}, {selectedProperty.state} {selectedProperty.zip_code}</Typography>
                <Typography variant="subtitle2" sx={{ mt: 2 }}>HOA</Typography>
                <Typography>{selectedProperty.subdivision || "N/A"}</Typography>
              </>
            ) : (
              <Typography>No property selected</Typography>
            )}
          </CardContent>
        </Card>

        {/* Navigator Chat Agent */}
        <Card style={{ flex: 1 }}>
          <CardHeader title="Navigator Agent" />
          <CardContent>
            <div style={{ height: "150px", background: "#f5f5f5", padding: "8px", borderRadius: "8px", overflowY: "auto" }}>
              {/* Chat messages go here */}
            </div>
            <div style={{ display: "flex", gap: "8px", marginTop: "8px" }}>
              <TextField
                variant="outlined"
                placeholder="Ask about the HOA..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                fullWidth
              />
              <Button variant="contained" color="primary">Send</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  </div>
);

};

export default MapComponent;
