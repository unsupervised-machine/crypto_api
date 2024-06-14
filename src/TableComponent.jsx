import React, { useState, useEffect } from 'react';
import tableData from './MOCK_DATA.json'; // Import the JSON data
import './styles.css'; // Import the CSS file

const TableComponent = () => {
  const [data, setData] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: '', direction: 'ascending' });

  useEffect(() => {
    setData(tableData);
  }, []);

  const sortTable = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }

    const sortedData = [...data].sort((a, b) => {
      if (a[key] < b[key]) {
        return direction === 'ascending' ? -1 : 1;
      }
      if (a[key] > b[key]) {
        return direction === 'ascending' ? 1 : -1;
      }
      return 0;
    });

    setSortConfig({ key, direction });
    setData(sortedData);
  };

  return (
    <div className="container">
      <h2>Cryptocurrency Table</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>
              <button onClick={() => sortTable('id')}>
                ID {sortConfig.key === 'id' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
              </button>
            </th>
            <th>
              <button onClick={() => sortTable('symbol')}>
                Symbol {sortConfig.key === 'symbol' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
              </button>
            </th>
            <th>
              <button onClick={() => sortTable('name')}>
                Name {sortConfig.key === 'name' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
              </button>
            </th>
            <th>Image</th>
            <th>
              <button onClick={() => sortTable('current_price')}>
                Current Price {sortConfig.key === 'current_price' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((crypto, index) => (
            <tr key={crypto._id}>
              <td>{index + 1}</td>
              <td>{crypto.id}</td>
              <td>{crypto.symbol}</td>
              <td>{crypto.name}</td>
              <td><img src={crypto.image} alt={crypto.name} /></td>
              <td>${crypto.current_price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableComponent;
