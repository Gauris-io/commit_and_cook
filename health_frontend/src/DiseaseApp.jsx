import React, { useState, useEffect } from 'react';

const DiseaseApp = () => {
  const [data, setData] = useState({ molecules: [], recipes: [], nutrients: {} });
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState('Diabetes');

  const fetchData = async (disease) => {
    setLoading(true);
    setSelected(disease);
    try {
      const response = await fetch(`http://localhost:5000/api/research?disease=${disease}`);
      const result = await response.json();
      if (result.success) setData(result);
    } catch (e) { console.error("Fetch Error:", e); }
    setLoading(false);
  };

  useEffect(() => { fetchData('Diabetes'); }, []);

  return (
    <div className="container">
      <div className="card">
        <h3>1. Select Condition</h3>
        <div className="button-group">
          {["Diabetes", "Hypertension", "Obesity", "Celiac", "PCOS", "Heart Disease", "Anemia", "GERD (Reflux)"].map(d => (
            <button key={d} onClick={() => fetchData(d)} className={`option-btn ${selected === d ? 'active' : ''}`}>{d}</button>
          ))}
        </div>
      </div>

      <div className="card">
        <h3>2. Nutrition: {selected}</h3>
        <div className="nutrition-grid" style={{display: 'flex', gap: '10px'}}>
          {Object.entries(data.nutrients || {}).map(([k, v]) => (
            <div key={k} className="nutrient-tag"><strong>{k}:</strong> {v}</div>
          ))}
        </div>
      </div>

      <div className="data-grid">
        <div className="card">
          <h3>Flavor Molecules</h3>
          <div className="scroll-box">
            {loading ? <p>Loading...</p> : data.molecules?.map((m, i) => (
              <div key={i} className="list-item"><strong>{m.name}</strong><div className="flavor-text">{m.flavor}</div></div>
            ))}
          </div>
        </div>
        <div className="card">
          <h3>Healing Recipes</h3>
          <div className="scroll-box">
            {loading ? <p>Loading...</p> : data.recipes?.map((r, i) => (
              <div key={i} className="recipe-card-inner"><h4>{r.Recipe_title}</h4><small>{r.Region}</small></div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
export default DiseaseApp;