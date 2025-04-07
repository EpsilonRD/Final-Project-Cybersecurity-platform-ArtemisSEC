// static/js/create_news.js

document.addEventListener('DOMContentLoaded', () => {
    const editor = document.getElementById('content-editor');
    const textarea = document.querySelector('textarea[name="content"]');
    const titleInput = document.querySelector('input[name="title"]');
    const imageInput = document.querySelector('input[name="image"]');
    const newsIdInput = document.getElementById('news-id');
    const submitText = document.getElementById('submit-text');
    const formatButtons = document.querySelectorAll('.format-btn');
    const editLinks = document.querySelectorAll('.edit-link');
    const deleteLinks = document.querySelectorAll('.delete-link');

    // Sync initial content from textarea to editor
    if (textarea.value) {
        editor.innerHTML = textarea.value.replace(/\n/g, '<br>');
    }

    // Format button actions
    formatButtons.forEach(button => {
        button.addEventListener('click', () => {
            const action = button.getAttribute('data-action');
            switch (action) {
                case 'bold':
                    document.execCommand('bold', false, null);
                    break;
                case 'italic':
                    document.execCommand('italic', false, null);
                    break;
                case 'bullet':
                    document.execCommand('insertUnorderedList', false, null);
                    break;
                case 'number':
                    document.execCommand('insertOrderedList', false, null);
                    break;
            }
            editor.focus();
            syncContent();
        });
    });

    // Sync editor content to textarea on input
    editor.addEventListener('input', syncContent);

    // Handle edit links
    editLinks.forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            const newsId = link.getAttribute('data-id');
            try {
                const response = await fetch(`/news/api/get/${newsId}/`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                const data = await response.json();
                if (data.success) {
                    titleInput.value = data.news.title;
                    editor.innerHTML = data.news.content;
                    newsIdInput.value = newsId;
                    submitText.textContent = 'Update';
                    imageInput.value = ''; // Reset file input
                    syncContent();
                } else {
                    alert('Error loading news post');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to load news post');
            }
        });
    });

    // Handle delete links
    deleteLinks.forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this post?')) {
                const newsId = link.getAttribute('data-id');
                try {
                    const response = await fetch(`/news/api/delete/${newsId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });
                    const data = await response.json();
                    if (data.success) {
                        link.closest('.history-item').remove();
                    } else {
                        alert('Error deleting news post');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Failed to delete news post');
                }
            }
        });
    });

    // Sync content before form submission
    document.getElementById('news-form').addEventListener('submit', () => {
        syncContent();
    });

    function syncContent() {
        textarea.value = editor.innerHTML;
    }
});