// src/routes/+layout.js
import { API_URL } from '$lib/api.js';

/** @type {import('@sveltejs/kit').LayoutLoad} */
export async function load({ fetch }) {
  try {
    const response = await fetch(`${API_URL}/api/sources/`);
    if (!response.ok) {
      throw new Error('Failed to fetch sources');
    }
    const sources = await response.json();
    return { sources };
  } catch (error) {
    console.error("Error fetching sources:", error);
    return { sources: [] };
  }
}