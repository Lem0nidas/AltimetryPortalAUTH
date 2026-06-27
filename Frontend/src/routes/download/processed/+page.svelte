<script lang="ts">
	import { X } from '@lucide/svelte';
	import type { RADSVariable } from '$lib/data/variables';
	import type { RADSSatellite } from '$lib/data/satellites';
	import { variables } from '$lib/data/variables';
	import { satellites } from '$lib/data/satellites';
	import { processedDownload } from '$lib';
	import Map from '$lib/components/Map.svelte';
	import { requestCycles } from '$lib/api/cycles';

	let { children } = $props();

	let selectedSatellite: RADSSatellite = $state({ name: '', code: '', start: '', end: '' });
	let selectedVariable: RADSVariable = $state({ name: '', varName: '', description: '' });
	let listBoxItems: RADSVariable[] = $state([]);
	let selectedRegion: string = $state('');
	let fileType: boolean = $state(false);
	let options: Record<string, string | string[]> = $derived.by(() => {
		let opts: Record<string, string | string[]> = {
			cycle: Array.from(selectedCycles).sort(),
			vars: listBoxItems.map((v) => v.varName).join(','),
			region: selectedRegion
		};
		return opts;
	});

	let messages = $state({
		response: '',
		error: '',
		download: '',
		custom: '',
		date: ''
	});

	let toggles = $state({
		disableButton: true
	});

	let allCycles: any[] = $state([]);
	$effect(() => {
		if (selectedSatellite.code) {
			(async () => {
				allCycles = await requestCycles(selectedSatellite.code);
			})();
		}

		if (selectedSatellite.name && listBoxItems.length > 0) {
			toggles.disableButton = false;
		} else {
			toggles.disableButton = true;
		}
	});

	function addToList() {
		if (!listBoxItems.some((item) => item.name === selectedVariable.name)) {
			listBoxItems = [...listBoxItems, selectedVariable];
		}
	}

	function removeFromList(index: number) {
		listBoxItems = listBoxItems.filter((_, i) => i !== index);
	}

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		if (!selectedSatellite || listBoxItems.length === 0 || selectedCycles.size === 0) {
			messages.response = 'Please provide satellite, variable and cycles';
			return;
		}

		try {
			messages.response = await processedDownload(selectedSatellite.code, options, fileType);
		} catch (err) {
			messages.error = 'Error contacting server.';
			console.log(err);
		}
	}

	let selectedCycles: Set<string> = $state(new Set());
	let lastClickedIndex: number | null = null;

	function handleClickCheckbox(
		index: number,
		item: { cycle: string; start: string; end: string },
		event: MouseEvent
	) {
		if (event.shiftKey && lastClickedIndex !== null) {
			const [start, end] = [lastClickedIndex, index].sort((a, b) => a - b);

			for (let i = start; i <= end; i++) {
				selectedCycles.add(allCycles[i].cycle);
			}
		} else {
			if (selectedCycles.has(item.cycle)) {
				selectedCycles.delete(item.cycle);
			} else {
				selectedCycles.add(item.cycle);
			}
			lastClickedIndex = index;
		}

		selectedCycles = new Set(selectedCycles);
	}

	let allSelected: boolean = $derived(selectedCycles.size == allCycles.length);
	function toggleAll() {
		if (allSelected) {
			selectedCycles = new Set(allCycles.map((item) => item.cycle));
		} else {
			selectedCycles = new Set();
		}
	}

	let inputValue = $state('');
	let formatedInputValue = $derived(inputValue.padStart(3, '0'));
	const checkboxMap: Record<string, HTMLInputElement> = $state({});

	$effect(() => {
		const checkboxElement = checkboxMap[formatedInputValue];

		if (checkboxElement) {
			checkboxElement.scrollIntoView({
				behavior: 'instant',
				block: 'center'
			});
		}
	});
</script>

