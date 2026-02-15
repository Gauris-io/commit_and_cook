import React, { useState } from "react"; // usestate is like a container which will store the values of variables

function RecipeForm() { // this is an entire fuction which will perform the workflow

  const [age, setAge] = useState(""); // here we have created variables 
  const [texture, setTexture] = useState([]); // this fucntion will update the variable by "set'variable'"
  const [cuisine, setCuisine] = useState(""); // usestate("") --> initially variable = ""
  const [diet, setDiet] = useState(""); // NEW → diet state added
  const [allergies, setAllergies] = useState([]);
  const [result, setResult] = useState(null);


  const allergyOptions = ["Dairy", "Eggs", "Nuts", "Gluten", "Soy", "Fish"];

  // NEW → Diet options from API
  const dietOptions = [
    "no_preference",
    "vegan",
    "pescetarian",
    "ovo_vegetarian",
    "lacto_vegetarian",
    "ovo_lacto_vegetarian"
  ];
  const textureOptions = [
  "Boil","Steam","Blend","Blanch","Bake",
  "Cook","Mash","Puree","Braize","Crockpot","Dice"
  ];
  // UPDATED → Region list exactly from API
  const regionOptions = [
    "Australian",
    "Belgian",
    "Canadian",
    "Caribbean",
    "Central American",
    "Chinese and Mongolian",
    "Deutschland",
    "Eastern European",
    "French",
    "Greek",
    "Indian Subcontinent",
    "Irish",
    "Italian",
    "Japanese",
    "Korean",
    "Mexican",
    "Middle Eastern",
    "Northern Africa",
    "Rest Africa",
    "Scandinavian",
    "South American",
    "Southeast Asian",
    "Spanish and Portuguese",
    "Thai",
    "UK",
    "US"
  ];
   const toggleTexture = (item) => {
    if (texture.includes(item)) {
     setTexture(texture.filter(t => t !== item));
   } else {
    setTexture([...texture, item]);
  }
 };

  const toggleAllergy = (allergy) => {
    if (allergies.includes(allergy)) {
      setAllergies(allergies.filter(a => a !== allergy));
    } else {
      setAllergies([...allergies, allergy]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // stops the page from reloading.
    console.log("BUTTON CLICKED"); // the moment the button clicks handlesubmit activates and console shows - "BUTTON CLICKED"
    try {
      const response = await fetch("http://127.0.0.1:5000/get-recipes", { // "http://127.0.0.1:5000/get-recipes" --> this is flask app.py api which will let react POST the users's input into the database
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          age,
          cuisine,
          texture,
          diet, // NEW → sending diet to backend
          allergies
        })
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();
      setResult(data);   //  this stores backend response
    } catch (error) {
      console.error("Fetch error:", error);
    }
  };

  return (
    <div className="container"> {/* This connects to your CSS: React → assigns class, CSS → styles that class */}
      <form onSubmit={handleSubmit}> {/* When the form is submitted --> React will call the function handleSubmit */}
        

        <div className="card">
          <h3>Baby's Age (months)</h3>
          <input
            type="number"
            placeholder="e.g., 8"
            className="input-field"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
        </div>

        <div className="card">
          <h3>Texture Stage</h3>
          <div className="button-group">
            {textureOptions.map(item => (
              <button
                type="button"
                key={item}
                className={`option-btn ${texture.includes(item) ? "active" : ""}`}
                onClick={() => toggleTexture(item)}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {/* NEW → Diet Section */}
        <div className="card">
          <h3>Diet Preference</h3>
          <div className="button-group">
            {dietOptions.map(item => (
              <button
                type="button"
                key={item}
                className={`option-btn ${diet === item ? "active" : ""}`}
                onClick={() => setDiet(item)}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {/* UPDATED → Region instead of limited cuisine */}
        <div className="card">
          <h3>Preferred Region</h3>
          <div className="button-group">
            {regionOptions.map(item => (
              <button
                type="button"
                key={item}
                className={`option-btn ${cuisine === item ? "active" : ""}`}
                onClick={() => setCuisine(item)}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        <div className="card">
          <h3>Allergies (optional)</h3>
          <div className="button-group">
            {allergyOptions.map(item => (
              <button
                type="button"
                key={item}
                className={`option-btn ${allergies.includes(item) ? "active" : ""}`}
                onClick={() => toggleAllergy(item)}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {/* A form gets submitted when: You click a button with type="submit"  */}
        <button  
          type="submit" 
          className="submit-btn"
          onClick={() => console.log("DIRECT CLICK WORKING")}
       >
       TEST BUTTON
       </button>
       {/* on clicking the find recipie button the console log will give message - "DIRECT CLICK WORKING" */}

      </form>
      {result && (
      <div className="card">
        <h3>Baby Friendly Recipe</h3>

        {result.baby_friendly_recipe?.error ? (
          <pre style={{ whiteSpace: "pre-wrap" }}>
            {result.baby_friendly_recipe.raw_response}
          </pre>
        ) : (
          <div>
            <h4>{result.baby_friendly_recipe?.title}</h4>

            <h5>Ingredients</h5>
            <ul>
              {result.baby_friendly_recipe?.ingredients?.map((item, index) => (
                <li key={index}>
                  {item.ingredient} — {item.quantity}
                </li>
              ))}
            </ul>

            <h5>Instructions</h5>
            <ol>
              {result.baby_friendly_recipe?.instructions?.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ol>

            <p><strong>Nutrition:</strong> {result.baby_friendly_recipe?.nutrition_notes}</p>
            <p><strong>Safety:</strong> {result.baby_friendly_recipe?.safety_notes}</p>
          </div>
        )}
      </div>
    )}

  </div>
);
    
}

export default RecipeForm;
