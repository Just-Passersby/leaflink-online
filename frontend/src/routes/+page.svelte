<section class="hero">
	<div>
		<p class="eyebrow">SvelteKit + FastAPI + PostgreSQL</p>
		<h1>Leaflink Online</h1>
		<p class="subtitle">
			A lightweight web vault for markdown notes, tags, and backlinks.
		</p>
		<div class="actions">
			<a class="primary" href="/vaults">Open vaults</a>
			<a class="ghost" href="/search">Search notes</a>
		</div>
	</div>
	<div class="card">
		<h3>Features</h3>
		<ul>
			<li>Markdown notes with live preview</li>
			<li><code>[[WikiLink]]</code> backlinks</li>
			<li>Tags &amp; full-text search</li>
			<li>Public &amp; private vaults</li>
		</ul>
	</div>
</section>

<style>
	.hero {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 2.5rem;
		align-items: center;
	}

	.eyebrow {
		text-transform: uppercase;
		letter-spacing: 0.2em;
		font-size: 0.75rem;
		color: #6b5d4c;
		margin: 0 0 0.75rem;
	}

	h1 {
		font-size: clamp(2.4rem, 4vw, 3.4rem);
		margin: 0 0 1rem;
	}

	.subtitle {
		font-size: 1.1rem;
		color: #3f3327;
		line-height: 1.6;
		margin-bottom: 2rem;
	}

	.actions {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
	}

	.primary,
	.ghost {
		padding: 0.7rem 1.5rem;
		border-radius: 999px;
		font-weight: 600;
		border: 1px solid #1b1b1b;
	}

	.primary {
		background: #1b1b1b;
		color: #fff;
	}

	.ghost {
		background: transparent;
		color: #1b1b1b;
	}

	.card {
		background: rgba(255, 255, 255, 0.9);
		padding: 1.5rem;
		border-radius: 1.25rem;
		box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
	}

	.card ul {
		margin: 0;
		padding-left: 1.25rem;
		color: #4b3f33;
	}
</style>
