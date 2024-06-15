import "@mantine/core/styles.css";
import {MantineProvider, Table} from "@mantine/core";
import { theme } from "./theme";
import { HomePageTable } from "./components/Table/HomePageTable.tsx";
import { Header } from "./components/Header/Header.tsx"


export default function App() {
  return (
    <MantineProvider theme={theme}>
      <div className="App">
        <Header />
        {/*<h1>Welcome to My App</h1>*/}
        {/*<SignInButton />*/}
        {/*<SignUpButton />*/}
        <HomePageTable />
      </div>
    </MantineProvider>
  );
}
