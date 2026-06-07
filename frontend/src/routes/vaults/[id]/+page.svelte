<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { authUser } from '$lib/auth.js';
	import { getVault, removeVault, updateVault } from '$lib/vaults.js';

	let vault = null;
	let isOwner = false;
	let isLoading = true;
	let errorMessage = '';
	let name = '';
	let publicValue = false;
	let saving = false;
	let deleting = false;

	async function loadVault() {
		isLoading = true;
		errorMessage = '';
		try {
			vault = await getVault(page.params.id);
			name = vault.name;
			publicValue = vault.public;
			isOwner = Boolean($authUser && vault.owner_username === $authUser.username);
		} catch (error) {
			errorMessage = error?.message || 'Failed to load vault.';
		} finally {
			isLoading = false;
		}
	}

	async function handleSave(event) {
		event.preventDefault();
		if (saving) return;
		saving = true;
		errorMessage = '';
		try {
			vault = await updateVault(page.params.id, { name, public: publicValue });
			await loadVault();
		} catch (error) {
			errorMessage = error?.message || 'Failed to update vault.';
		} finally {
			saving = false;
		}
	}

	async function handleDelete() {
		if (deleting) return;
		if (!confirm('Delete this vault? This action cannot be undone.')) return;
		deleting = true;
		errorMessage = '';
		try {
			await removeVault(page.params.id);
			goto('/vaults');
		} catch (error) {
			errorMessage = error?.message || 'Failed to delete vault.';
		} finally {
			deleting = false;
		}
	}

	onMount(() => {
		loadVault();
	});
</script>

<section class="page-shell">
	{#if isLoading}
		<p class="muted">Loading vault...</p>
	{:else if errorMessage && !vault}
		<p class="error">{errorMessage}</p>
	{:else if vault}
		<div class="hero">
			<div>
				<p class="eyebrow">Vault detail</p>
				<h1>{vault.name}</h1>
				<p class="subtitle">
					{vault.public ? 'Public vault' : 'Private vault'} · Owner: {vault.owner_username}
				</p>
			</div>
			<div class="meta-card">
				<span>ID #{vault.id}</span>
				<span>Created {new Date(vault.created_at).toLocaleString()}</span>
			</div>
		</div>

		{#if isOwner}
			<form class="panel" on:submit={handleSave}>
				<h2>Edit vault</h2>
				<label>
					<span>Name</span>
					<input type="text" bind:value={name} maxlength="255" required />
				</label>
				<label class="toggle">
					<input type="checkbox" bind:checked={publicValue} />
					<span>Public vault</span>
				</label>
				<div class="actions">
					<button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save changes'}</button>
					<button type="button" class="danger" on:click={handleDelete} disabled={deleting}>
						{deleting ? 'Deleting...' : 'Delete vault'}
					</button>
				</div>
			</form>
		{:else}
			<div class="panel">
				<p class="muted">You can view this vault, but only the owner can edit it.</p>
			</div>
		{/if}

		{#if errorMessage}
			<p class="error">{errorMessage}</p>
		{/if}
	{/if}
</section>

<style>
	.page-shell {
		display: grid;
		gap: 1.25rem;
	}

	.hero {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		align-items: flex-start;
		flex-wrap: wrap;
	}

	.eyebrow {
		text-transform: uppercase;
		letter-spacing: 0.2em;
		font-size: 0.75rem;
		color: #6b5d4c;
		margin: 0 0 0.75rem;
	}

	h1,
	h2,
	p {
		margin: 0;
	}

	.subtitle {
		margin-top: 0.75rem;
		color: #3f3327;
	}

	.meta-card,
	.panel {
		background: rgba(255, 255, 255, 0.95);
		padding: 1.25rem;
		border-radius: 1.25rem;
		box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
	}

	.meta-card {
		display: grid;
		gap: 0.45rem;
		color: #6b5d4c;
	}

	.panel {
		display: grid;
		gap: 0.9rem;
	}

	label {
		display: grid;
		gap: 0.45rem;
		font-weight: 600;
		color: #3f3327;
	}

	input[type='text'] {
		padding: 0.7rem 0.9rem;
		border-radius: 0.75rem;
		border: 1px solid rgba(17, 17, 17, 0.2);
		font: inherit;
		background: #fff;
	}

	.toggle {
		display: flex;
		align-items: center;
		gap: 0.65rem;
	}

	.actions {
		display: flex;
		gap: 0.75rem;
		flex-wrap: wrap;
	}

	button {
		padding: 0.75rem 1.15rem;
		border-radius: 999px;
		border: none;
		background: #1b1b1b;
		color: #fff;
		font-weight: 600;
		cursor: pointer;
	}

	button:disabled {
		opacity: 0.65;
		cursor: not-allowed;
	}

	button.danger {
		background: #9b3a2d;
	}

	.error {
		color: #9b3a2d;
		font-weight: 600;
	}

	.muted {
		color: #6b5d4c;
	}
</style>
