import React, { useState } from 'react';
import { Button, Modal, Group, TextInput, PasswordInput } from '@mantine/core';

const SignInButton = () => {
  const [open, setOpen] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    // Add your form submission logic here
  };

  return (
    <div>
      <Button onClick={handleOpen}>Sign In</Button>
      <Modal opened={open} onClose={handleClose} title="Sign In Form">
        <form onSubmit={handleSubmit}>
          <Group direction="column" spacing="md">
            <TextInput label="Email" placeholder="Email" required />
            <PasswordInput label="Password" placeholder="Password" required />
            <Button type="submit">Sign In</Button>
          </Group>
        </form>
      </Modal>
    </div>
  );
};

export default SignInButton;
