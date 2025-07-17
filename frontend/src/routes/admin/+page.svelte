<!-- // frontend/src/routes/admin/+page.server.js -->
<script>
  import { API_URL } from '$lib/api.js';
  export let data;
  let pendingQuotes = data.quotes || [];

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  async function approveQuote(id) {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(`${API_URL}/api/moderation/${id}/approve/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      credentials: 'include', // <-- DEZE REGEL IS TOEGEVOEGD
    });
    if (response.ok) {
      pendingQuotes = pendingQuotes.filter(q => q.id !== id);
    } else {
      alert('Goedkeuren mislukt!');
    }
  }

  async function deleteQuote(id) {
    if (!confirm('Weet je zeker dat je deze quote wilt verwijderen?')) return;
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(`${API_URL}/api/moderation/${id}/`, {
      method: 'DELETE',
      headers: { 'X-CSRFToken': csrftoken },
      credentials: 'include', // <-- DEZE REGEL IS TOEGEVOEGD
    });
    if (response.ok) {
      pendingQuotes = pendingQuotes.filter(q => q.id !== id);
    } else {
      alert('Verwijderen mislukt!');
    }
  }
</script>

<svelte:head>
  <title>Beheer Quotes</title>
</svelte:head>

<div class="container">
  <h1>Quotes in Afwachting</h1>
  {#if pendingQuotes.length > 0}
    <ul class="quote-list">
      {#each pendingQuotes as quote (quote.id)}
        <li class="quote-item">
          <blockquote class="quote-text">"{quote.text}"</blockquote>
          <p class="quote-author">- {quote.author?.name || 'Onbekend'}</p>
          <div class="actions">
            <button class="approve-btn" on:click={() => approveQuote(quote.id)}>Goedkeuren</button>
            <button class="delete-btn" on:click={() => deleteQuote(quote.id)}>Verwijderen</button>
          </div>
        </li>
      {/each}
    </ul>
  {:else}
    <p>Er zijn geen quotes die wachten op goedkeuring. ✅</p>
  {/if}
</div>

<style>
  .container { max-width: 800px; margin: 2rem auto; padding: 1rem; }
  .quote-list { list-style: none; padding: 0; }
  .quote-item { border: 1px solid #ccc; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
  .quote-text { font-style: italic; margin: 0; }
  .quote-author { text-align: right; color: #555; }
  .actions { margin-top: 1rem; display: flex; gap: 1rem; }
  .approve-btn { background-color: #28a745; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer; }
  .delete-btn { background-color: #dc3545; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer; }
</style>