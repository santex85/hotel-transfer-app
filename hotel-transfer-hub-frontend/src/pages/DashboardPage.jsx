// src/pages/DashboardPage.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/api';
import Modal from '../components/Modal';
import TransferForm from '../components/TransferForm';

function DashboardPage() {
  const [transfers, setTransfers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const fetchTransfers = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/v1/transfers');
      console.log('Fetched transfers:', response.data);
      setTransfers(response.data);
    } catch (err) {
      setError('Failed to fetch transfers.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransfers();
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleTransferCreated = (newTransfer) => {
    console.log('New transfer created:', newTransfer);
    console.log('Current transfers before update:', transfers);
    setTransfers(prevTransfers => {
      const updatedTransfers = [newTransfer, ...prevTransfers];
      console.log('Updated transfers:', updatedTransfers);
      return updatedTransfers;
    });
    setIsModalOpen(false);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  console.log('Rendering dashboard with transfers:', transfers);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Transfers</h1>
        <button onClick={handleLogout}>Logout</button>
      </div>

      <div style={{ margin: '1rem 0' }}>
        <button>Today</button>
        <button>Tomorrow</button>
        <button>This week</button>
        <input type="search" placeholder="Search guest name or room number" style={{ marginLeft: '1rem' }} />
        <button onClick={() => setIsModalOpen(true)} style={{ float: 'right' }}>+ New Transfer</button>
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #ccc' }}>
            <th style={{ textAlign: 'left', padding: '8px' }}>Time</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Guest</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Route</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Status</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {transfers.length > 0 ? (
            transfers.map((transfer) => (
              <tr key={transfer._id || transfer.id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '8px' }}>{new Date(transfer.transfer_date).toLocaleTimeString()}</td>
                <td style={{ padding: '8px' }}>{transfer.guest_name}</td>
                <td style={{ padding: '8px' }}>{`${transfer.pickup_location} to ${transfer.destination}`}</td>
                <td style={{ padding: '8px' }}>{transfer.status}</td>
                <td style={{ padding: '8px' }}>
                  <button>Edit</button>
                  <button>Cancel</button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" style={{ textAlign: 'center', padding: '16px' }}>No transfers found.</td>
            </tr>
          )}
        </tbody>
      </table>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <TransferForm
          onTransferCreated={handleTransferCreated}
          onError={(err) => setError(err)}
        />
      </Modal>
    </div>
  );
}

export default DashboardPage; 