import { deleteJson, getJson, patchJson, postJson } from '$lib/api.js';

function addQuery(path, params = {}) {
	const url = new URL(path, 'http://localhost');
	for (const [key, value] of Object.entries(params)) {
		if (value === undefined || value === null || value === '') continue;
		url.searchParams.set(key, String(value));
	}
	return `${url.pathname}${url.search}`;
}

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
