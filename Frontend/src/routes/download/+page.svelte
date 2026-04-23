<!-- FIXME Raw data info box conflicts with the other info box while the other way is not a problem? How? -->
<script lang="ts">
	import HoverInfo from './HoverInfo.svelte';

	let { children } = $props();
	let currentInfo = $state<'raw' | 'processed' | null>(null);
</script>

<div class="page">
	<h1>Download page</h1>

	<div class="box">
		<p>Here you can download the altimetry data.</p>

		<div class="button-wrapper">
			<a
				href="/download/raw"
				class="button"
				onmouseenter={() => (currentInfo = 'raw')}
				onmouseleave={() => (currentInfo = null)}
				aria-disabled={currentInfo === 'processed'}
			>
				Download Raw Data
			</a>

			<a
				href="/download/processed"
				class="button"
				onmouseenter={() => (currentInfo = 'processed')}
				onmouseleave={() => (currentInfo = null)}
				aria-disabled={currentInfo === 'raw'}
			>
				Download Processed Data
			</a>
		</div>
	</div>

	<HoverInfo {currentInfo} />

	{@render children?.()}
</div>

<style>
	.page {
		height: 100vh;
		padding: 1rem;
		background: radial-gradient(circle at top, #1e293b, #020617);
	}

	.button-wrapper {
		width: auto;
		display: flex;
		justify-content: center;
		margin: 40px 10px 10px;
		gap: 15em;
	}

	.box {
		max-width: fit-content;
		margin: 2rem auto;
		padding: 2rem;
		border-radius: 10px;
		background-color: #1c1f26;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
	}

	.button {
		display: inline-block;
		padding: 0.75rem 1.5rem;
		background: linear-gradient(55deg, #238cbd, #2563eb);
		color: white;
		text-decoration: none;
		border-radius: 5px;
		font-weight: bold;
		cursor: pointer;
		text-align: center;
		transition: all 0.5s ease;
	}

	.button:hover {
		box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
	}

	.button[aria-disabled='true'] {
		opacity: 0.4;
		cursor: not-allowed;
		pointer-events: none;
	}

	h1 {
		text-align: center;
		color: white;
		margin-top: 1.5rem;
	}

	a {
		color: var(--primary);
		text-decoration: none;
		font-size: 1.25rem;
	}

	p {
		text-align: center;
		font-style: italic;
		color: white;
	}
</style>
