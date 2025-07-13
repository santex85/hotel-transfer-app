// src/components/TransferForm.jsx
import React, { useState } from 'react';
import apiClient from '../services/api';

const TransferForm = ({ onTransferCreated, onError }) => {
  const [formData, setFormData] = useState({
    guest_name: '',
    room_number: '',
    phone_number: '',
    transfer_date: '',
    passengers: 1,
    pickup_location: 'Hotel',
    destination: '',
    comments: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitting form data:', formData);
    
    try {
      const requestData = {
        ...formData,
        // Убедимся, что дата в правильном формате ISO
        transfer_date: new Date(formData.transfer_date).toISOString(),
        passengers: parseInt(formData.passengers, 10)
      };
      
      console.log('Sending request with data:', requestData);
      
      const response = await apiClient.post('/api/v1/transfers', requestData);
      console.log('Transfer created successfully:', response.data);
      
      onTransferCreated(response.data); // Передаем созданный трансфер наверх
    } catch (err) {
      console.error("Failed to create transfer", err);
      onError("Не удалось создать трансфер. Проверьте данные.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>New Transfer</h2>
      <input name="guest_name" value={formData.guest_name} onChange={handleChange} placeholder="Guest Name" required />
      <input name="room_number" value={formData.room_number} onChange={handleChange} placeholder="Room Number" required />
      <input name="phone_number" value={formData.phone_number} onChange={handleChange} placeholder="Phone Number" required />
      <input name="transfer_date" type="datetime-local" value={formData.transfer_date} onChange={handleChange} required />
      <input name="passengers" type="number" value={formData.passengers} onChange={handleChange} placeholder="Passengers" min="1" required />
      <input name="pickup_location" value={formData.pickup_location} onChange={handleChange} placeholder="Pickup Location" required />
      <input name="destination" value={formData.destination} onChange={handleChange} placeholder="Destination" required />
      <textarea name="comments" value={formData.comments} onChange={handleChange} placeholder="Comments" />
      <button type="submit">Create Transfer</button>
    </form>
  );
};

export default TransferForm; 