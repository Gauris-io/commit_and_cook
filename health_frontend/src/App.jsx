import React from 'react';
import DiseaseApp from './DiseaseApp'; // Bringing in your research tool

function App() {
  return (
    <div className="App">
      {/* You can add a global Navbar here later */}
      <DiseaseApp /> 
      {/* This renders everything you built in the other file */}
    </div>
  );
}

export default App;