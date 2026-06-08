import { addQuery, apiFetch, deleteJson, getJson, patchJson, postJson } from '$lib/api.js';

export function getVaultNotes(vaultId, params = {}) {
	return getJson(addQuery(`/vaults/${vaultId}/notes`, params));
}

export function getNote(noteId) {
	return getJson(`/notes/${noteId}`);
}

export function createNote(payload) {
	return postJson('/notes', payload);
}

export function updateNote(noteId, payload) {
	return patchJson(`/notes/${noteId}`, payload);
}

export function removeNote(noteId) {
	return deleteJson(`/notes/${noteId}`);
}

export function searchNotes(params = {}) {
	return getJson(addQuery('/search', params));
}

export async function uploadNote(vaultId, file, tags = '') {
	const form = new FormData();
	form.append('vault_id', String(vaultId));
	form.append('file', file);
	form.append('tags', tags);
	const response = await apiFetch('/notes/upload', { method: 'POST', body: form });
	return response.json();
}
