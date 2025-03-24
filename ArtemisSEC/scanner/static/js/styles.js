$(document).ready(function() {
    function applyStyles() {
      
        document.querySelectorAll('td.result-safe').forEach(el => {
            el.style.color = '#28a745';
            el.style.fontWeight = 'bold';
        });
        document.querySelectorAll('td.result-unsupported').forEach(el => {
            el.style.color = '#6c757d';
        });
        document.querySelectorAll('td.result-danger').forEach(el => {
            el.style.color = '#dc3545';
            el.style.fontWeight = 'bold';
            el.style.backgroundColor = 'rgba(220, 53, 69, 0.1)';
        });
        document.querySelectorAll('td.result-timeout').forEach(el => {
            el.style.color = '#ffc107';
        });
        document.querySelectorAll('td.result-unknown').forEach(el => {
            el.style.color = '#6c757d';
        });

        // Debug
        console.log('Total result-safe elements:', document.querySelectorAll('td.result-safe').length);
        document.querySelectorAll('td.result-safe').forEach((el, index) => {
            console.log(`result-safe #${index}: text=${el.textContent}, color=${el.style.color}`);
        });
    }

    const observer = new MutationObserver((mutations) => {
        mutations.forEach(() => {
            console.log('Mutation detected, applying styles');
            applyStyles();
        });
    });
    observer.observe(document.getElementById('result'), { childList: true, subtree: true });

    setTimeout(applyStyles, 100);
});