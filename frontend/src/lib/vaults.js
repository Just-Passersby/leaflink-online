import { apiFetch, deleteJson, getJson, patchJson, postJson } from '$lib/api.js';

function addQuery(path, params = {}) {
	const url = new URL(path, 'http://localhost');
	for (const [key, value] of Object.entries(params)) {
		if (value === undefined || value === null || value === '') continue;
		url.searchParams.set(key, String(value));
	}
	return `${url.pathname}${url.search}`;
}

export function getMyVaults(params = {}) {
	return getJson(addQuery('/vaults/mine', params));
}

export function getExploreVaults(params = {}) {
	return getJson(addQuery('/vaults/explore', params));
}

export function getVault(vaultId) {
	return getJson(`/vaults/${vaultId}`);
}

export function createVault(payload) {
	return postJson('/vaults', payload);
}

export function updateVault(vaultId, payload) {
	return patchJson(`/vaults/${vaultId}`, payload);
}

export function removeVault(vaultId) {
	return deleteJson(`/vaults/${vaultId}`);
}

export async function getVaultNotes(vaultId, params = {}) {
	return getJson(addQuery(`/vaults/${vaultId}/notes`, params));
}
