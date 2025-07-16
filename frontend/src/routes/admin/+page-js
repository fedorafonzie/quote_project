// frontend/src/routes/admin/+page.js
import { API_URL } from '$lib/api.js';

export async function load({ fetch }) {
  try {
    // Voeg { credentials: 'include' } toe om de login-cookie mee te sturen
    const response = await fetch(`${API_URL}/api/moderation/`, { credentials: 'include' });

    if (!response.ok) {
      console.error('Failed to fetch pending quotes, status:', response.status);
      throw new Error(`Failed to fetch pending quotes. Status: ${response.status}`);
    }
    const quotes = await response.json();
    return { quotes };
  } catch (error) {
    console.error("Error in admin load function:", error);
    return { quotes: [] };
  }
}