// DataTable.tsx

import React from "react";

const DataTable: React.FC = () => {
  // Example data for the table
  const data = [
    { id: 1, name: "John Doe", age: 28, email: "john.doe@example.com" },
    { id: 2, name: "Jane Smith", age: 32, email: "jane.smith@example.com" },
    { id: 3, name: "Mike Johnson", age: 24, email: "mike.johnson@example.com" },
    { id: 4, name: "Anna White", age: 30, email: "anna.white@example.com" },
  ];

  return (
    <div>
      <h2>Example Table</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Age</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.name}</td>
              <td>{row.age}</td>
              <td>{row.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;