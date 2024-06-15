import React, { useState } from 'react';
import { Button, Modal, Group, TextInput, PasswordInput } from '@mantine/core';

const SignUpButton = () => {
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Form data:', formData);
    // You can add your form submission logic here, e.g., an API call to a backend service
    handleClose(); // Close the modal after submission
  };

  return (
    <div>
      <Button onClick={handleOpen}>Sign Up</Button>
      <Modal opened={open} onClose={handleClose} title="Sign Up Form">
        <form onSubmit={handleSubmit}>
          <Group direction="column" spacing="md">
            <TextInput
              label="Name"
              placeholder="Name"
              required
              name="name"
              value={formData.name}
              onChange={handleChange}
            />
            <TextInput
              label="Email"
              placeholder="Email"
              required
              name="email"
              value={formData.email}
              onChange={handleChange}
            />
            <PasswordInput
              label="Password"
              placeholder="Password"
              required
              name="password"
              value={formData.password}
              onChange={handleChange}
            />
            <Button type="submit">Sign Up</Button>
          </Group>
        </form>
      </Modal>
    </div>
  );
};

export default SignUpButton;
