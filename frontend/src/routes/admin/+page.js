// frontend/src/routes/admin/+page.server.js
import { API_URL } from '$lib/api.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
  console.log('1. ✅ Admin +page.server.js: load() functie gestart.');

  try {
    const urlToFetch = `${API_URL}/api/moderation/`;
    console.log('2. ➡️ Aanvraag naar:', urlToFetch);

    const response = await fetch(urlToFetch, { credentials: 'include' });
    console.log('3. ⬅️ Antwoord van API, Status:', response.status);

    if (!response.ok) {
      throw new Error(`API gaf status ${response.status} terug`);
    }

    const quotes = await response.json();
    console.log('4. 📦 Data ontvangen van API:', quotes);

    return { quotes };
  } catch (error) {
    console.error('❌ Fout in admin load functie:', error);
    return { quotes: [] };
  }
}