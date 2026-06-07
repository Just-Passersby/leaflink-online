<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { authUser } from '$lib/auth.js';
	import { createNote, getVaultNotes } from '$lib/notes.js';
	import { getVault, removeVault, updateVault } from '$lib/vaults.js';

	let vault = $state(null);
	let isOwner = $state(false);
	let isLoading = $state(true);
	let errorMessage = $state('');
	let notes = $state([]);
	let notesLoading = $state(true);
	let notesError = $state('');
	let name = $state('');
	let publicValue = $state(false);
	let saving = $state(false);
	let deleting = $state(false);
	let creatingNote = $state(false);
	let noteTitle = $state('');
	let noteContent = $state('');
	let noteTags = $state('');

	function normalizeTags(value) {
		return value
			.split(',')
			.map((tag) => tag.trim())
			.filter(Boolean);
	}

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

	async function loadNotes() {
		notesLoading = true;
		notesError = '';
		try {
			const response = await getVaultNotes(page.params.id, { page: 1, size: 100 });
			notes = response.items ?? [];
		} catch (error) {
			notesError = error?.message || 'Failed to load notes.';
		} finally {
			notesLoading = false;
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

	async function handleCreateNote(event) {
		event.preventDefault();
		if (creatingNote) return;
		creatingNote = true;
		notesError = '';
		try {
			const created = await createNote({
				vault_id: Number(page.params.id),
				title: noteTitle,
				content: noteContent,
				tags: normalizeTags(noteTags)
			});
			noteTitle = '';
			noteContent = '';
			noteTags = '';
			await loadNotes();
			goto(`/notes/${created.id}`);
		} catch (error) {
			notesError = error?.message || 'Failed to create note.';
		} finally {
			creatingNote = false;
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
		loadNotes();
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
			<form class="panel" onsubmit={handleSave}>
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
					<button type="button" class="danger" onclick={handleDelete} disabled={deleting}>
						{deleting ? 'Deleting...' : 'Delete vault'}
					</button>
				</div>
			</form>
		{:else}
			<div class="panel">
				<p class="muted">You can view this vault, but only the owner can edit it.</p>
			</div>
		{/if}

		<section class="panel notes-panel">
			<div class="section-head">
				<h2>Notes</h2>
				<span>{notes.length}</span>
			</div>

			{#if isOwner}
				<form class="note-form" onsubmit={handleCreateNote}>
					<label>
						<span>Title</span>
						<input type="text" bind:value={noteTitle} maxlength="255" required />
					</label>
					<label>
						<span>Content</span>
						<textarea bind:value={noteContent} rows="6" placeholder="# Heading\n\nWrite your note here..."></textarea>
					</label>
					<label>
						<span>Tags</span>
						<input type="text" bind:value={noteTags} placeholder="linux, btrfs, setup" />
					</label>
					<button type="submit" disabled={creatingNote}>
						{creatingNote ? 'Creating...' : 'Create note'}
					</button>
				</form>
			{/if}

			{#if notesLoading}
				<p class="muted">Loading notes...</p>
			{:else if notesError}
				<p class="error">{notesError}</p>
			{:else if notes.length === 0}
				<p class="muted">No notes in this vault yet.</p>
			{:else}
				<div class="notes-list">
					{#each notes as note}
						<a class="note-card" href={`/notes/${note.id}`}>
							<div>
								<h3>{note.title}</h3>
								<p>{new Date(note.updated_at).toLocaleString()}</p>
							</div>
							<div class="tag-row">
								{#each note.tags as tag}
									<span class="tag">{tag.name}</span>
								{/each}
							</div>
						</a>
					{/each}
				</div>
			{/if}
		</section>

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
	h3,
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

	.section-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
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

	.note-form {
		display: grid;
		gap: 0.9rem;
	}

	.notes-list {
		display: grid;
		gap: 0.75rem;
	}

	.note-card {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		align-items: flex-start;
		padding: 0.95rem 1rem;
		border-radius: 1rem;
		border: 1px solid rgba(17, 17, 17, 0.08);
		text-decoration: none;
		color: inherit;
		background: #fff;
	}

	.note-card p {
		margin-top: 0.2rem;
		color: #6b5d4c;
		font-size: 0.92rem;
	}

	.tag-row {
		display: flex;
		gap: 0.45rem;
		flex-wrap: wrap;
		justify-content: flex-end;
	}

	.tag {
		padding: 0.28rem 0.55rem;
		border-radius: 999px;
		background: #f3ede3;
		color: #4b3f33;
		font-size: 0.82rem;
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

	.notes-panel {
		gap: 1rem;
	}

	@media (max-width: 640px) {
		.note-card {
			flex-direction: column;
		}
	}
</style>
