$(document).ready(function() {
    // Load History 
    loadScanHistory();

    $('#uploadForm').submit(function(e) {
        e.preventDefault();
        let formData = new FormData(this);
        
        $.ajax({
            url: '/scanner/upload/', 
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    $('#result').html('<p class="loading">Scanning file... Please wait</p>');
                    checkScanResult(response.scan_id);
                    // Reload history after uploading a file
                    loadScanHistory();
                } else {
                    $('#result').html('<p>Error: ' + response.message + '</p>');
                }
            },
            error: function(xhr, status, error) {
                $('#result').html('<p>Error uploading file: ' + status + ' - ' + error + '</p>');
            }
        });
    });

    // History function 
    function loadScanHistory() {
        $.ajax({
            url: '/scanner/history/',
            type: 'GET',
            success: function(response) {
                if (response.success) {
                    let historyHtml = '';
                    response.history.forEach(function(scan) {
                        historyHtml += `
                            <div class="history-item">
                                <p><strong>${scan.file_name}</strong></p>
                                <p>Status: ${scan.status}</p>
                                <p>Date: ${scan.created_at}</p>
                                <a href="#" class="view-result" data-scan-id="${scan.scan_id}">View Result</a>
                            </div>
                        `;
                    });
                    $('#history-list').html(historyHtml || '<p>No scans yet.</p>');
                } else {
                    $('#history-list').html('<p>Error loading history.</p>');
                }
            },
            error: function() {
                $('#history-list').html('<p>Error loading history.</p>');
            }
        });
    }

    //  clics in  "View Result"
    $('#history-list').on('click', '.view-result', function(e) {
        e.preventDefault();
        let scanId = $(this).data('scan-id');
        checkScanResult(scanId);
    });

    function checkScanResult(scanId) {
        $.ajax({
            url: '/scanner/result/' + scanId + '/',  
            type: 'GET',
            timeout: 30000,
            success: function(response) {
                if (response.success && response.completed) {
                    let resultText = `Scan completed. Detected: ${response.positives}/${response.total}`;
                    
                    let scanResultsHtml = '<h3>Scan Results</h3><table><tr><th>Engine</th><th>Result</th></tr>';
                    let undetectedCount = 0;
                    for (let engine in response.scan_results) {
                        let category = response.scan_results[engine].category;
                        let displayResult = category !== undefined ? category : 'Unknown';
                        let resultClass;
                        switch (displayResult) {
                            case 'undetected':
                                resultClass = 'result-safe';
                                undetectedCount++;
                                break;
                            case 'type-unsupported':
                                resultClass = 'result-unsupported';
                                break;
                            case 'malicious':
                            case 'suspicious':
                                resultClass = 'result-danger';
                                break;
                            case 'timeout':
                                resultClass = 'result-timeout';
                                break;
                            default:
                                resultClass = 'result-unknown';
                        }
                        scanResultsHtml += `<tr><td>${engine}</td><td class="${resultClass}">${displayResult}</td></tr>`;
                    }
                    scanResultsHtml += '</table>';

                    let props = response.file_properties;
                    let filePropsHtml = `
                        <div class="file-properties">
                            <h3>File Properties</h3>
                            <p><strong>MD5</strong>: ${props.md5}</p>
                            <p><strong>SHA-1</strong>: ${props.sha1}</p>
                            <p><strong>SHA-256</strong>: ${props.sha256}</p>
                            <p><strong>File Size</strong>: ${props.size_kb.toFixed(2)} KB</p>
                            <p><strong>File Type</strong>: ${props.file_type}</p>
                        </div>
                    `;

                    let resultWithPie = `
                        <div class="scan-result">
                            <canvas id="detectionPieChart" width="100" height="100"></canvas>
                            <p>${resultText}</p>
                        </div>
                    `;

                    $('#result').html(`
                        <div class="result-container">
                            ${filePropsHtml}
                            ${resultWithPie}
                        </div>
                        ${scanResultsHtml}
                        <p><a href="${response.permalink}" target="_blank">View full report</a></p>
                    `);

                    // Draw the chart
                    let ctx = document.getElementById('detectionPieChart').getContext('2d');
                    let ringColor = response.positives > 0 ? '#dc3545' : '#28a745';
                    console.log('Ring color:', ringColor, 'Positives:', response.positives);

                    new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: ['Detected', 'Not Detected'],
                            datasets: [{
                                data: [response.positives, response.total - response.positives],
                                backgroundColor: [ringColor, '#00FF5E'],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { display: false }
                            },
                            cutout: '50%'
                        }
                    });
                } else if (!response.success && response.message.includes('still in progress')) {
                    $('#result').html('<p class="loading">Scan in progress... Please wait a moment and refresh.</p>');
                } else {
                    $('#result').html('<p>Error: ' + response.message + '</p>');
                }
            },
            error: function(xhr, status, error) {
                $('#result').html('<p>Error checking scan results: ' + status + ' - ' + error + '</p>');
            }
        });
    }
});