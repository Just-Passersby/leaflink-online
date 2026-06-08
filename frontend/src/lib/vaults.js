import { addQuery, deleteJson, getJson, patchJson, postJson } from '$lib/api.js';

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
