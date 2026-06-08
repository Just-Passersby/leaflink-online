<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { searchNotes } from '$lib/notes.js';

	let query = $state('');
	let results = $state([]);
	let total = $state(0);
	let isLoading = $state(false);
	let searched = $state(false);
	let errorMessage = $state('');

	async function doSearch() {
		if (!query.trim()) return;
		isLoading = true;
		errorMessage = '';
		searched = true;
		try {
			goto(`/search?q=${encodeURIComponent(query.trim())}`, { replaceState: true, noScroll: true });
			const res = await searchNotes({ q: query.trim(), page: 1, size: 50 });
			results = res.items ?? [];
			total = res.total ?? 0;
		} catch (error) {
			errorMessage = error?.message || 'Search failed.';
		} finally {
			isLoading = false;
		}
	}

	function handleSubmit(event) {
		event.preventDefault();
		doSearch();
	}

	onMount(() => {
		const q = page.url.searchParams.get('q');
		if (q) {
			query = q;
			doSearch();
		}
	});
</script>

<section class="page-shell">
	<div class="hero">
		<p class="eyebrow">Full-text search</p>
		<h1>Search notes</h1>
		<p class="subtitle">Searches public vaults and your own private vaults.</p>
	</div>

	<form class="search-bar" onsubmit={handleSubmit}>
		<input
			type="search"
			bind:value={query}
			placeholder="Search keywords..."
			autocomplete="off"
		/>
		<button type="submit" disabled={isLoading || !query.trim()}>
			{isLoading ? 'Searching...' : 'Search'}
		</button>
	</form>

	{#if errorMessage}
		<p class="error">{errorMessage}</p>
	{/if}

	{#if searched && !isLoading}
		<div class="result-header">
			<span>{total} result{total !== 1 ? 's' : ''} for <strong>"{query}"</strong></span>
		</div>

		{#if results.length === 0}
			<p class="muted">No notes matched your search.</p>
		{:else}
			<div class="result-list">
				{#each results as note}
					<a class="result-card" href={`/notes/${note.id}`}>
						<div class="result-main">
							<h3>{note.title}</h3>
							<p class="meta">
								In <span class="vault-name">{note.vault_name}</span> · by {note.owner_username} ·
								{new Date(note.updated_at).toLocaleDateString()}
							</p>
						</div>
						<div class="tag-row">
							{#each (note.tags ?? []) as tag}
								<span class="tag">{tag.name}</span>
							{/each}
						</div>
					</a>
				{/each}
			</div>
		{/if}
	{/if}
</section>

<style>
	.page-shell {
		display: grid;
		gap: 1.5rem;
	}

	.hero {
		display: grid;
		gap: 0.4rem;
	}

	.eyebrow {
		text-transform: uppercase;
		letter-spacing: 0.2em;
		font-size: 0.75rem;
		color: #6b5d4c;
		margin: 0;
	}

	h1,
	p {
		margin: 0;
	}

	.subtitle {
		color: #3f3327;
	}

	.search-bar {
		display: flex;
		gap: 0.75rem;
	}

	.search-bar input {
		flex: 1;
		padding: 0.75rem 1rem;
		border-radius: 999px;
		border: 1px solid rgba(17, 17, 17, 0.2);
		font: inherit;
		font-size: 1rem;
		background: #fff;
		outline: none;
	}

	.search-bar input:focus {
		border-color: #1b1b1b;
	}

	button {
		padding: 0.75rem 1.5rem;
		border-radius: 999px;
		border: none;
		background: #1b1b1b;
		color: #fff;
		font-weight: 600;
		cursor: pointer;
		white-space: nowrap;
	}

	button:disabled {
		opacity: 0.55;
		cursor: not-allowed;
	}

	.result-header {
		color: #6b5d4c;
		font-size: 0.92rem;
	}

	.result-list {
		display: grid;
		gap: 0.75rem;
	}

	.result-card {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 1rem;
		padding: 1rem 1.15rem;
		border-radius: 1.1rem;
		border: 1px solid rgba(17, 17, 17, 0.08);
		background: rgba(255, 255, 255, 0.95);
		box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
		text-decoration: none;
		color: inherit;
	}

	.result-card:hover {
		border-color: rgba(17, 17, 17, 0.2);
	}

	.result-main h3 {
		margin: 0 0 0.3rem;
		font-size: 1rem;
	}

	.meta {
		margin: 0;
		font-size: 0.88rem;
		color: #6b5d4c;
	}

	.vault-name {
		font-weight: 600;
		color: #4b3f33;
	}

	.tag-row {
		display: flex;
		gap: 0.4rem;
		flex-wrap: wrap;
		justify-content: flex-end;
		flex-shrink: 0;
	}

	.tag {
		padding: 0.25rem 0.55rem;
		border-radius: 999px;
		background: #f3ede3;
		color: #4b3f33;
		font-size: 0.82rem;
	}

	.muted {
		color: #6b5d4c;
	}

	.error {
		color: #9b3a2d;
		font-weight: 600;
	}

	@media (max-width: 560px) {
		.search-bar {
			flex-direction: column;
		}

		.result-card {
			flex-direction: column;
		}

		.tag-row {
			justify-content: flex-start;
		}
	}
</style>
