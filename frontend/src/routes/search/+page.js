import { API_URL } from '$lib/api.js';

export async function load({ fetch, url }) {
  const searchTerm = url.searchParams.get('q');
  const page = url.searchParams.get('page') || '1'; // Huidige pagina, standaard 1

  if (!searchTerm) {
    return { results: [], searchTerm: '' };
  }

  try {
    // Voeg de page parameter toe aan de API call
    const response = await fetch(`${API_URL}/api/quotes/?search=${searchTerm}&page=${page}`);
    if (!response.ok) {
      throw new Error('Search request failed');
    }

    const paginatedData = await response.json();
    const results = paginatedData.results || [];

    // Geef alle benodigde data door aan de Svelte-pagina
    return {
      results: results,
      searchTerm: searchTerm,
      count: paginatedData.count,
      pageSize: 50, // De page size van de API
      currentPage: parseInt(page, 10),
    };

  } catch (error) {
    console.error("Error fetching search results:", error);
    return { results: [], searchTerm: searchTerm };
  }
}