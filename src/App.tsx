import "@mantine/core/styles.css";
import {MantineProvider, Table} from "@mantine/core";
import { theme } from "./theme";
// import DataTable from "./DataTable.tsx";
// import {TableSort} from "./TableSort.tsx";
import {Table_w_images} from "./Table_w_images.tsx";

export default function App() {
  return (
    <MantineProvider theme={theme}>
      <div className="App">
        <h1>Welcome to My App</h1>
        {/*<DataTable /> /!* Render the DataTable component here *!/*/}
        {/*<TableSort />*/}
        <Table_w_images />
      </div>
    </MantineProvider>
  );
}
