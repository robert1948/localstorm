import React from 'react';
import { useEffect, useState } from 'react';
import { fetchDashboardData } from '../services/api.service';
import DashboardCard from '../components/dashboard/DashboardCard';
import './Dashboard.css';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                const result = await fetchDashboardData();
                setData(result);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error loading data: {error.message}</div>;
    }

    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            {data && data.map((item) => (
                <DashboardCard key={item.id} data={item} />
            ))}
        </div>
    );
};

export default Dashboard;