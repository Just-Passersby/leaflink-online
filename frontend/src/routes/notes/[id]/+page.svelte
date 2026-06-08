<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { authUser } from '$lib/auth.js';
	import { getNote, removeNote, updateNote } from '$lib/notes.js';
	import { getVault } from '$lib/vaults.js';
	import { marked } from 'marked';
	import DOMPurify from 'dompurify';
	import MarkdownEditor from '$lib/components/MarkdownEditor.svelte';

	let note = $state(null);
	let isOwner = $state(false);
	let isLoading = $state(true);
	let errorMessage = $state('');
	let title = $state('');
	let content = $state('');
	let tagsText = $state('');
	let saving = $state(false);
	let deleting = $state(false);

	function toTagText(tags) {
		return (tags ?? []).map((tag) => tag.name).join(', ');
	}

	function toTagArray(value) {
		return value
			.split(',')
			.map((tag) => tag.trim())
			.filter(Boolean);
	}

	async function loadNote() {
		isLoading = true;
		errorMessage = '';
		try {
			note = await getNote(page.params.id);
			const vault = await getVault(note.vault_id);
			title = note.title;
			content = note.content;
			tagsText = toTagText(note.tags);
			isOwner = Boolean($authUser && vault.owner_username === $authUser.username);
		} catch (error) {
			errorMessage = error?.message || 'Failed to load note.';
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
			note = await updateNote(page.params.id, {
				title,
				content,
				tags: toTagArray(tagsText)
			});
			await loadNote();
		} catch (error) {
			errorMessage = error?.message || 'Failed to update note.';
		} finally {
			saving = false;
		}
	}

	async function handleDelete() {
		if (deleting) return;
		if (!confirm('Delete this note? This action cannot be undone.')) return;
		deleting = true;
		errorMessage = '';
		try {
			await removeNote(page.params.id);
			goto(`/vaults/${note.vault_id}`);
		} catch (error) {
			errorMessage = error?.message || 'Failed to delete note.';
		} finally {
			deleting = false;
		}
	}

	onMount(() => {
		loadNote();
	});
</script>

<section class="page-shell">
	{#if isLoading}
		<p class="muted">Loading note...</p>
	{:else if errorMessage && !note}
		<p class="error">{errorMessage}</p>
	{:else if note}
		<div class="hero">
			<div>
				<p class="eyebrow">Note detail</p>
				<h1>{note.title}</h1>
				<p class="subtitle">In vault #{note.vault_id}</p>
			</div>
			<div class="meta-card">
				<span>Created {new Date(note.created_at).toLocaleString()}</span>
				<span>Updated {new Date(note.updated_at).toLocaleString()}</span>
			</div>
		</div>

		{#if isOwner}
			<form class="panel" onsubmit={handleSave}>
				<h2>Edit note</h2>
				<label>
					<span>Title</span>
					<input type="text" bind:value={title} maxlength="255" required />
				</label>
				<div class="field">
					<span>Content</span>
					<MarkdownEditor bind:value={content} rows={12} placeholder="# Heading&#10;&#10;Write your note here..." />
				</div>
				<label>
					<span>Tags</span>
					<input type="text" bind:value={tagsText} placeholder="linux, btrfs" />
				</label>
				<div class="actions">
					<button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save changes'}</button>
					<button type="button" class="danger" onclick={handleDelete} disabled={deleting}>
						{deleting ? 'Deleting...' : 'Delete note'}
					</button>
				</div>
			</form>
		{/if}

		<div class="layout">
			<section class="panel">
				<h2>Content</h2>
				<div class="prose rendered">
					{@html DOMPurify.sanitize(String(marked.parse(note.content || '')))}
				</div>
			</section>

			<section class="panel">
				<h2>Tags</h2>
				<div class="chip-row">
					{#each note.tags as tag}
						<span class="chip">{tag.name}</span>
					{/each}
				</div>
			</section>

			<section class="panel">
				<h2>Backlinks</h2>
				{#if note.backlinks.length === 0}
					<p class="muted">No backlinks found.</p>
				{:else}
					<div class="link-list">
						{#each note.backlinks as backlink}
							<a href={`/notes/${backlink.id}`}>{backlink.title}</a>
						{/each}
					</div>
				{/if}
			</section>
		</div>

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

	.layout {
		display: grid;
		grid-template-columns: 2fr 1fr;
		gap: 1rem;
	}

	label {
		display: grid;
		gap: 0.45rem;
		font-weight: 600;
		color: #3f3327;
	}

	input[type='text'],
	textarea {
		padding: 0.7rem 0.9rem;
		border-radius: 0.75rem;
		border: 1px solid rgba(17, 17, 17, 0.2);
		font: inherit;
		background: #fff;
	}

	textarea {
		resize: vertical;
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

	.field {
		display: grid;
		gap: 0.45rem;
		font-weight: 600;
		color: #3f3327;
	}

	.rendered {
		padding: 0.9rem 1rem;
		border-radius: 1rem;
		background: #f8f4ec;
		line-height: 1.7;
	}

	.rendered :global(h1),
	.rendered :global(h2),
	.rendered :global(h3),
	.rendered :global(h4) {
		margin: 1rem 0 0.4rem;
		color: #1b1b1b;
	}

	.rendered :global(h1) {
		font-size: 1.5rem;
	}
	.rendered :global(h2) {
		font-size: 1.25rem;
	}
	.rendered :global(h3) {
		font-size: 1.05rem;
	}

	.rendered :global(p) {
		margin: 0.5rem 0;
		color: #3f3327;
	}

	.rendered :global(code) {
		background: #ece3d2;
		padding: 0.15rem 0.35rem;
		border-radius: 0.35rem;
		font-size: 0.88em;
		font-family: 'Courier New', monospace;
	}

	.rendered :global(pre) {
		background: #ece3d2;
		padding: 0.9rem;
		border-radius: 0.6rem;
		overflow-x: auto;
		margin: 0.75rem 0;
	}

	.rendered :global(pre code) {
		background: none;
		padding: 0;
	}

	.rendered :global(blockquote) {
		border-left: 3px solid #c9b99a;
		margin: 0.75rem 0;
		padding: 0.2rem 0.9rem;
		color: #6b5d4c;
	}

	.rendered :global(ul),
	.rendered :global(ol) {
		padding-left: 1.4rem;
		margin: 0.5rem 0;
		color: #3f3327;
	}

	.rendered :global(li) {
		margin: 0.2rem 0;
	}

	.rendered :global(a) {
		color: #7a5c3a;
	}

	.rendered :global(table) {
		border-collapse: collapse;
		width: 100%;
		margin: 0.75rem 0;
		font-size: 0.92rem;
	}

	.rendered :global(th),
	.rendered :global(td) {
		border: 1px solid #e0d5c5;
		padding: 0.4rem 0.7rem;
		text-align: left;
	}

	.rendered :global(th) {
		background: #ece3d2;
		font-weight: 600;
	}

	.rendered :global(hr) {
		border: none;
		border-top: 1px solid #e0d5c5;
		margin: 1rem 0;
	}

	.chip-row {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
	}

	.chip {
		padding: 0.3rem 0.6rem;
		border-radius: 999px;
		background: #f3ede3;
		color: #4b3f33;
	}

	.link-list {
		display: grid;
		gap: 0.5rem;
	}

	.link-list a {
		color: inherit;
	}

	.error {
		color: #9b3a2d;
		font-weight: 600;
	}

	.muted {
		color: #6b5d4c;
	}

	@media (max-width: 760px) {
		.layout {
			grid-template-columns: 1fr;
		}
	}
</style>
