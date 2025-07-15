// src/pages/DashboardPage.jsx
import React, { useState, useEffect, useCallback } from 'react';
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
  const [editingTransfer, setEditingTransfer] = useState(null); // Для хранения данных редактируемого трансфера
  const { logout } = useAuth();
  const navigate = useNavigate();

  const fetchTransfers = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/v1/transfers');
      // Маппинг _id -> id для совместимости с фронтом
      const data = response.data.map(t => ({
        ...t,
        id: t._id || t.id,
      }));
      setTransfers(data);
    } catch (err) {
      setError('Failed to fetch transfers.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTransfers();
  }, [fetchTransfers]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleOpenCreateModal = () => {
    setEditingTransfer(null);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (transfer) => {
    setEditingTransfer(transfer);
    setIsModalOpen(true);
  };

  const handleDelete = async (transferId) => {
    if (window.confirm('Are you sure you want to delete this transfer?')) {
      try {
        await apiClient.delete(`/api/v1/transfers/${transferId}`);
        setTransfers(prev => prev.filter(t => t.id !== transferId));
      } catch (err) {
        setError('Failed to delete transfer.');
      }
    }
  };

  const handleFormSubmit = (updatedOrNewTransfer) => {
    // Маппинг _id -> id для совместимости с фронтом
    const transfer = {
      ...updatedOrNewTransfer,
      id: updatedOrNewTransfer._id || updatedOrNewTransfer.id,
    };
    if (editingTransfer) { // Если было редактирование
      setTransfers(prev => prev.map(t => t.id === transfer.id ? transfer : t));
    } else { // Если было создание
      setTransfers(prev => [transfer, ...prev]);
    }
    setIsModalOpen(false);
    setEditingTransfer(null);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Transfers</h1>
        <button onClick={handleLogout}>Logout</button>
      </div>
      
      <div style={{ margin: '1rem 0' }}>
        <button onClick={handleOpenCreateModal} style={{ float: 'right' }}>+ New Transfer</button>
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
              <tr key={transfer.id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '8px' }}>{new Date(transfer.transfer_date).toLocaleString()}</td>
                <td style={{ padding: '8px' }}>{transfer.guest_name}</td>
                <td style={{ padding: '8px' }}>{`${transfer.pickup_location} to ${transfer.destination}`}</td>
                <td style={{ padding: '8px' }}>{transfer.status}</td>
                <td style={{ padding: '8px' }}>
                  <button onClick={() => handleOpenEditModal(transfer)}>Edit</button>
                  <button onClick={() => handleDelete(transfer.id)} style={{ marginLeft: '5px' }}>Delete</button>
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
          onFormSubmit={handleFormSubmit}
          onError={(err) => setError(err)}
          initialData={editingTransfer}
        />
      </Modal>
    </div>
  );
}

export default DashboardPage; 