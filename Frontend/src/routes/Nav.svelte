<script lang="ts">
	import Menu from '/home/leon/node_modules/@lucide/svelte/dist/icons/menu';
	import Home from '/home/leon/node_modules/@lucide/svelte/dist/icons/home';
	import Download from '/home/leon/node_modules/@lucide/svelte/dist/icons/download';
	import View from '/home/leon/node_modules/@lucide/svelte/dist/icons/view';
	import Info from '/home/leon/node_modules/@lucide/svelte/dist/icons/info';
	import BookText from '/home/leon/node_modules/@lucide/svelte/dist/icons/book-text';
	import CircleHelp from '/home/leon/node_modules/@lucide/svelte/dist/icons/circle-help';
	import Mail from '/home/leon/node_modules/@lucide/svelte/dist/icons/mail';
	import { fade, fly } from 'svelte/transition';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { onDestroy, onMount } from 'svelte';

	const menuItems = [
		{ href: '/', label: 'Home', icon: Home },
		{ href: '/download', label: 'Download', icon: Download },
		{ href: '/viewer', label: 'NetCDF Viewer', icon: View },
		{ href: '/info/overview', label: 'More Info', icon: Info },
		// {href: '/about', label: 'About', icon: BookText},
		// {href: '/help', label: 'Help', icon: CircleHelp},
		{ href: '/contact', label: 'Contact', icon: Mail }
	];
	const isHome = $derived(page.url.pathname === '/');
	let menuOpen = $state(false);
	let navEl: HTMLElement | null = null;

	function toggleMenu() {
		menuOpen = !menuOpen;
	}

	function handleClickOutside(event: MouseEvent) {
		const target = event.target;

		if (menuOpen && navEl && target instanceof Node && !navEl.contains(target)) {
			menuOpen = false;
		}
	}

	onMount(() => {
		document.addEventListener('click', handleClickOutside);

		return () => {
			document.removeEventListener('click', handleClickOutside);
		};
	});
</script>

<nav bind:this={navEl} class:transparent={isHome}>
	<button class="menu-btn" onclick={() => (menuOpen = !menuOpen)}><Menu /></button>

	<div class="title">Altimetry Portal</div>
</nav>

{#if menuOpen}
	<div class="dropdown" in:fly={{ y: -20, duration: 350 }} out:fade>
		{#each menuItems as item, i}
			<a href={item.href} onclick={toggleMenu}>
				<item.icon />
				<span>{item.label}</span>
			</a>
		{/each}
	</div>
{/if}

<style>
	nav:not(.transparent) {
		display: flex;
		position: fixed;
		width: 100%;
		height: var(--nav-height);
		top: 0;
		z-index: 1;
		align-items: center;
		justify-content: space-between;
		padding: 0.75rem 1.5rem;
		background: rgba(0, 12, 34, 0.2);
		backdrop-filter: blur(5px);
		color: white;
		border-radius: 0 0 12px 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
	}

	nav.transparent {
		display: flex;
		position: sticky;
		height: var(--nav-height);
		top: 0;
		z-index: 1;
		align-items: center;
		justify-content: space-between;
		padding: 0.75rem 1.5rem;
		background: rgba(0, 0, 0, 0);
		color: white;
		border-radius: 0 0 12px 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
	}

	.title {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		font-size: 1.25rem;
		font-weight: bold;
		color: var(--primary,);
		white-space: nowrap;
	}

	.menu-btn {
		background: none;
		border: none;
		font-size: 0rem;
		color: white;
		cursor: pointer;
		transition: color 0.2s ease;
	}

	.menu-btn:hover {
		color: #ccc;
	}

	.dropdown {
		display: flex;
		flex-direction: column;
		position: fixed;
		top: calc(var(--nav-height) + 0.5rem);
		left: 1rem;
		z-index: 100;
		margin-top: 0.5rem;
		padding: 0.75rem;
		gap: 0.5rem;
		background-color: rgba(0, 0, 0, 0.5);
		border-radius: 10px;
		border: 1px solid rgba(255, 255, 255, 0.2);
		box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(5px);
	}

	.dropdown a {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 0.75rem;
		color: white;
		text-decoration: none;
		border-radius: 8px;
		transition:
			background-color 0.2s ease,
			box-shadow 0.2s ease;
	}

	.dropdown a:hover {
		background-color: #383838;
		box-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
		color: #f0f0f0;
	}
</style>
