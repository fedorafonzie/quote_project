// frontend/src/routes/source/[id]/+page.js
import { API_URL } from '$lib/api.js';

// Jouw JSDoc types - Dit is goede praktijk!
/**
 * @typedef {{
 * count: number;
 * next: string | null;
 * previous: string | null;
 * results: Array<{ id: number; text: string; source: { name: string } | null; }>;
 * }} PaginatedQuotes
 */

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params, url }) {
  const sourceId = params.id;
  const page = url.searchParams.get('page') || '1';
  const apiUrl = `${API_URL}/api/quotes/?source=${sourceId}&page=${page}`;

  console.log("Aanvraag naar API URL:", apiUrl); // <-- DEBUG LOG 1

  try {
    const response = await fetch(apiUrl);
    console.log("Antwoord van API, Status:", response.status); // <-- DEBUG LOG 2

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    /** @type {PaginatedQuotes} */
    const paginatedData = await response.json();
    console.log("Ontvangen data:", paginatedData); // <-- DEBUG LOG 3

    const quotes = paginatedData.results || [];
    // Aangepast om correct de naam uit het geneste source-object te halen
    const sourceName = quotes.length > 0 && quotes[0].source ? quotes[0].source.name : "Category";

    // Data direct teruggeven, ZONDER 'props' object
    return {
      quotes: quotes,
      sourceName: sourceName,
      count: paginatedData.count,
      pageSize: 50,
      currentPage: parseInt(page, 10),
      sourceId: sourceId,
    };

  } catch (error) {
    console.error(`Error fetching quotes for source ${sourceId}:`, error);
    return { 
      error: error instanceof Error ? error.message : String(error), 
      quotes: [], 
      sourceName: "Error" 
    };
  }
}