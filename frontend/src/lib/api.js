// frontend/src/lib/api.js
import { browser } from '$app/environment';
import { PUBLIC_API_URL } from '$env/static/public';

// Dit is de URL die alleen binnen het Docker-netwerk wordt gebruikt (tijdens de build)
const INTERNAL_API_URL = 'http://api:8000';

// We exporteren één constante. Deze is PUBLIC_API_URL in de browser, 
// en INTERNAL_API_URL op de server.
export const API_URL = browser ? PUBLIC_API_URL : INTERNAL_API_URL;