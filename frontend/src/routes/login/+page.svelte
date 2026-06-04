<script>
	import { goto } from '$app/navigation';
	import { login } from '$lib/auth.js';

	let username = '';
	let password = '';
	let errorMessage = $state('');
	let isSubmitting = $state(false);

	async function handleSubmit(event) {
		event.preventDefault();
		if (isSubmitting) return;

		isSubmitting = true;
		errorMessage = '';
		try {
			await login({ username, password });
			goto('/vaults');
		} catch (error) {
			errorMessage = error?.message || 'Login failed.';
		} finally {
			isSubmitting = false;
		}
	}
</script>

<section class="auth">
	<div>
		<p class="eyebrow">Welcome back</p>
		<h1>Login</h1>
		<p class="subtitle">Use your username and password to continue.</p>
	</div>

	<form class="card" onsubmit={handleSubmit}>
		<label>
			<span>Username</span>
			<input type="text" bind:value={username} autocomplete="username" required />
		</label>
		<label>
			<span>Password</span>
			<input type="password" bind:value={password} autocomplete="current-password" required />
		</label>
		{#if errorMessage}
			<p class="error">{errorMessage}</p>
		{/if}
		<button type="submit" disabled={isSubmitting}>
			{isSubmitting ? 'Signing in...' : 'Login'}
		</button>
		<p class="hint">
			No account yet? <a href="/register">Create one</a>
		</p>
	</form>
</section>

<style>
	.auth {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
		gap: 2.5rem;
		align-items: start;
	}

	.eyebrow {
		text-transform: uppercase;
		letter-spacing: 0.2em;
		font-size: 0.75rem;
		color: #6b5d4c;
		margin: 0 0 0.75rem;
	}

	.subtitle {
		color: #3f3327;
		line-height: 1.6;
	}

	.card {
		background: rgba(255, 255, 255, 0.95);
		padding: 1.75rem;
		border-radius: 1.25rem;
		box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
		display: grid;
		gap: 1rem;
	}

	label {
		display: grid;
		gap: 0.5rem;
		font-weight: 600;
		color: #3f3327;
	}

	input {
		padding: 0.7rem 0.9rem;
		border-radius: 0.75rem;
		border: 1px solid rgba(17, 17, 17, 0.2);
		font: inherit;
		background: #fff;
	}

	button {
		padding: 0.7rem 1.2rem;
		border-radius: 999px;
		border: none;
		background: #1b1b1b;
		color: #fff;
		font-weight: 600;
		cursor: pointer;
	}

	button:disabled {
		opacity: 0.7;
		cursor: not-allowed;
	}

	.error {
		color: #9b3a2d;
		font-weight: 600;
		margin: 0;
	}

	.hint {
		margin: 0;
		font-size: 0.9rem;
		color: #6b5d4c;
	}

	.hint a {
		font-weight: 600;
	}
</style>
