import React, { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";


mapboxgl.accessToken = "pk.eyJ1IjoiZHJ1ZWRhODciLCJhIjoiY203ZjVnZ3FnMG1pajJxb2g5YmZnY3BjNCJ9.fpQgwsSJLvoE2es3SeYLqQ"; // 🔥 Replace with your token

const MapComponent = () => {
  const mapContainerRef = useRef(null);
  const [map, setMap] = useState(null);
  const [properties, setProperties] = useState([]);

  // Fetch property data from API
  useEffect(() => {
    fetch("http://127.0.0.1:5000/properties") // 🔥 Ensure API is running
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched Properties:", data); // 🔥 Debugging
        setProperties(data); // Store property data
      })
      .catch((error) => console.error("Error fetching properties:", error));
  }, []);

  // Initialize Mapbox map
  useEffect(() => {
    if (!mapContainerRef.current) return;

    const newMap = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [-94.67, 38.99], // Default center (Overland Park, KS)
      zoom: 10,
    });

    setMap(newMap);

    return () => newMap.remove(); // Cleanup on unmount
  }, []);

  // Add markers when properties are available
  useEffect(() => {
    if (!map || properties.length === 0) return;

    properties.forEach((property) => {
      const lat = parseFloat(property.latitude); // 🔥 Ensure it's a number
      const lng = parseFloat(property.longitude);

      if (!isNaN(lat) && !isNaN(lng)) { // 🔥 Ensure values are valid before adding markers
        new mapboxgl.Marker()
          .setLngLat([lng, lat]) // Longitude first!
          .setPopup(new mapboxgl.Popup().setHTML(`<h3>${property.address_line1}</h3>`)) // Popup with address
          .addTo(map);
      } else {
        console.error("Invalid coordinates for property:", property);
      }
    });
  }, [map, properties]);

  return <div ref={mapContainerRef} style={{ width: "100%", height: "700px" }} />;
};

export default MapComponent;
