const DEFAULT_BASE = '';

let apiBase = (import.meta?.env?.VITE_API_BASE ?? DEFAULT_BASE).trim();

export function setApiBase(baseUrl) {
	apiBase = (baseUrl ?? '').trim();
}

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

export async function postJson(path, body) {
	const response = await apiFetch(path, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(body ?? {})
	});
	return response.json();
}

export async function patchJson(path, body) {
	const response = await apiFetch(path, {
		method: 'PATCH',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(body ?? {})
	});
	return response.json();
}

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
