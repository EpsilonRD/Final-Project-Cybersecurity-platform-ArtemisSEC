// integrity/static/js/integrity.js

$(document).ready(function() {
    const historyList = $('#history-list');
    const historyUrl = historyList.data('url');

    // Función para cargar el historial
    function loadHistory() {
        $.ajax({
            url: historyUrl,
            method: 'GET',
            success: function(data) {
                if (data.history && data.history.length > 0) {
                    let html = '';
                    data.history.forEach(function(item) {
                        const statusClass = item.is_valid ? 'text-success' : 'text-danger';
                        html += `
                            <div class="history-item">
                                <p>${item.file_name}</p>
                                <p class="${statusClass}">${item.is_valid ? 'Valid' : 'Invalid'} (${item.algorithm})</p>
                                <small>${item.timestamp}</small>
                                <a href="?check_id=${item.id}" class="view-results">View Results</a>
                            </div>
                        `;
                    });
                    historyList.html(html);
                } else {
                    historyList.html('<p>No history available.</p>');
                }
            },
            error: function() {
                historyList.html('<p>Error loading history.</p>');
            }
        });
    }

    // Cargar historial al iniciar
    loadHistory();

    // Actualizar historial después de enviar el formulario
    $('.integrity-form').on('submit', function(e) {
        setTimeout(loadHistory, 1000); // Retraso para dar tiempo a que se guarde el nuevo registro
    });
});