// static/scan_ip_domain/js/scan_ip_domain.js
$(document).ready(function() {
    console.log('scan_ip_domain.js loaded');

// Function to render the results (reusable for new scans and details)
function renderResults(response, $results) {
        if (response.error) {
            $results.html(`<p class="result-danger">${response.error}</p>`);
            $results.addClass('visible');
            return;
        }

        if (!response.details || typeof response.details.abuse_score === 'undefined') {
            $results.html('<p class="result-danger">Invalid response data</p>');
            $results.addClass('visible');
            return;
        }

        const details = `
            <div class="result-container">
                <div class="result-details">
                    <p><strong>Target:</strong> ${response.target || 'N/A'}</p>
                    <p><strong>Status:</strong> ${response.is_suspicious ? 'Suspicious' : 'Clean'}</p>
                    <p><strong>Resolved IP:</strong> ${response.details.resolved_ip || 'N/A'}</p>
                    <p><strong>Public IP:</strong> ${response.details.is_public || 'N/A'}</p>
                    <p><strong>IP Version:</strong> ${response.details.ip_version || 'N/A'}</p>
                    <p><strong>Whitelisted:</strong> ${response.details.is_whitelisted || 'N/A'}</p>
                    <p><strong>Abuse Confidence Score:</strong> ${response.details.abuse_score}%</p>
                    <p><strong>Country:</strong> ${response.details.country || 'N/A'}</p>
                    <p><strong>Usage Type:</strong> ${response.details.usage_type || 'N/A'}</p>
                    <p><strong>ISP:</strong> ${response.details.isp || 'N/A'}</p>
                    <p><strong>Domain:</strong> ${response.details.domain || 'N/A'}</p>
                    <p><strong>Hostnames:</strong> ${response.details.hostnames || 'N/A'}</p>
                    <p><strong>Total Reports:</strong> ${response.details.total_reports || '0'}</p>
                    <p><strong>Distinct Users:</strong> ${response.details.distinct_users || '0'}</p>
                    <p><strong>Last Reported:</strong> ${response.details.last_reported || 'Never'}</p>
                </div>
                <div class="chart-container">
                    <canvas id="scoreChart"></canvas>
                </div>
            </div>
        `;
        $results.html(details);
        $results.addClass('visible');

        try {
            const ctx = document.getElementById('scoreChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Abuse Score', 'Safe'],
                    datasets: [{
                        data: [response.details.abuse_score, 100 - response.details.abuse_score],
                        backgroundColor: ['#ff2e63', '#00b3b3']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        } catch (error) {
            console.error('Error creating chart:', error);
        }
    }

    // Funtion to load the scan history 
    function loadHistory() {
        const $historyList = $('#history-list');
        const historyUrl = $historyList.data('url');
        console.log('History URL:', historyUrl);

        $historyList.html('<p>Loading history...</p>');

        $.ajax({
            url: historyUrl,
            type: 'GET',
            success: function(response) {
                console.log('History response:', response);
                if (response.history && response.history.length > 0) {
                    const historyItems = response.history.map(item => `
                        <div class="history-item">
                            <p><strong>${item.target}</strong></p> <!-- Target en su propio párrafo -->
                            <p>
                                <span class="${item.is_suspicious ? 'text-danger' : 'text-success'}">
                                    ${item.is_suspicious ? 'Suspicious' : 'Clean'}
                                </span>
                            </p> <!-- Estado en su propio párrafo -->
                            <small>${new Date(item.scan_date).toLocaleString()}</small>
                            <a href="#" class="view-result" data-scan-id="${item.id}">View Result</a>
                        </div>
                    `).join('');
                    $historyList.html(historyItems);

                //Event for Scan result 
                    $('.view-result').on('click', function(e) {
                        e.preventDefault();
                        const scanId = $(this).data('scan-id');
                        const $results = $('#scan-results');
                        $results.html('<p class="loading">Loading scan results...</p>');
                        $results.addClass('visible');

                        $.ajax({
                            url: `/scan-ip-domain/detail/${scanId}/`,
                            type: 'GET',
                            success: function(response) {
                                renderResults(response, $results);
                            },
                            error: function(xhr, status, error) {
                                console.error('Error loading scan details:', status, error);
                                $results.html('<p class="result-danger">Error loading scan details.</p>');
                                $results.addClass('visible');
                            }
                        });
                    });
                } else {
                    $historyList.html('<p>No scan history available.</p>');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error loading history:', status, error);
                $historyList.html('<p>Error loading history.</p>');
            }
        });
    }

    // Load the history when website is open
    loadHistory();

    $('#scan-form').on('submit', function(e) {
        e.preventDefault();
        console.log('Form submitted');

        const formData = new FormData(this);
        const $results = $('#scan-results');
        const url = $(this).data('url');
        console.log('URL:', url);

        $results.html('<p class="loading">Scanning...</p>');
        $results.addClass('visible');

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log('Response:', response);
                renderResults(response, $results);
                // updated the history after a susscefull scan 
                loadHistory();
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', status, error);
                $results.html('<p class="result-danger">Error scanning target. Please try again.</p>');
                $results.addClass('visible');
            }
        });
    });
});