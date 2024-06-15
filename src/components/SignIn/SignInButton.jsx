// SignInButton.jsx

import React, { useState } from 'react';
import { Button, Modal } from '@mantine/core';
import SignInForm from './SignInForm';

const SignInButton = () => {
  const [isOpen, setIsOpen] = useState(false);

  const openSignInForm = () => {
    setIsOpen(true);
  };

  const closeSignInForm = () => {
    setIsOpen(false);
  };

  return (
    <>
      <Button onClick={openSignInForm}>Sign In</Button>
      <Modal title="Sign In" opened={isOpen} onClose={closeSignInForm}>
        <SignInForm onClose={closeSignInForm} />
      </Modal>
    </>
  );
};

export default SignInButton;
