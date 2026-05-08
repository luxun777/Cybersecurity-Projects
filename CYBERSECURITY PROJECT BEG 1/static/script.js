document.addEventListener('DOMContentLoaded', () => {
    const scanBtn = document.getElementById('scanBtn');
    const targetInput = document.getElementById('targetInput');
    const scanStatus = document.getElementById('scanStatus');
    const resultsDashboard = document.getElementById('resultsDashboard');
    const downloadReportBtn = document.getElementById('downloadReportBtn');
    
    let currentChart = null;
    let currentReportFile = null;

    // Tab Switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.style.display = 'none');
            
            // Add active class to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target') + '-tab';
            document.getElementById(targetId).style.display = 'block';
        });
    });

    // Scan Button Click
    scanBtn.addEventListener('click', async () => {
        const target = targetInput.value.trim();
        if (!target) {
            alert('Please enter a target IP or domain.');
            return;
        }

        // UI Updates for Scanning State
        scanBtn.disabled = true;
        scanBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Scanning...';
        scanStatus.style.display = 'flex';
        resultsDashboard.style.display = 'none';

        try {
            const response = await fetch('/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ target: target })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Scan failed.');
            }

            // Populate Dashboard
            populateDashboard(data);
            
            // Show Dashboard
            scanStatus.style.display = 'none';
            resultsDashboard.style.display = 'grid';
            
            if (data.report_file) {
                currentReportFile = data.report_file;
                downloadReportBtn.style.display = 'inline-flex';
            }

        } catch (error) {
            alert(`Error: ${error.message}`);
            scanStatus.style.display = 'none';
        } finally {
            scanBtn.disabled = false;
            scanBtn.innerHTML = '<i class="fa-solid fa-play"></i> Initiate Scan';
        }
    });

    downloadReportBtn.addEventListener('click', () => {
        if (currentReportFile) {
            const filename = currentReportFile.split('/').pop();
            window.location.href = `/report/${filename}`;
        }
    });

    function populateDashboard(data) {
        // Update Score
        const score = data.score || 0;
        document.getElementById('scoreValue').textContent = score;
        
        // Animate Circle
        const circle = document.getElementById('scoreCircle');
        const circumference = 2 * Math.PI * 45; // r=45
        const offset = circumference - (score / 100) * circumference;
        circle.style.strokeDashoffset = offset;

        // Score Color & Label
        const scoreLabel = document.getElementById('scoreLabel');
        if (score >= 90) {
            circle.style.stroke = 'var(--success)';
            scoreLabel.textContent = 'Excellent';
            scoreLabel.style.color = 'var(--success)';
        } else if (score >= 70) {
            circle.style.stroke = 'var(--warning)';
            scoreLabel.textContent = 'Fair';
            scoreLabel.style.color = 'var(--warning)';
        } else {
            circle.style.stroke = 'var(--danger)';
            scoreLabel.textContent = 'Critical';
            scoreLabel.style.color = 'var(--danger)';
        }

        // Update Stats
        document.getElementById('openPortsCount').textContent = data.open_ports.length;
        document.getElementById('missingHeadersCount').textContent = data.missing_headers.length;
        document.getElementById('totalRisksCount').textContent = data.vulnerabilities.length;

        // Populate Ports Table
        const portsTableBody = document.getElementById('portsTableBody');
        portsTableBody.innerHTML = '';
        if (data.open_ports.length === 0) {
            portsTableBody.innerHTML = '<tr><td colspan="3">No open ports detected.</td></tr>';
        } else {
            data.open_ports.forEach(port => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><span class="badge low">${port.port}</span></td>
                    <td>${port.service}</td>
                    <td style="font-family: monospace; font-size: 0.8rem; color: var(--text-muted);">${port.banner}</td>
                `;
                portsTableBody.appendChild(tr);
            });
        }

        // Populate Vulnerabilities
        const vulnList = document.getElementById('vulnList');
        vulnList.innerHTML = '';
        
        let highCount = 0, mediumCount = 0, lowCount = 0;

        if (data.vulnerabilities.length === 0) {
            vulnList.innerHTML = '<p>No vulnerabilities detected.</p>';
        } else {
            data.vulnerabilities.forEach(vuln => {
                // Count for chart
                if (vuln.severity === 'High') highCount++;
                else if (vuln.severity === 'Medium') mediumCount++;
                else if (vuln.severity === 'Low') lowCount++;

                const item = document.createElement('div');
                item.className = 'vuln-item';
                item.innerHTML = `
                    <div class="vuln-info">
                        <h4>${vuln.title}</h4>
                        <p>${vuln.description}</p>
                    </div>
                    <span class="badge ${vuln.severity.toLowerCase()}">${vuln.severity}</span>
                `;
                vulnList.appendChild(item);
            });
        }

        // Populate Headers
        const headersList = document.getElementById('headersList');
        headersList.innerHTML = '';
        if (data.missing_headers.length === 0) {
            headersList.innerHTML = '<li>All standard security headers are present.</li>';
        } else {
            data.missing_headers.forEach(header => {
                const li = document.createElement('li');
                li.style.marginBottom = '0.5rem';
                li.innerHTML = `<i class="fa-solid fa-triangle-exclamation" style="color: var(--warning); margin-right: 0.5rem;"></i> Missing: ${header}`;
                headersList.appendChild(li);
            });
        }

        // Render Chart
        renderChart(highCount, mediumCount, lowCount);
    }

    function renderChart(high, medium, low) {
        const ctx = document.getElementById('severityChart').getContext('2d');
        
        if (currentChart) {
            currentChart.destroy();
        }

        currentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['High', 'Medium', 'Low'],
                datasets: [{
                    data: [high, medium, low],
                    backgroundColor: [
                        '#ef4444', // danger
                        '#f59e0b', // warning
                        '#3b82f6'  // blue/low
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#94a3b8'
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }
});
