import { writable } from 'svelte/store';
import { apiFetch, getJson, postJson } from '$lib/api.js';

export const authUser = writable(null);
export const authStatus = writable({ loading: false, error: '' });

export async function fetchMe() {
	authStatus.set({ loading: true, error: '' });
	try {
		const data = await getJson('/auth/me');
		authUser.set(data);
		authStatus.set({ loading: false, error: '' });
		return data;
	} catch (error) {
		if (error?.status === 401 || error?.status === 403) {
			authUser.set(null);
			authStatus.set({ loading: false, error: '' });
			return null;
		}

		authStatus.set({ loading: false, error: error?.message || 'Unable to load user.' });
		throw error;
	}
}

export async function login({ username, password }) {
	const data = await postJson('/auth/login', { username, password });
	authUser.set(data);
	return data;
}

export async function register({ username, email, password }) {
	const data = await postJson('/auth/register', { username, email, password });
	authUser.set(data);
	return data;
}

export async function logout() {
	await apiFetch('/auth/logout', { method: 'POST' });
	authUser.set(null);
}
