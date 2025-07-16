import { API_URL } from '$lib/api.js';

export async function load({ fetch }) {
  try {
    // Haal de lijst van alle sources op van uw API
    const response = await fetch(`${API_URL}/api/sources/`);
    if (!response.ok) {
      throw new Error('Failed to fetch sources');
    }
    const sources = await response.json();
    // Geef de sources door aan de +page.svelte pagina
    return { sources };
  } catch (error) {
    console.error("Error fetching sources:", error);
    return { sources: [] };
  }
}