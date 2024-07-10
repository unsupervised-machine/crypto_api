import React, { useState } from 'react';
import {
  HoverCard,
  Group,
  Button,
  UnstyledButton,
  Text,
  SimpleGrid,
  ThemeIcon,
  Anchor,
  Divider,
  Center,
  Box,
  Burger,
  Drawer,
  Collapse,
  ScrollArea,
  rem,
  useMantineTheme,
  Modal,
  TextInput,
  PasswordInput,
  Paper,
} from '@mantine/core';
import { MantineLogo } from '@mantinex/mantine-logo';
import { useDisclosure } from '@mantine/hooks';
import {
  IconNotification,
  IconCode,
  IconBook,
  IconChartPie3,
  IconFingerprint,
  IconCoin,
  IconChevronDown,
} from '@tabler/icons-react';
import axios from 'axios';
import classes from './Header.module.css';

const mockdata = [
  {
    icon: IconCode,
    title: 'Open source',
    description: 'This Pokémon’s cry is very loud and distracting',
  },
  {
    icon: IconCoin,
    title: 'Free for everyone',
    description: 'The fluid of Smeargle’s tail secretions changes',
  },
  {
    icon: IconBook,
    title: 'Documentation',
    description: 'Yanma is capable of seeing 360 degrees without',
  },
  {
    icon: IconFingerprint,
    title: 'Security',
    description: 'The shell’s rounded shape and the grooves on its.',
  },
  {
    icon: IconChartPie3,
    title: 'Analytics',
    description: 'This Pokémon uses its flying ability to quickly chase',
  },
  {
    icon: IconNotification,
    title: 'Notifications',
    description: 'Combusken battles with the intensely hot flames it spews',
  },
];

