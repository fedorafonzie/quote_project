<script>
  export let data;

  // Bereken het totaal aantal pagina's
  $: totalPages = Math.ceil(data.count / data.pageSize);

  // Maak een "slimme" lijst van paginanummers voor responsive weergave
  $: paginationNumbers = (() => {
    if (!totalPages) return [];
    const current = data.currentPage;
    const last = totalPages;
    const delta = 1;
    const left = current - delta;
    const right = current + delta + 1;
    const range = [];
    const rangeWithDots = [];

    for (let i = 1; i <= last; i++) {
      if (i === 1 || i === last || (i >= left && i < right)) {
        range.push(i);
      }
    }

    let l;
    for (const num of range) {
      if (l) {
        if (num - l === 2) {
          rangeWithDots.push(l + 1);
        } else if (num - l !== 1) {
          rangeWithDots.push('...');
        }
      }
      rangeWithDots.push(num);
      l = num;
    }
    return rangeWithDots;
  })();
</script>

<h1 class="page-title">Search Results</h1>

<form action="/search" method="GET" class="search-form">
  <input type="search" name="q" value={data.searchTerm} placeholder="Search for a quote or author..." />
  <button type="submit">Search</button>
</form>

{#if data.searchTerm}
  {#if data.results && data.results.length > 0}
    <p>Found {data.count} quote(s) for "{data.searchTerm}":</p>

    <div class="quote-list">
      {#each data.results as quote}
        <div class="quote-item">
          <blockquote>{@html quote.text.replace(/\n/g, '<br/>')}</blockquote>
          <cite>— {quote.author || 'Unknown'}</cite>
        </div>
      {/each}
    </div>

    <div class="pagination">
      {#if data.currentPage > 1}
        <a href="/search?q={data.searchTerm}&page={data.currentPage - 1}">&laquo; Previous</a>
      {/if}

      {#each paginationNumbers as pageNum}
        {#if typeof pageNum === 'number'}
          {#if pageNum === data.currentPage}
            <span class="current-page">{pageNum}</span>
          {:else}
            <a href="/search?q={data.searchTerm}&page={pageNum}">{pageNum}</a>
          {/if}
        {:else}
          <span class="dots">...</span>
        {/if}
      {/each}

      {#if data.currentPage < totalPages}
        <a href="/search?q={data.searchTerm}&page={data.currentPage + 1}">Next &raquo;</a>
      {/if}
    </div>

  {:else}
    <p>No results found for "{data.searchTerm}".</p>
  {/if}
{/if}

<style>
  .search-form { margin-bottom: 2rem; }
  .page-title { border-bottom: 2px solid #eee; padding-bottom: 0.5rem; }
  .quote-list { padding: 0; }
  .quote-item { margin-top: 2rem; border-top: 1px solid #eee; padding-top: 2rem; }
  blockquote { margin: 0; font-style: italic; font-size: 1.2rem; line-height: 1.6; }
  cite { display: block; text-align: right; margin-top: 1rem; font-weight: bold; }
  .pagination { margin-top: 2.5rem; padding-top: 1.5rem; border-top: 2px solid #eee; text-align: center; font-size: 1.1rem; display: flex; justify-content: center; align-items: center; gap: 0.5rem; flex-wrap: wrap; }
  .pagination a, .pagination .current-page, .pagination .dots { padding: 0.25rem 0.5rem; font-weight: bold; text-decoration: none; color: #3D3D3D; }
  .pagination .current-page { color: #B22222; text-decoration: underline; }
</style>