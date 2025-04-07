// static/js/news_home.js

document.addEventListener('DOMContentLoaded', () => {
    const newsListContainer = document.getElementById('news-list');
    let lastNewsIds = Array.from(document.querySelectorAll('.news-box')).map(box => box.getAttribute('data-id'));

    // Function to fetch and update news list
    async function updateNewsList() {
        try {
            const response = await fetch('/news/api/list/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const data = await response.json();
            const newNewsList = data.news_list;

            // Get current news IDs
            const currentIds = new Set(lastNewsIds);
            const newIds = new Set(newNewsList.map(news => news.id.toString()));

            // Remove deleted posts
            const boxes = newsListContainer.querySelectorAll('.news-box');
            boxes.forEach(box => {
                const id = box.getAttribute('data-id');
                if (!newIds.has(id)) {
                    box.style.opacity = '0';
                    setTimeout(() => box.remove(), 500); // Fade out then remove
                }
            });

            // Add or update posts
            newNewsList.forEach(news => {
                const existingBox = newsListContainer.querySelector(`.news-box[data-id="${news.id}"]`);
                if (!currentIds.has(news.id.toString())) {
                    // New post: Add to top
                    const newsBox = createNewsBox(news);
                    newsListContainer.insertBefore(newsBox, newsListContainer.firstChild);
                    newsBox.style.opacity = '0';
                    setTimeout(() => newsBox.style.opacity = '1', 10); // Fade in
                } else if (existingBox) {
                    // Update existing post (if needed, e.g., title changed)
                    updateNewsBox(existingBox, news);
                }
            });

            // Update last known IDs
            lastNewsIds = Array.from(newIds);
            if (newNewsList.length === 0 && !newsListContainer.querySelector('.no-news')) {
                newsListContainer.innerHTML = '<p class="no-news">No news available.</p>';
            }
        } catch (error) {
            console.error('Error fetching news:', error);
        }
    }

    // Create a news box element
    function createNewsBox(news) {
        const div = document.createElement('div');
        div.className = 'news-box';
        div.setAttribute('data-id', news.id);
        div.innerHTML = `
            <div class="news-image-section">
                ${news.image ? `<img src="${news.image}" alt="${news.title}" class="news-image">` : '<div class="news-placeholder">No Image</div>'}
                <p class="news-meta">
                    <i class="bi bi-person"></i> ${news.author} |
                    <i class="bi bi-calendar"></i> ${news.created_at}
                </p>
            </div>
            <div class="news-details">
                <h2 class="news-title">${news.title}</h2>
                <p class="news-excerpt">${news.content}</p>
                <a href="/news/${news.id}/" class="btn-news">
                    <i class="bi bi-eye"></i> Read More
                </a>
            </div>
        `;
        div.style.transition = 'opacity 0.5s ease'; // Smooth fade
        return div;
    }

    // Update an existing news box (if edited)
    function updateNewsBox(box, news) {
        const title = box.querySelector('.news-title');
        const excerpt = box.querySelector('.news-excerpt');
        const image = box.querySelector('.news-image');
        const placeholder = box.querySelector('.news-placeholder');
        const meta = box.querySelector('.news-meta');

        if (title.textContent !== news.title) title.textContent = news.title;
        if (excerpt.textContent !== news.content) excerpt.innerHTML = news.content;
        if (news.image && image) image.src = news.image;
        else if (!news.image && placeholder) placeholder.style.display = 'flex';
        meta.innerHTML = `<i class="bi bi-person"></i> ${news.author} | <i class="bi bi-calendar"></i> ${news.created_at}`;
    }

    // Poll every 5 seconds
    setInterval(updateNewsList, 5000);

    // Initial update
    updateNewsList();
});