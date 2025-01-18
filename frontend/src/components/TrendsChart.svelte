<script>
    import Chart from 'chart.js/auto';
    import { onDestroy } from 'svelte';

    let { grievances } = $props();
    let canvas;
    let chart;

    function createChart() {
        if (chart) {
            chart.destroy();
        }

        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const monthlyData = {};
        
        // Process grievances to get date range
        grievances.forEach(g => {
            const date = new Date(g.created_at);
            const key = `${date.getFullYear()}-${date.getMonth()}`;
            monthlyData[key] = (monthlyData[key] || 0) + 1;
        });

        // Sort the keys to get chronological order
        const sortedKeys = Object.keys(monthlyData).sort();
        
        // Take the last 6 months of data (or all if less than 6)
        const recentKeys = sortedKeys.slice(-6);
        
        // Create labels and data arrays
        const labels = recentKeys.map(key => {
            const [year, month] = key.split('-');
            return `${months[parseInt(month)]} ${year}`;
        });
        
        const data = recentKeys.map(key => monthlyData[key]);

        chart = new Chart(canvas, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Grievances',
                    data,
                    borderColor: '#64B5F6',
                    tension: 0.4,
                    fill: true,
                    backgroundColor: 'rgba(100, 181, 246, 0.1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 8,
                        right: 8,
                        top: 8,
                        bottom: 8
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: '#e0e0e0',
                            padding: 5,
                            font: {
                                size: 11
                            }
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#e0e0e0',
                            padding: 5,
                            maxRotation: 45,
                            minRotation: 45,
                            font: {
                                size: 11
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(45, 45, 45, 0.9)',
                        titleFont: {
                            size: 12
                        },
                        bodyFont: {
                            size: 11
                        },
                        padding: 8,
                        callbacks: {
                            title: (context) => context[0].label,
                            label: (context) => `${context.parsed.y} grievance${context.parsed.y !== 1 ? 's' : ''}`
                        }
                    }
                }
            }
        });
    }

    $effect(() => {
        if (grievances && canvas) {
            createChart();
        }
    });

    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });
</script>

<div class="chart-card">
    <h3>Monthly Trends</h3>
    <div class="chart-container">
        <canvas bind:this={canvas}></canvas>
    </div>
</div>

<style>
    .chart-card {
        background: var(--gray-dark, #333333);
        padding: 1.25rem 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        width: 100%;
        aspect-ratio: 16/9;
        max-height: 400px;
        display: flex;
        flex-direction: column;
    }

    .chart-card h3 {
        margin: 0 0 1rem 0;
        text-align: center;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-light, #FFFFFF);
        opacity: 0.8;
        flex-shrink: 0;
    }

    .chart-container {
        position: relative;
        flex: 1;
        min-height: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    canvas {
        max-width: 100%;
        max-height: 100%;
    }

    @media (max-width: 1200px) {
        .chart-card {
            aspect-ratio: 3/2;
        }
    }

    @media (max-width: 768px) {
        .chart-card {
            aspect-ratio: 4/3;
            padding: 1rem 0.75rem;
        }

        .chart-card h3 {
            margin-bottom: 0.75rem;
            font-size: 0.85rem;
        }
    }

    @media (max-width: 480px) {
        .chart-card {
            aspect-ratio: 1/1;
            padding: 0.75rem 0.5rem;
        }

        .chart-card h3 {
            margin-bottom: 0.5rem;
            font-size: 0.8rem;
        }
    }
</style> 