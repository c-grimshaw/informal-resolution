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

        // Count grievances by unit
        const unitCounts = grievances.reduce((acc, g) => {
            acc[g.unit] = (acc[g.unit] || 0) + 1;
            return acc;
        }, {});

        // Generate colors based on number of units
        const colors = Object.keys(unitCounts).map((_, index) => {
            const hue = (index * 360) / Object.keys(unitCounts).length;
            return `hsla(${hue}, 70%, 50%, 0.8)`;
        });

        chart = new Chart(canvas, {
            type: 'polarArea',
            data: {
                labels: Object.keys(unitCounts),
                datasets: [{
                    data: Object.values(unitCounts),
                    backgroundColor: colors,
                    borderWidth: 1,
                    borderColor: 'rgba(255, 255, 255, 0.1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        ticks: {
                            color: '#e0e0e0',
                            backdropColor: 'transparent'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        angleLines: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#e0e0e0',
                            padding: 10,
                            font: {
                                size: 11
                            },
                            boxWidth: 15,
                            boxHeight: 15
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
    <h3>Grievances by Unit</h3>
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
        aspect-ratio: 4/3;
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
            aspect-ratio: 16/9;
        }
    }

    @media (max-width: 768px) {
        .chart-card {
            aspect-ratio: 3/2;
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