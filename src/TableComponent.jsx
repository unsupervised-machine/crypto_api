// src/TableComponent.jsx
import React, { useState, useEffect } from 'react';
import tableData from './MOCK_DATA.json'; // Import the JSON data

const TableComponent = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Simulating fetching data from JSON file (can also use fetch API or axios)
    setData(tableData);
  }, []);

  return (
    <div>
      <h2>Cryptocurrency Table</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Symbol</th>
            <th>Name</th>
            <th>Image</th>
            <th>Current Price</th>
          </tr>
        </thead>
        <tbody>
          {data.map((crypto) => (
            <tr key={crypto._id}>
              <td>{crypto.id}</td>
              <td>{crypto.symbol}</td>
              <td>{crypto.name}</td>
              <td><img src={crypto.image} alt={crypto.name} style={{ width: '50px', height: 'auto' }} /></td>
              <td>${crypto.current_price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableComponent;
