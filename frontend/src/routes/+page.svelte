<script>
  import { API_URL } from '$lib/api.js'
  export let data;
  let quote = data.quote; // Start met de quote die bij het laden is meegegeven

  async function fetchNewQuote() {
    try {
      const response = await fetch(`${API_URL}/api/quotes/random/`);
      if (!response.ok) throw new Error('Failed to fetch new quote');
      quote = await response.json(); // Update de 'quote' variabele met de nieuwe data
    } catch (error) {
      console.error("Error fetching new quote:", error);
      quote = {
        text: "Could not load a new quote.",
        author: "System"
      };
    }
  }
</script>

<div class="quote-container">
  {#if quote}
    <blockquote class="quote-text">
      {@html quote.text.replace(/\n/g, '<br/>')}
    </blockquote>
    <p class="quote-author">
      — {quote.author || 'Unknown'}
    </p>
  {:else}
    <p>Loading quote...</p>
  {/if}

  <button on:click={fetchNewQuote}>
    Get Another Quote
  </button>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,700;1,400&display=swap');

  .quote-container {
    font-family: 'EB Garamond', serif;
    background-color: #FDFBF5;
    color: #3D3D3D;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
  }

  .quote-text {
    font-size: 2.5rem;
    font-style: italic;
    max-width: 800px;
    line-height: 1.4;
    margin: 0;
  }

  .quote-author {
    font-size: 1.5rem;
    margin-top: 2rem;
    font-weight: 700;
  }

  button {
    margin-top: 3rem;
    padding: 0.8rem 1.5rem;
    font-family: 'EB Garamond', serif;
    font-size: 1.2rem;
    background-color: #3D3D3D;
    color: #FDFBF5;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: #555;
  }
</style>