<script>
  export let data;
  let isMenuOpen = false; // Variabele om bij te houden of het mobiele menu open is

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
  }

  function closeMenu() {
    isMenuOpen = false;
  }
</script>

<div class="app-container">
  {#if isMenuOpen}
    <div class="overlay" role="button" tabindex="0" on:click={closeMenu} on:keydown on:keypress on:keyup></div>
  {/if}

  <aside class="nav-drawer" class:open={isMenuOpen}>
    <nav class="mobile-nav">
      <a href="/" on:click={closeMenu}>Home</a>
      <a href="/search" on:click={closeMenu}>Search</a>
      <a href="/submit" on:click={closeMenu}>Submit Quote</a>
      <hr>
      <h3>Categories</h3>
      {#if data.sources && data.sources.length > 0}
        {#each data.sources as source}
          <a href="/source/{source.id}" on:click={closeMenu}>{source.name}</a>
        {/each}
      {/if}
    </nav>
  </aside>

  <header class="app-header">
    <div class="header-left">
      <button class="hamburger" aria-label="Open menu" on:click={toggleMenu}>
        <span></span>
        <span></span>
        <span></span>
      </button>
      <nav class="desktop-nav">
        <a href="/">Home</a>
        <div class="dropdown">
          <button class="dropbtn">Categories</button>
          <div class="dropdown-content">
            {#if data.sources && data.sources.length > 0}
              {#each data.sources as source}
                <a href="/source/{source.id}">{source.name}</a>
              {/each}
            {/if}
          </div>
        </div>
        <a href="/submit">Submit Quote</a>
      </nav>
    </div>
    
    <div class="search-container">
      <form action="/search" method="GET">
        <input type="search" name="q" placeholder="Search..." />
        <button type="submit">Go</button>
      </form>
    </div>
  </header>

  <main class="main-content">
    <slot />
  </main>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: 'EB Garamond', serif;
    background-color: #FDFBF5;
    color: #3D3D3D;
  }
  .app-container { display: flex; flex-direction: column; min-height: 100vh; }
  .app-header {
  /* Stijlen die altijd gelden */
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

/* Media Query voor DESKTOP schermen (breder dan 768px) */
@media (min-width: 769px) {
  .app-header {
    position: sticky;
    top: 0;
    background-color: #f1f1f1;
    border-bottom: 1px solid #ddd;
  }
}
  .header-left { display: flex; align-items: center; gap: 1.5rem; }
  
  /* Desktop Navigatie */
  .desktop-nav { display: flex; align-items: center; gap: 1.5rem; }
  .desktop-nav a { color: #3D3D3D; text-decoration: none; font-size: 1.1rem; font-weight: 700; }
  .dropdown { position: relative; display: inline-block; }
  .dropbtn { background: none; border: none; color: #3D3D3D; font-family: 'EB Garamond', serif; font-size: 1.1rem; font-weight: 700; cursor: pointer; padding: 0; }
  .dropdown-content { display: none; position: absolute; background-color: #FDFBF5; min-width: 220px; box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.1); z-index: 1; border: 1px solid #eee; }
  .dropdown-content a { color: black; padding: 12px 16px; text-decoration: none; display: block; font-size: 1rem; font-weight: 400; }
  .dropdown-content a:hover { background-color: #e9e9e9; }
  .dropdown:hover .dropdown-content { display: block; }

  /* Zoekveld */
  .search-container input { padding: 0.4rem 0.6rem; border: 1px solid #ccc; font-family: 'EB Garamond', serif; font-size: 1rem; }
  .search-container button { padding: 0.4rem 0.8rem; border: 1px solid #ccc; background-color: #3D3D3D; color: #fff; cursor: pointer; font-family: 'EB Garamond', serif; font-size: 1rem; }
  
  /* Mobiele Navigatie (Hamburger & Drawer) */
  .hamburger { display: none; /* Standaard verborgen */ }
  .nav-drawer {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 280px;
    background: #fff;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
    z-index: 200;
    padding: 1rem;
    overflow-y: auto;
  }
  .nav-drawer.open { transform: translateX(0); }
  .mobile-nav a { display: block; padding: 0.8rem 1rem; text-decoration: none; color: #333; font-size: 1.2rem; border-bottom: 1px solid #eee; }
  .mobile-nav h3 { padding: 0 1rem; }
  .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 100; }
  
  .main-content { flex: 1; padding: 2rem; max-width: 900px; margin: 0 auto; width: 100%; }

  /* Media Query voor mobiele schermen */
  @media (max-width: 768px) {
    .desktop-nav { display: none; } /* Verberg desktop menu */
    .hamburger { /* Toon hamburger knop */
      display: flex;
      flex-direction: column;
      gap: 5px;
      cursor: pointer;
      border: none;
      background: none;
      padding: 0;
    }
    .hamburger span {
      display: block;
      width: 25px;
      height: 3px;
      background-color: #333;
    }
  }
</style>