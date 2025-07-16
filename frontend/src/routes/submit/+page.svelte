<script>
  import { onMount } from 'svelte';
  export let data;
  import { API_URL } from '$lib/api.js';

  // Uw publieke Site Key
  const RECAPTCHA_SITE_KEY = '6LeXOH0rAAAAAE8D6m1cPL3x1ZqCXOlSc4QLcZzV'; 
  
  let message = '';
  let recaptchaContainer; // Een 'anker' voor het reCAPTCHA-element in de HTML

  // --- DE FIX ---
  // Deze onMount-functie is ontworpen om robuust om te gaan met SvelteKit's navigatie.
  onMount(() => {
    const renderRecaptcha = () => {
      // Controleer of de Google-library en ons anker-element bestaan
      if (window.grecaptcha && window.grecaptcha.render && recaptchaContainer) {
        // Leeg de container voor het geval er al een oude, onzichtbare widget was
        recaptchaContainer.innerHTML = ''; 
        // Geef Google expliciet de opdracht om de widget hier te tekenen
        window.grecaptcha.render(recaptchaContainer, {
          'sitekey' : RECAPTCHA_SITE_KEY
        });
      }
    };

    // Maak onze render-functie globaal beschikbaar
    window.onloadCallback = renderRecaptcha;

    // Als het Google-script al bestaat (na eerdere navigatie), voer de functie direct uit
    if (window.grecaptcha && window.grecaptcha.render) {
      renderRecaptcha();
    } else {
      // Als het script nog niet bestaat, voeg het toe aan de pagina.
      // Het 'onload=onloadCallback' zorgt ervoor dat onze functie wordt aangeroepen zodra het script geladen is.
      if (!document.querySelector('#recaptcha-script')) {
        const script = document.createElement('script');
        script.id = 'recaptcha-script';
        script.src = 'https://www.google.com/recaptcha/api.js?onload=onloadCallback&render=explicit';
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
      }
    }
  });
  // --- EINDE FIX ---

  // Uw werkende handleSubmit functie (ongewijzigd)
  async function handleSubmit(event) {
    const formData = new FormData(event.target);
    const recaptchaResponse = formData.get('g-recaptcha-response');

    if (!recaptchaResponse) {
      message = 'Please complete the reCAPTCHA.';
      return;
    }

    const quoteData = {
      text: formData.get('text'),
      author_name: formData.get('author_name'),
      source_id: formData.get('source_id'),
      'g-recaptcha-response': recaptchaResponse,
       'category_ids': []
    };

    try {
      const response = await fetch(`${API_URL}/api/submit/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(quoteData),
      });

      const result = await response.json();
      if (response.ok) {
        message = 'Quote successfully submitted!';
        event.target.reset();
        if (window.grecaptcha) window.grecaptcha.reset();
      } else {
        message = `Failed to submit quote: ${result.detail || JSON.stringify(result)}`;
      }
    } catch (error) {
      message = 'An error occurred while submitting the quote.';
    }
  }
</script>

<h1>Submit a New Quote</h1>

{#if message}
  <p class="message">{message}</p>
{/if}

<form on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="text">Quote Text:</label>
    <textarea id="text" name="text" rows="6" required></textarea>
  </div>

  <div>
    <label for="author_name">Author Name (optional):</label>
    <input type="text" id="author_name" name="author_name" />
  </div>

  <div>
    <label for="source_id">Source (optional):</label>
    {#if data.sources}
      <select id="source_id" name="source_id">
        <option value="">-- Select a Source --</option>
        {#each data.sources as source}
          <option value={source.id}>{source.name}</option>
        {/each}
      </select>
    {/if}
  </div>
  
  <div bind:this={recaptchaContainer}></div>

  <button type="submit">Submit Quote</button>
</form>

<style>
  /* Uw bestaande CSS-stijlen blijven hier ongewijzigd */
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 700;
  }
  input, textarea, select {
    width: 100%;
    padding: 0.8rem;
    font-family: 'EB Garamond', serif;
    font-size: 1.1rem;
    border: 1px solid #ccc;
    background-color: #fff;
  }
  button {
    margin-top: 1rem;
    padding: 0.8rem 1.5rem;
    font-family: 'EB Garamond', serif;
    font-size: 1.2rem;
    background-color: #3D3D3D;
    color: #FDFBF5;
    border: none;
    cursor: pointer;
  }
  .message {
    margin-top: 1rem;
    font-weight: bold;
    color: #B22222;
  }
</style>