import { addQuery, deleteJson, getJson, patchJson, postJson } from '$lib/api.js';

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
