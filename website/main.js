// Navigation and Interactive Search Logic for Iconic Vintage Pulp Fiction

document.addEventListener('DOMContentLoaded', () => {
  const views = document.querySelectorAll('.view');
  const sidebar = document.getElementById('sidebar');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const searchInput = document.getElementById('live-search-input');
  const searchClearBtn = document.getElementById('search-clear-btn');
  const searchResultsSection = document.getElementById('search-results-section');
  const searchResultsGrid = document.getElementById('search-results-grid');
  const searchResultsCount = document.getElementById('search-results-count');
  const homeMainContent = document.getElementById('home-main-content');

  // 1. Index all books across all categories for instant lightning-fast search
  const booksIndex = [];
  const bookCardElements = document.querySelectorAll('.view:not(#home) .book-card');
  
  bookCardElements.forEach(card => {
    const parentSection = card.closest('.view');
    const seriesTitle = parentSection ? (parentSection.querySelector('.section-hero h2')?.textContent || '') : '';
    const sectionId = parentSection ? parentSection.id : '';
    const title = card.querySelector('h3')?.textContent || '';
    const author = card.querySelector('.author')?.textContent || '';
    const lang = card.querySelector('.store-badge')?.textContent || '';
    const imgEl = card.querySelector('img');
    const img = imgEl ? (imgEl.getAttribute('src') || '') : '';
    const linkEl = card.querySelector('.btn');
    const link = linkEl ? (linkEl.getAttribute('href') || '#') : '#';
    const numberEl = card.querySelector('.book-number, .book-number-badge');
    const number = numberEl ? numberEl.textContent : '';

    booksIndex.push({
      title,
      author,
      lang,
      series: seriesTitle,
      sectionId,
      img,
      link,
      number,
      html: card.outerHTML
    });
  });

  // 2. Main Navigation function with History API sync
  function navigateTo(targetId, updateHash = true) {
    // If navigating to a non-home view, clear search
    if (targetId !== 'home' && searchInput) {
      searchInput.value = '';
      if (searchClearBtn) searchClearBtn.style.display = 'none';
      if (searchResultsSection) searchResultsSection.style.display = 'none';
      if (homeMainContent) homeMainContent.style.display = 'block';
    }

    // Hide all views
    views.forEach(view => {
      view.classList.remove('active');
    });
    
    // Show target view
    const targetView = document.getElementById(targetId);
    if (targetView) {
      targetView.classList.add('active');
    }

    // Update active state on nav links
    document.querySelectorAll('.nav-list a').forEach(link => {
      link.classList.remove('active');
      if (link.dataset.target === targetId || link.getAttribute('href') === `#${targetId}`) {
        link.classList.add('active');
      }
    });

    // Close sidebar on mobile
    if (window.innerWidth <= 1024 && sidebar) {
      sidebar.classList.remove('open');
    }

    // Synchronize URL hash with history API
    if (updateHash) {
      if (targetId === 'home') {
        if (window.location.hash) {
          history.pushState(null, '', window.location.pathname + window.location.search);
        }
      } else {
        if (window.location.hash !== `#${targetId}`) {
          history.pushState(null, '', `#${targetId}`);
        }
      }
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // 3. Global click listener for any element with data-target or anchor hash
  document.addEventListener('click', (e) => {
    const targetEl = e.target.closest('[data-target], a[href^="#"]');
    if (targetEl) {
      const target = targetEl.dataset.target || targetEl.getAttribute('href')?.replace(/^#/, '');
      if (target) {
        e.preventDefault();
        navigateTo(target);
      }
    }
  });

  // 4. Handle initial deep-link and browser back/forward buttons
  function checkInitialHash() {
    const hash = window.location.hash.replace(/^#/, '');
    if (hash) {
      const el = document.getElementById(hash);
      if (el && el.classList.contains('view')) {
        navigateTo(hash, false);
        return;
      }
    }
  }

  window.addEventListener('popstate', () => {
    const hash = window.location.hash.replace(/^#/, '') || 'home';
    const el = document.getElementById(hash);
    if (el && el.classList.contains('view')) {
      navigateTo(hash, false);
    } else {
      navigateTo('home', false);
    }
  });

  // Check initial hash on load
  checkInitialHash();

  // 5. Live Search Handler
  function handleSearch() {
    const rawQuery = searchInput.value;
    const query = rawQuery.trim().toLowerCase();

    if (!query) {
      if (searchClearBtn) searchClearBtn.style.display = 'none';
      if (searchResultsSection) searchResultsSection.style.display = 'none';
      if (homeMainContent) homeMainContent.style.display = 'block';
      return;
    }

    // Ensure we are on the Home view to show search results
    const homeView = document.getElementById('home');
    if (homeView && !homeView.classList.contains('active')) {
      views.forEach(v => v.classList.remove('active'));
      homeView.classList.add('active');
      document.querySelectorAll('.nav-list a').forEach(l => l.classList.remove('active'));
      const homeLink = document.querySelector('.nav-list a[data-target="home"], .nav-list a[href="#home"]');
      if (homeLink) homeLink.classList.add('active');
    }

    if (searchClearBtn) searchClearBtn.style.display = 'flex';
    if (homeMainContent) homeMainContent.style.display = 'none';
    if (searchResultsSection) searchResultsSection.style.display = 'block';

    const terms = query.split(/\s+/).filter(t => t.length > 0);
    const matched = booksIndex.filter(b => {
      const searchStr = `${b.title} ${b.author} ${b.lang} ${b.series}`.toLowerCase();
      return terms.every(term => searchStr.includes(term));
    });

    if (searchResultsCount) {
      searchResultsCount.textContent = `Found ${matched.length} book${matched.length === 1 ? '' : 's'} matching "${rawQuery}"`;
    }

    if (searchResultsGrid) {
      if (matched.length === 0) {
        searchResultsGrid.innerHTML = `
          <div class="no-results-msg" style="grid-column: 1 / -1;">
            <p>🏜️ No vintage books found matching <strong>"${rawQuery}"</strong>.</p>
            <p style="font-size: 0.9rem; margin-top: 0.5rem; color: #a89070;">Try searching for series names like <em>Sahara</em>, <em>Swart Luiperd</em>, <em>Oloff</em>, or authors like <em>Venter</em>.</p>
          </div>
        `;
      } else {
        searchResultsGrid.innerHTML = matched.map(b => b.html).join('');
      }
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', handleSearch);
  }

  if (searchClearBtn) {
    searchClearBtn.addEventListener('click', () => {
      if (searchInput) {
        searchInput.value = '';
        searchInput.focus();
        handleSearch();
      }
    });
  }

  // 6. Mobile menu toggle
  if (mobileMenuBtn && sidebar) {
    mobileMenuBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 1024) {
        if (!e.target.closest('#sidebar') && !e.target.closest('#mobile-menu-btn') && !e.target.closest('[data-target]') && !e.target.closest('a[href^="#"]')) {
          sidebar.classList.remove('open');
        }
      }
    });
  }
});
