<script>
	import { onMount } from 'svelte';
	import favicon from '$lib/assets/favicon.svg';
	import { authStatus, authUser, fetchMe, logout } from '$lib/auth.js';

	let { children } = $props();

	onMount(() => {
		fetchMe().catch(() => {});
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>Leaflink Online</title>
</svelte:head>

<div class="app">
	<header class="site-header">
		<div class="brand">
			<span class="brand-mark">LL</span>
			<span class="brand-name">Leaflink Online</span>
		</div>
		<nav class="nav">
			<a href="/">Home</a>
			<a href="/vaults">Vaults</a>
			<a href="/search">Search</a>
		</nav>
		<div class="auth-links">
			{#if $authStatus.loading}
				<span class="muted">Checking session...</span>
			{:else if $authUser}
				<span class="user">Hi, {$authUser.username}</span>
				<button class="ghost" type="button" onclick={() => logout().catch(e => console.error('Logout failed', e))}>Logout</button>
			{:else}
				{#if $authStatus.error}
					<span class="muted">{$authStatus.error}</span>
				{/if}
				<a href="/login">Login</a>
				<a class="button" href="/register">Register</a>
			{/if}
		</div>
	</header>

	<main class="content">
		{@render children()}
	</main>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
		color: #1b1b1b;
		background: radial-gradient(circle at top, #fdf6e5 0%, #f7f2e8 42%, #f1efe9 100%);
		min-height: 100vh;
	}
	
	.nav a, .auth-links a, .brand {
		text-decoration: none;
		color: inherit;
	}

	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	.site-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1.5rem;
		padding: 1.25rem 2rem;
		background: rgba(255, 255, 255, 0.92);
		backdrop-filter: blur(12px);
		border-bottom: 1px solid rgba(17, 17, 17, 0.08);
		position: sticky;
		top: 0;
		z-index: 10;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	.brand-mark {
		display: grid;
		place-items: center;
		width: 2.25rem;
		height: 2.25rem;
		border-radius: 0.75rem;
		background: linear-gradient(140deg, #f28c28, #f2c94c);
		color: #1b1b1b;
		font-size: 0.95rem;
	}

	.nav,
	.auth-links {
		display: flex;
		align-items: center;
		gap: 1rem;
		font-size: 0.95rem;
	}

	.auth-links .button {
		padding: 0.55rem 1rem;
		border-radius: 999px;
		background: #1b1b1b;
		color: #fff;
		font-weight: 600;
	}

	.auth-links .ghost {
		padding: 0.45rem 0.85rem;
		border-radius: 999px;
		border: 1px solid #1b1b1b;
		background: transparent;
		font-weight: 600;
	}

	.user {
		font-weight: 600;
	}

	.muted {
		color: #6b5d4c;
		font-size: 0.9rem;
	}

	.content {
		flex: 1;
		padding: 2.5rem 2rem 3.5rem;
	}

	@media (max-width: 820px) {
		.site-header {
			flex-direction: column;
			align-items: flex-start;
		}

		.nav,
		.auth-links {
			flex-wrap: wrap;
		}
	}
</style>
