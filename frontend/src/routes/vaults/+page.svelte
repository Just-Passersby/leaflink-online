<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authUser } from '$lib/auth.js';
	import { createVault, getExploreVaults, getMyVaults } from '$lib/vaults.js';

	let myVaults = $state([]);
	let exploreVaults = $state([]);
	let myTotal = $state(0);
	let exploreTotal = $state(0);
	let isLoading = $state(true);
	let errorMessage = $state('');
	let createName = $state('');
	let createPublic = $state(false);
	let creating = $state(false);

	async function loadVaults() {
		isLoading = true;
		errorMessage = '';
		try {
			const [mine, explore] = await Promise.all([
				getMyVaults({ page: 1, size: 100 }),
				getExploreVaults({ page: 1, size: 100 })
			]);
			myVaults = mine.items ?? [];
			myTotal = mine.total ?? myVaults.length;
			exploreVaults = explore.items ?? [];
			exploreTotal = explore.total ?? exploreVaults.length;
		} catch (error) {
			errorMessage = error?.message || 'Failed to load vaults.';
		} finally {
			isLoading = false;
		}
	}

	async function handleCreate(event) {
		event.preventDefault();
		if (creating) return;
		creating = true;
		errorMessage = '';
		try {
			const created = await createVault({ name: createName, public: createPublic });
			createName = '';
			createPublic = false;
			await loadVaults();
			goto(`/vaults/${created.id}`);
		} catch (error) {
			errorMessage = error?.message || 'Failed to create vault.';
		} finally {
			creating = false;
		}
	}

	onMount(() => {
		loadVaults();
	});
</script>

<section class="page-shell">
	<div class="hero">
		<div>
			<p class="eyebrow">Vault management</p>
			<h1>Vaults</h1>
			<p class="subtitle">
				Manage your private workspace and browse public vaults.
			</p>
		</div>

		<form class="create-card" onsubmit={handleCreate}>
			<h2>Create vault</h2>
			<label>
				<span>Name</span>
				<input type="text" bind:value={createName} maxlength="255" required />
			</label>
			<label class="toggle">
				<input type="checkbox" bind:checked={createPublic} />
				<span>Public vault</span>
			</label>
			<button type="submit" disabled={creating || !$authUser}>
				{creating ? 'Creating...' : 'Create vault'}
			</button>
			{#if !$authUser}
				<p class="hint">Sign in to create a vault.</p>
			{/if}
		</form>
	</div>

	{#if errorMessage}
		<p class="error">{errorMessage}</p>
	{/if}

	{#if isLoading}
		<p class="muted">Loading vaults...</p>
	{:else}
		<div class="grid">
			<section class="panel">
				<div class="section-head">
					<h2>My vaults</h2>
					<span>{myTotal}</span>
				</div>
				{#if myVaults.length === 0}
					<p class="empty">You do not have any vaults yet.</p>
				{:else}
					<div class="list">
						{#each myVaults as vault}
							<a class="vault-card" href={`/vaults/${vault.id}`}>
								<div>
									<h3>{vault.name}</h3>
									<p>{vault.public ? 'Public' : 'Private'}</p>
								</div>
								<span>{new Date(vault.created_at).toLocaleDateString()}</span>
							</a>
						{/each}
					</div>
				{/if}
			</section>

			<section class="panel">
				<div class="section-head">
					<h2>Explore public vaults</h2>
					<span>{exploreTotal}</span>
				</div>
				{#if exploreVaults.length === 0}
					<p class="empty">No public vaults yet.</p>
				{:else}
					<div class="list">
						{#each exploreVaults as vault}
							<a class="vault-card" href={`/vaults/${vault.id}`}>
								<div>
									<h3>{vault.name}</h3>
									<p>by {vault.owner_username}</p>
								</div>
								<span>{new Date(vault.created_at).toLocaleDateString()}</span>
							</a>
						{/each}
					</div>
				{/if}
			</section>
		</div>
	{/if}
</section>

<style>
	.page-shell {
		display: grid;
		gap: 1.5rem;
	}

	.hero {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 1.5rem;
		align-items: start;
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
	h3,
	p {
		margin: 0;
	}

	.subtitle {
		margin-top: 0.75rem;
		color: #3f3327;
		line-height: 1.6;
	}

	.create-card,
	.panel {
		background: rgba(255, 255, 255, 0.95);
		padding: 1.25rem;
		border-radius: 1.25rem;
		box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
	}

	.create-card {
		display: grid;
		gap: 0.9rem;
	}

	.create-card h2 {
		font-size: 1.05rem;
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

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 1.25rem;
	}

	.section-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 1rem;
	}

	.list {
		display: grid;
		gap: 0.75rem;
	}

	.vault-card {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		padding: 0.95rem 1rem;
		border-radius: 1rem;
		border: 1px solid rgba(17, 17, 17, 0.08);
		text-decoration: none;
		color: inherit;
		background: #fff;
	}

	.vault-card p {
		margin-top: 0.2rem;
		color: #6b5d4c;
		font-size: 0.92rem;
	}

	.empty,
	.muted,
	.hint {
		color: #6b5d4c;
	}

	.error {
		color: #9b3a2d;
		font-weight: 600;
	}

	@media (max-width: 640px) {
		.vault-card {
			align-items: flex-start;
			flex-direction: column;
		}
	}
</style>
