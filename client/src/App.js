import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import axios from 'axios';
import { PublicClientApplication } from "@azure/msal-browser";

// Initialize the MSAL application object
const msalInstance = new PublicClientApplication({
  auth: {
    clientId: "your-app-client-id",
    redirectUri: "your-app-redirect-uri"
  }
});

function App() {
  const [user, setUser] = useState(null);
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    const result = await axios.post('/api/ProcessFiles', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    console.log(result.data);
  };

  return (
    <Router>
      <div>
        {/* Add your login UI here. On successful login, set the user state. */}
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleFileUpload}>Upload</button>
      </div>
    </Router>
  );
}

export default App;
