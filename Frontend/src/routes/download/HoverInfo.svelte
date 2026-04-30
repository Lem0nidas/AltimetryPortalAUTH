<!-- TODO Update the Hover Info for each button. Add images -->
<script lang="ts">
	import { fade } from 'svelte/transition';

	let { currentInfo } = $props();

	// Δεδομένα παρατηρίσεων υψηλής ανάλυσης, όπου έχουν εφαρμοστεί οι γεωφυσικές διορθώσεις.
	const rawText = `
        High-resolution observation data, where geophysical corrections have been applied.
    `;

	const processedText = `
    Turn radar altimetry data to readable, shareable, and analyzable information.
    `;
</script>

<div class="info-box">
	{#if currentInfo === 'raw'}
		<div class="info-text-wrapper" transition:fade={{ duration: 250 }}>
			<h2>Raw altimetry Data</h2>
			<p>{rawText}</p>
		</div>
	{:else if currentInfo === 'processed'}
		<div class="info-text-wrapper" transition:fade={{ duration: 250 }}>
			<h2>Processed Alitimetry Data</h2>
			<p>{processedText}</p>
		</div>
	{/if}
</div>

<style>
	.info-box {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.info-text-wrapper {
		width: 50%;
		margin-top: 0.5rem;
		padding: 0.5rem 1rem;
		background-color: #1c1f26;
		border-radius: 4px;
		font-size: 0.9rem;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
	}

	h2 {
		text-align: center;
	}

	p {
		text-align: center;
		font-style: italic;
		color: white;
	}
</style>