export function Header() {
  const [drawerOpened, { toggle: toggleDrawer, close: closeDrawer }] = useDisclosure(false);
  const [linksOpened, { toggle: toggleLinks }] = useDisclosure(false);
  const [loginOpened, { open: openLogin, close: closeLogin }] = useDisclosure(false);
  const [signupOpened, { open: openSignup, close: closeSignup }] = useDisclosure(false);
  const theme = useMantineTheme();

  // State for form inputs
  const [signupEmail, setSignupEmail] = useState('');
  const [signupPassword, setSignupPassword] = useState('');
  const [signupConfirmPassword, setSignupConfirmPassword] = useState('');

  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  // Authentication state
  const [authenticated, setAuthenticated] = useState(false); // Initially false, assuming not authenticated

  // Handle sign-up form submission
  const handleSignupSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:3000/api/signup', {
        signupEmail,
        signupPassword,
        signupConfirmPassword,
      }, {
        withCredentials: true
      });

      // Assuming successful signup sets authenticated state
      setAuthenticated(true);
    } catch (error) {
      console.error('Error signing up:', error);
      // Handle error UI changes or display error message
    }

    // Close the sign-up modal or perform other actions after sign-up
    closeSignup();
  };

  // Handle log-in form submission
  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:3000/api/signin', {
        email: loginEmail,
        password: loginPassword
      });

      // Assuming successful login sets authenticated state
      setAuthenticated(true);
    } catch (error) {
      console.error('Error logging in:', error);
      // Handle error UI changes or display error message to the user
    }

    // Close the login modal or perform other actions after login attempt
    closeLogin();
  };

  const handleLogout = async () => {
    try {
      // Call your backend API to clear session (optional, if needed)
      const response = await fetch('/api/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        console.log('Logged out successfully');
      } else {
        console.error('Logout failed');
      }

      // Perform client-side logout actions
      setAuthenticated(false); // Example state update for authentication status
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const links = mockdata.map((item) => (
    <UnstyledButton className={classes.subLink} key={item.title}>
      <Group wrap="nowrap" align="flex-start">
        <ThemeIcon size={34} variant="default" radius="md">
          <item.icon style={{ width: rem(22), height: rem(22) }} color={theme.colors.blue[6]} />
        </ThemeIcon>
        <div>
          <Text size="sm" fw={500}>
            {item.title}
          </Text>
          <Text size="xs" c="dimmed">
            {item.description}
          </Text>
        </div>
      </Group>
    </UnstyledButton>
  ));

  const loginForm = (
    <Paper p="md" component="form" onSubmit={handleLoginSubmit}>
      <TextInput
          label="Email"
          placeholder="you@example.com"
          required
          value={loginEmail}
          onChange={(event) => setLoginEmail(event.currentTarget.value)}
      />
      <PasswordInput
          label="Password"
          placeholder="Your password"
          required
          mt="md"
          value={loginPassword}
          onChange={(event) => setLoginPassword(event.currentTarget.value)}
      />
      <Group justify="flex-end" mt="md">
        <Button onClick={closeLogin}>Cancel</Button>
        <Button type="submit">Log in</Button>
      </Group>
    </Paper>
  );

  const signupForm = (
    <Paper p="md" component="form" onSubmit={handleSignupSubmit}>
      <TextInput
        label="Email"
        placeholder="you@example.com"
        required
        value={signupEmail}
        onChange={(event) => setSignupEmail(event.currentTarget.value)}
      />
      <PasswordInput
        label="Password"
        placeholder="Your password"
        required
        mt="md"
        value={signupPassword}
        onChange={(event) => setSignupPassword(event.currentTarget.value)}
      />
      <PasswordInput
        label="Confirm Password"
        placeholder="Confirm your password"
        required
        mt="md"
        value={signupConfirmPassword}
        onChange={(event) => setSignupConfirmPassword(event.currentTarget.value)}
      />
      <Group justify="flex-end" mt="md">
        <Button onClick={closeSignup}>Cancel</Button>
        <Button type="submit">Sign up</Button>
      </Group>
    </Paper>
  );

  return (
    <Box pb={120}>
      <header className={classes.header}>
        <Group justify="space-between" h="100%">
          <MantineLogo size={30} />

          <Group h="100%" gap={0} visibleFrom="sm">
            <a href="#" className={classes.link}>
              Home
            </a>
            <HoverCard width={600} position="bottom" radius="md" shadow="md" withinPortal>
              <HoverCard.Target>
                <a href="#" className={classes.link}>
                  <Center inline>
                    <Box component="span" mr={5}>
                      Features
                    </Box>
                    <IconChevronDown
                      style={{ width: rem(16), height: rem(16) }}
                      color={theme.colors.blue[6]}
                    />
                  </Center>
                </a>
              </HoverCard.Target>

              <HoverCard.Dropdown style={{ overflow: 'hidden' }}>
                <Group justify="space-between" px="md">
                  <Text fw={500}>Features</Text>
                  <Anchor href="#" fz="xs">
                    View all
                  </Anchor>
                </Group>

                <Divider my="sm" />

                <SimpleGrid cols={2} spacing={0}>
                  {links}
                </SimpleGrid>

                <div className={classes.dropdownFooter}>
                  <Group justify="space-between">
                    <div>
                      <Text fw={500} fz="sm">
                        Get started
                      </Text>
                      <Text size="xs" c="dimmed">
                        Their food sources have decreased, and their numbers
                      </Text>
                    </div>
                    <Button variant="default">Get started</Button>
                  </Group>
                </div>
              </HoverCard.Dropdown>
            </HoverCard>
            <a href="#" className={classes.link}>
              Learn
            </a>
            <a href="#" className={classes.link}>
              Academy
            </a>
          </Group>

          <Group visibleFrom="sm">
            {authenticated ? (
              <Button onClick={handleLogout}>Logout</Button>
            ) : (
              <>
                <Button variant="default" onClick={openLogin}>Log in</Button>
                <Button onClick={openSignup}>Sign up</Button>
              </>
            )}
          </Group>

          <Burger opened={drawerOpened} onClick={toggleDrawer} hiddenFrom="sm" />
        </Group>
      </header>

      <Drawer
        opened={drawerOpened}
        onClose={closeDrawer}
        size="100%"
        padding="md"
        title="Navigation"
        hiddenFrom="sm"
        zIndex={1000000}
      >
        <ScrollArea h={`calc(100vh - ${rem(80)})`} mx="-md">
          <Divider my="sm" />

          <a href="#" className={classes.link}>
            Home
          </a>
          <UnstyledButton className={classes.link} onClick={toggleLinks}>
            <Center inline>
              <Box component="span" mr={5}>
                Features
              </Box>
              <IconChevronDown
                style={{ width: rem(16), height: rem(16) }}
                color={theme.colors.blue[6]}
              />
            </Center>
          </UnstyledButton>
          <Collapse in={linksOpened}>{links}</Collapse>
          <a href="#" className={classes.link}>
            Learn
          </a>
          <a href="#" className={classes.link}>
            Academy
          </a>

          <Divider my="sm" />

          <Group justify="center" grow pb="xl" px="md">
            {authenticated ? (
              <Button onClick={handleLogout}>Logout</Button>
            ) : (
              <>
                <Button variant="default" onClick={openLogin}>Log in</Button>
                <Button onClick={openSignup}>Sign up</Button>
              </>
            )}
          </Group>
        </ScrollArea>
      </Drawer>

      <Modal opened={loginOpened} onClose={closeLogin} title="Log in">
        {loginForm}
      </Modal>

      <Modal opened={signupOpened} onClose={closeSignup} title="Sign up">
        {signupForm}
      </Modal>
    </Box>
  );
}
