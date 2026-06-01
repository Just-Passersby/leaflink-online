import.meta.env.VITE_API_BASE

const DEFAULT_BASE = '';

let apiBase = (import.meta?.env?.VITE_API_BASE ?? DEFAULT_BASE).trim();

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

export async function getJson(path) {
	const response = await apiFetch(path);
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
