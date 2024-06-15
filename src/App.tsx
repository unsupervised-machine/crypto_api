import "@mantine/core/styles.css";
import {MantineProvider, Table} from "@mantine/core";
import { theme } from "./theme";
import {Table_w_images} from "./components/Table/Table_w_images.tsx";
import SignInButton from "./components/SignIn/SignInButton.jsx"
import SignUpButton from "./components/SignUp/SignUpButton.jsx"
import { Header } from "./components/Header/Header.tsx"


export default function App() {
  return (
    <MantineProvider theme={theme}>
      <div className="App">
        <Header />
        <h1>Welcome to My App</h1>
        {/*<SignInButton />*/}
        {/*<SignUpButton />*/}
        <Table_w_images />
      </div>
    </MantineProvider>
  );
}
