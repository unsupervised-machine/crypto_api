// SignInForm.jsx

import React from 'react';
import { Button, TextInput } from '@mantine/core';

const SignInForm = ({ onClose }) => {
  const handleSignIn = (e) => {
    e.preventDefault();
    // Implement sign-in logic here
  };

  return (
    <form onSubmit={handleSignIn}>
      <TextInput label="Email" type="email" required />
      <TextInput label="Password" type="password" required />
      <Button type="submit">Sign In</Button>
      <Button variant="link" onClick={onClose}>
        Cancel
      </Button>
    </form>
  );
};

export default SignInForm;