<div class="page">
	<h1>Download Processed Data page</h1>

	<form onsubmit={handleSubmit}>
		<fieldset>
			<label for="satellite">Choose a satellite</label>
			<select id="satellite" bind:value={selectedSatellite} required>
				<option value="" disabled selected>Select one</option>
				{#each satellites as sat}
					<option value={sat}>{sat.name}</option>
				{/each}
			</select>
		</fieldset>

		<fieldset disabled={!selectedSatellite.code}>
			<div class="cycle-search-wrapper">
				<div class="cycle-search">
					<label for="cycle-number"> Cycle number </label>
					<input
						type="text"
						id="cycle-number"
						placeholder="Search for a cycle number"
						maxlength={3}
						bind:value={inputValue}
					/>
				</div>
				<div class="select-all">
					<label for="select-all">
						<input
							type="checkbox"
							name="select-all"
							id="select-all"
							bind:checked={allSelected}
							onchange={toggleAll}
						/>
						Select all the cycles
					</label>
				</div>
			</div>

			<div class="cycle-listbox-wrapper">
				<ul id="cycle-listbox">
					{#each allCycles as item, index}
						<li>
							<label>
								<input
									type="checkbox"
									id={String(index)}
									checked={selectedCycles.has(item.cycle)}
									bind:this={checkboxMap[item.cycle]}
									onclick={(e) => handleClickCheckbox(index, item, e)}
								/>
								Cycle {item.cycle} | From {item.start} - Until {item.end}
							</label>
						</li>
					{/each}
				</ul>
			</div>
		</fieldset>

		<fieldset>
			<label for="var-listbox">Selected Variables:</label>
			<div class="var-listbox-wrapper">
				<ul id="var-listbox">
					{#each listBoxItems as items, index}
						<li>
							<span>{items.name}</span>
							<button
								type="button"
								id="removeButton"
								onclick={() => removeFromList(index)}
								aria-label="Remove item"
							>
								<X size={16} />
							</button>
						</li>
					{/each}
				</ul>
			</div>

			<label for="variables">Pick variables</label>
			<select
				name="variables"
				id="variables"
				bind:value={selectedVariable}
				onchange={addToList}
				required
			>
				<option value={null} disabled selected>Select any amount</option>
				{#each variables as variable (variable.varName)}
					<option value={variable}>{variable.name}</option>
				{/each}
			</select>
		</fieldset>

		<fieldset id="button">
			<button type="submit" disabled={toggles.disableButton}>Submit</button>
			<label for="file-type-switch">
				ASCII File
				<input id="file-type-switch" type="checkbox" role="switch" bind:checked={fileType} />
				NetCDF File
			</label>
		</fieldset>
	</form>

	<Map bind:selectedArea={selectedRegion} />
	{@render children?.()}
</div>

<style>
	div.page {
		padding-top: calc(var(--nav-height) + 1rem);
		padding-bottom: var(--page-padding-bottom);
		background: url('/stardust.png'), rgba(0, 12, 34, 0.5);
		background-position: 50% 15%;
	}

	form {
		max-width: 600px;
		margin: 2rem auto;
		padding: 2rem;
		border-radius: 10px;
		border: 1px solid rgba(255, 255, 255, 0.05);
		background: rgba(0, 0, 0, 0.2);
		box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(5px);
		-webkit-backdrop-filter: blur(5px);
	}

	h1 {
		text-align: center;
		margin-top: 1.5rem;
		color: white;
	}

	fieldset {
		border: none;
		margin-bottom: 1rem;
	}

	fieldset#button {
		display: grid;
		justify-content: center;
	}

	input[type='text'],
	select {
		width: 100%;
		padding: 0.75rem 1rem;
		border-radius: 8px;
		border: 1px solid #444;
		background-color: rgb(26, 39, 56, 0.5);
		color: white;
	}

	ul#cycle-listbox li {
		list-style: none;
		user-select: none;
	}

	ul#var-listbox {
		display: flex;
		flex-wrap: wrap;
		gap: 0.2em;
		max-height: 250px;
		overflow-y: auto;
		list-style: none;
		padding: 0;
		margin: 0.2rem;
	}

	ul#var-listbox li {
		display: flex;
		align-items: center;
		padding: 0.3rem 0.6rem;
		border: 1px solid #eee;
		border-radius: 25px;
		font-size: medium;
		width: fit-content;
	}

	ul#var-listbox li:hover {
		background-color: #ffffff0a;
		box-shadow: 0 0 5px rgba(0, 0, 0, 0.4);
		cursor: default;
	}

	button[type='submit'] {
		background: linear-gradient(250deg, #0ea5e9, #2563eb);
		border-radius: 10px;
		border: none;
		padding: 0.8rem;
		font-weight: 600;
		transition: 0.5s;
	}

	button[type='submit']:hover {
		box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
		transform: translateY(-1px);
	}

	button#removeButton {
		font-size: 1rem;
		line-height: 1;
		padding: 0;
		margin: auto 0.2rem;
		background: none;
		border: none;
		color: rgb(17, 17, 17);
		cursor: pointer;
		transition: transform 0.3s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	button#removeButton:hover {
		transform: rotate(90deg);
		color: red;
	}

	label[for='file-type-switch'] {
		margin: auto 50px;
	}

	input#file-type-switch {
		margin-left: 0.5rem;
		--pico-background-color: rgba(122, 162, 247, 0.5);
		--pico-border-color: rgba(204, 160, 204, 0.2);
		--pico-form-element-focus-color: none;
	}

	input#file-type-switch:checked {
		--pico-background-color: #508aa8;
	}

	input#cycle-number {
		width: auto;
	}

	.var-listbox-wrapper {
		height: 270px;
		margin-bottom: 1rem;
		border: 1px solid #2a3140;
		border-radius: 20px;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
		background-color: rgb(26, 39, 56, 0.5);
		color: white;
	}

	.cycle-listbox-wrapper {
		height: 200px;
		border: 1px solid #2a3140;
		border-radius: 20px;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
		background-color: rgb(26, 39, 56, 0.5);
		color: white;
		margin-bottom: 1rem;
		overflow-y: auto;
	}

	.cycle-search-wrapper {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 5%;
	}

	.select-all {
		padding-top: 20px;
	}
</style>
