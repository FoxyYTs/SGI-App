// App.js (Frontend)
import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState([]);

  // Función para obtener datos del backend
  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/data');
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // Llamar a la función al cargar el componente
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div>
      <h1>Datos de la base de datos</h1>
      <ul>
        {data.map((item) => (
          <li key={item.id}>{item.nombre}</li>
        ))}
      </ul>
    </div>
  );
}
