document.addEventListener('DOMContentLoaded', () => {
    const scanBtn = document.getElementById('scan-btn');
    const emailInput = document.getElementById('email-input');
    const resultsPanel = document.getElementById('results-panel');
    const inputPanel = document.querySelector('.panel-input');
    
    // UI Elements for results
    const predictionBox = document.getElementById('prediction-box');
    const predictionText = document.getElementById('prediction-text');
    const confidenceValue = document.getElementById('confidence-value');
    const confidenceFill = document.getElementById('confidence-fill');
    const indicatorsList = document.getElementById('indicators-list');
    const recommendationText = document.getElementById('recommendation-text');

    // Initialize Chart
    initChart();

    scanBtn.addEventListener('click', async () => {
        const text = emailInput.value.trim();
        if (!text) {
            alert('Please paste some email content to scan.');
            return;
        }

        // Start scanning animation
        inputPanel.classList.add('scanning');
        scanBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
        scanBtn.disabled = true;

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();
            
            // Simulate processing time for UX
            setTimeout(() => {
                displayResults(data);
                inputPanel.classList.remove('scanning');
                scanBtn.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i> Analyze Content';
                scanBtn.disabled = false;
            }, 1000);

        } catch (error) {
            console.error('Error during analysis:', error);
            alert('An error occurred during analysis.');
            inputPanel.classList.remove('scanning');
            scanBtn.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i> Analyze Content';
            scanBtn.disabled = false;
        }
    });

    function displayResults(data) {
        resultsPanel.style.display = 'block';
        
        // Prediction and styling
        predictionText.textContent = data.prediction;
        predictionBox.className = 'prediction-box'; // reset classes
        
        if (data.prediction === 'PHISHING') {
            predictionBox.classList.add('is-phishing');
        } else {
            predictionBox.classList.add('is-safe');
        }

        // Confidence meter
        confidenceValue.textContent = data.confidence;
        // Small timeout for animation
        confidenceFill.style.width = '0%';
        setTimeout(() => {
            confidenceFill.style.width = `${data.confidence}%`;
        }, 100);

        // Threat Indicators
        indicatorsList.innerHTML = '';
        if (data.indicators && data.indicators.length > 0) {
            data.indicators.forEach(indicator => {
                const li = document.createElement('li');
                li.innerHTML = `<i class="fa-solid fa-bug"></i> ${indicator}`;
                indicatorsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.className = 'safe-indicator';
            li.innerHTML = `<i class="fa-solid fa-shield-halved"></i> No suspicious indicators found in text.`;
            indicatorsList.appendChild(li);
        }

        // Recommendation
        recommendationText.textContent = data.recommendation;
    }

    function initChart() {
        // Confusion matrix data comes from window.modelMetrics
        const cm = window.modelMetrics.confusion_matrix;
        if (!cm) return;

        const ctx = document.getElementById('confusionMatrixChart').getContext('2d');
        
        // To visualize confusion matrix, we'll use a bar chart showing True Neg, False Pos, False Neg, True Pos
        const chartData = {
            labels: ['True Safe', 'False Phishing', 'False Safe', 'True Phishing'],
            datasets: [{
                label: 'Sample Count',
                data: [cm[0][0], cm[0][1], cm[1][0], cm[1][1]],
                backgroundColor: [
                    'rgba(0, 255, 102, 0.6)', // True Safe
                    'rgba(255, 0, 85, 0.6)',  // False Phishing (FP)
                    'rgba(255, 165, 0, 0.6)', // False Safe (FN)
                    'rgba(0, 240, 255, 0.6)'  // True Phishing
                ],
                borderColor: [
                    '#00ff66',
                    '#ff0055',
                    '#ffa500',
                    '#00f0ff'
                ],
                borderWidth: 1
            }]
        };

        new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Confusion Matrix Distribution',
                        color: '#94a3b8'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    }
                }
            }
        });
    }
});
