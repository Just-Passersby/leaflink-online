<script>
	import { renderMarkdown } from '$lib/markdown.js';

	let { value = $bindable(''), rows = 10, placeholder = '' } = $props();
	let tab = $state('edit');
	let previewHtml = $derived(renderMarkdown(value));
</script>

<div class="md-editor">
	<div class="md-tabs">
		<button type="button" class:active={tab === 'edit'} onclick={() => (tab = 'edit')}>Edit</button>
		<button type="button" class:active={tab === 'preview'} onclick={() => (tab = 'preview')}
			>Preview</button
		>
	</div>

	{#if tab === 'edit'}
		<textarea {rows} {placeholder} bind:value></textarea>
	{:else}
		<div class="md-preview prose">
			{#if value.trim()}
				{@html previewHtml}
			{:else}
				<p class="empty">Nothing to preview.</p>
			{/if}
		</div>
	{/if}
</div>

<style>
	.md-editor {
		border-radius: 0.75rem;
		border: 1px solid rgba(17, 17, 17, 0.2);
		overflow: hidden;
		background: #fff;
	}

	.md-tabs {
		display: flex;
		border-bottom: 1px solid rgba(17, 17, 17, 0.1);
		background: #f8f4ec;
	}

	.md-tabs button {
		padding: 0.45rem 1rem;
		border: none;
		background: transparent;
		color: #6b5d4c;
		font: inherit;
		font-size: 0.88rem;
		font-weight: 500;
		cursor: pointer;
		border-radius: 0;
		border-bottom: 2px solid transparent;
		margin-bottom: -1px;
	}

	.md-tabs button.active {
		color: #1b1b1b;
		font-weight: 700;
		border-bottom-color: #1b1b1b;
	}

	textarea {
		display: block;
		padding: 0.75rem 0.9rem;
		border: none;
		font: inherit;
		font-size: 0.93rem;
		background: #fff;
		resize: vertical;
		width: 100%;
		box-sizing: border-box;
		outline: none;
		line-height: 1.6;
	}

	.md-preview {
		padding: 0.9rem 1.1rem;
		min-height: 8rem;
		background: #faf7f2;
		line-height: 1.7;
	}

	.empty {
		color: #6b5d4c;
		font-style: italic;
		margin: 0;
	}

	.prose :global(h1),
	.prose :global(h2),
	.prose :global(h3),
	.prose :global(h4) {
		margin: 1rem 0 0.4rem;
		color: #1b1b1b;
		line-height: 1.3;
	}

	.prose :global(h1) {
		font-size: 1.5rem;
	}
	.prose :global(h2) {
		font-size: 1.25rem;
	}
	.prose :global(h3) {
		font-size: 1.05rem;
	}

	.prose :global(p) {
		margin: 0.5rem 0;
		color: #3f3327;
	}

	.prose :global(code) {
		background: #f0e8d8;
		padding: 0.15rem 0.35rem;
		border-radius: 0.35rem;
		font-size: 0.88em;
		font-family: 'Courier New', monospace;
	}

	.prose :global(pre) {
		background: #f0e8d8;
		padding: 0.9rem;
		border-radius: 0.6rem;
		overflow-x: auto;
		margin: 0.75rem 0;
	}

	.prose :global(pre code) {
		background: none;
		padding: 0;
	}

	.prose :global(blockquote) {
		border-left: 3px solid #c9b99a;
		margin: 0.75rem 0;
		padding: 0.2rem 0.9rem;
		color: #6b5d4c;
	}

	.prose :global(ul),
	.prose :global(ol) {
		padding-left: 1.4rem;
		margin: 0.5rem 0;
		color: #3f3327;
	}

	.prose :global(li) {
		margin: 0.2rem 0;
	}

	.prose :global(a) {
		color: #7a5c3a;
		text-decoration: underline;
	}

	.prose :global(hr) {
		border: none;
		border-top: 1px solid #e0d5c5;
		margin: 1rem 0;
	}

	.prose :global(table) {
		border-collapse: collapse;
		width: 100%;
		margin: 0.75rem 0;
		font-size: 0.92rem;
	}

	.prose :global(th),
	.prose :global(td) {
		border: 1px solid #e0d5c5;
		padding: 0.4rem 0.7rem;
		text-align: left;
	}

	.prose :global(th) {
		background: #f3ede3;
		font-weight: 600;
	}

	.prose :global(strong) {
		color: #1b1b1b;
	}

	.prose :global(em) {
		color: #4b3f33;
	}
</style>
