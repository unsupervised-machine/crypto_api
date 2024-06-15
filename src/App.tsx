import "@mantine/core/styles.css";
import {MantineProvider, Table} from "@mantine/core";
import { theme } from "./theme";
import {Table_w_images} from "./components/Table/Table_w_images.tsx";
import SignInButton from "./components/SignIn/SignInButton.jsx"


export default function App() {
  return (
    <MantineProvider theme={theme}>
      <div className="App">
        <h1>Welcome to My App</h1>
        <SignInButton />
        <Table_w_images />
      </div>
    </MantineProvider>
  );
}
