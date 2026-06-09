const DEFAULT_BASE = '';

export function addQuery(path, params = {}) {
	const url = new URL(path, 'http://localhost');
	for (const [key, value] of Object.entries(params)) {
		if (value === undefined || value === null || value === '') continue;
		url.searchParams.set(key, String(value));
	}
	return `${url.pathname}${url.search}`;
}

let apiBase = ((import.meta.env && import.meta.env.VITE_API_BASE) || DEFAULT_BASE).trim();

function buildUrl(path) {
	if (!apiBase) return path;
	return `${apiBase.replace(/\/$/, '')}/${String(path).replace(/^\//, '')}`;
}

export async function apiFetch(path, options = {}) {
	const response = await fetch(buildUrl(path), {
		credentials: 'include',
		...options
	});

	if (!response.ok) {
		const message = await safeReadError(response);
		const error = new Error(message || `Request failed: ${response.status}`);
		error.status = response.status;
		throw error;
	}

	return response;
}

export async function getJson(path, options = {}) {
	const response = await apiFetch(path, options);
	return response.json();
}

const jsonBody = (method, path, body) =>
  apiFetch(path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? {})
  }).then(r => r.json());

export const postJson = (path, body) => jsonBody('POST', path, body);
export const patchJson = (path, body) => jsonBody('PATCH', path, body);

export async function deleteJson(path) {
	const response = await apiFetch(path, { method: 'DELETE' });
	if (response.status === 204) return null;
	return response.json();
}

async function safeReadError(response) {
	try {
		const text = await response.text();
		return text?.trim();
	} catch {
		return '';
	}
}
