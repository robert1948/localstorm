import React, { useEffect, useState } from 'react';
import { fetchAnalyticsData } from '../services/api.service';

const Analytics = () => {
    const [analyticsData, setAnalyticsData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getAnalyticsData = async () => {
            try {
                const data = await fetchAnalyticsData();
                setAnalyticsData(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        getAnalyticsData();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h1>Analytics Dashboard</h1>
            <ul>
                {analyticsData.map((item, index) => (
                    <li key={index}>{item.metric}: {item.value}</li>
                ))}
            </ul>
        </div>
    );
};

export default Analytics;