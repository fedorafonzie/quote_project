// quote_frontend/src/routes/+page.js
import { API_URL } from '$lib/api.js';

export async function load({ fetch }) {
  try {
    // Doe een verzoek naar uw draaiende API
    const response = await fetch(`${API_URL}/api/quotes/random/`);

    if (!response.ok) {
      throw new Error('Failed to fetch quote');
    }

    const quote = await response.json();

    return {
      quote: quote
    };
  } catch (error) {
    console.error("Error fetching quote:", error);
    return {
      quote: {
        text: "Could not load quote. Is the API server running?",
        author: "System"
      }
    };
  }
}