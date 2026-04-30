<script lang="ts">
	import Nav from './Nav.svelte';

	let { children } = $props();
</script>

<div class="layout-wrapper">
	<Nav />
	<div class="content-wrapper">
		<div class="content">
			{@render children()}
		</div>
		<div class="fade-bottom"></div>
	</div>
</div>

<style>
	.layout-wrapper {
		height: 100vh;
		padding-top: calc(var(--nav-height) + 2rem);
		background: url('/stardust.png'), rgba(0, 12, 34, 0.5);
		overflow: hidden;
	}

	.content-wrapper {
		height: 75vh;
		position: relative;
		margin-left: calc(var(--sidebar-width) + var(--page-padding-side));
		margin-right: var(--page-padding-side);
	}

	.content {
		height: 100%;
		overflow-y: auto;
		scrollbar-width: none;
		padding: 2rem;

		border-radius: 10px;
		border: 1px solid rgba(255, 255, 255, 0.05);
		background-color: rgba(0, 0, 0, 0.2);
		box-shadow: 0 0 30px rgba(0, 0, 0, 0.7);
		backdrop-filter: blur(5px);
		-webkit-backdrop-filter: blur(5px);
	}

	.fade-bottom {
		content: '';
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		height: 80px;
		pointer-events: none;
		margin: 0px 1rem 1px;

		background: linear-gradient(
			to bottom,
			rgba(7, 14, 26, 0) 0%,
			rgba(7, 14, 26, 0.5) 50%,
			rgba(7, 14, 26, 1) 95%
		);
	}
</style>
