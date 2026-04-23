<script lang="ts">
	import { requestCustomDownload, requestDateDownload } from '$lib';
	import Switch from '$lib/components/Switch.svelte';
	import type { RADSSatellite } from '$lib/data/satellites';
	import { satellites } from '$lib/data/satellites';

	let selectedSatellite: RADSSatellite = $state({ name: '', code: '', start: '', end: '' });
	let selectedCycle = $state('');
	let selectedPass = $state('');
	let currentDate = new Date().toISOString().split('T')[0];
	let selectedStartDate = $state('');
	let selectedEndDate = $state('');

	let toggles = $state({
		pass: false,
		dateSwitch: true,
		startDate: false,
		test: true
	});

	let messages = $state({
		response: '',
		error: '',
		download: '',
		custom: '',
		date: ''
	});

	$effect(() => {
		if (selectedSatellite.name != '') {
			toggles.dateSwitch = false;
			selectedStartDate = selectedSatellite.start;
			selectedEndDate = selectedSatellite.end == 'present' ? currentDate : selectedSatellite.end;
		}

		if (selectedSatellite.name && selectedCycle) {
			toggles.test = false;
		} else if (selectedSatellite.name && toggles.startDate) {
			toggles.test = false;
		} else {
			toggles.test = true;
		}

		if (!toggles.pass) {
			selectedPass = '';
		}

		if (toggles.startDate) {
			selectedCycle = '';
			selectedPass = '';
		}
	});

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		if (!selectedSatellite) {
			messages.response = 'Please select a satellite.';
			return;
		}

		try {
			if (!toggles.startDate && selectedCycle) {
				messages.response = await requestCustomDownload(
					selectedSatellite.code,
					selectedCycle,
					selectedPass
				);
			}

			if (toggles.startDate && selectedStartDate) {
				messages.date = await requestDateDownload(
					selectedSatellite.code,
					selectedStartDate,
					selectedEndDate
				);
			}
		} catch (err) {
			messages.error = 'Error contacting server.';
			console.error(err);
		}
	}
</script>

<div class="page">
	<h1>Download Raw Data page</h1>

	<form onsubmit={handleSubmit}>
		<fieldset>
			<label for="satellite">Choose a satellite:</label>
			<select id="satellite" bind:value={selectedSatellite} required>
				<option value="" disabled selected>Select one</option>
				{#each satellites as sat}
					<option value={sat}>{sat.name}</option>
				{/each}
			</select>
		</fieldset>

		<fieldset disabled={toggles.startDate}>
			<label for="cycle">Type the cycle number:</label>
			<input
				type="text"
				id="cycle"
				placeholder="e.g. 015"
				maxlength="3"
				bind:value={selectedCycle}
				onblur={() => {
					if (selectedCycle?.trim()) {
						selectedCycle = selectedCycle.padStart(3, '0');
					}
				}}
			/>
		</fieldset>

		<Switch bind:selectedProperty={selectedPass} type="Pass" disable={toggles.startDate} />

		<fieldset disabled={toggles.dateSwitch}>
			<label for="start-date-switch">
				<input
					type="checkbox"
					name="start-date-switch"
					role="switch"
					bind:checked={toggles.startDate}
				/>
				Date Based Download
			</label>
			{#if toggles.startDate}
				<label for="start-date">Pick Date:</label>
				<div class="date-container">
					<input
						type="date"
						name="start-date"
						min={selectedSatellite.start}
						max={selectedSatellite.end}
						bind:value={selectedStartDate}
					/>
					<input
						type="date"
						name="end-date"
						min={selectedSatellite.start}
						max={selectedSatellite.end}
						bind:value={selectedEndDate}
					/>
				</div>
			{/if}
		</fieldset>

		<button type="submit" disabled={toggles.test}>Submit</button>
	</form>

	{#each Object.entries(messages) as [key, value]}
		{#if value}
			<hr />
			<p>{value}</p>
		{/if}
	{/each}
</div>

<style>
	.page {
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
		border: 1px solid rgba(255, 255, 255, 0.055);
		background: rgba(0, 0, 0, 0.2);
		box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(5px);
	}
	/* Version 2
	form {
		background: rgba(20, 25, 40, 0.85);
		backdrop-filter: blur(12px);
		border-radius: 16px;
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
		padding: 2rem;
	} */

	h1 {
		text-align: center;
		margin: 0;
		color: white;
	}

	fieldset {
		border: none;
		margin-bottom: 1.5rem;
	}

	label {
		display: block;
		margin-bottom: 0.5rem;
		color: #9ca3af;
		font-weight: 500;
		/* font-size: 0.85rem; */
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

	.date-container {
		display: flex;
		gap: 10%;
		justify-content: center;
	}

	input[type='date'] {
		width: 40%;
	}

	input[type='checkbox'] {
		margin-right: 0.5rem;
		width: 40px;
		height: 22px;
	}

	input:focus,
	select:focus {
		outline: none;
		border: 1px solid #3b82f6;
		box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
	}

	button {
		background: linear-gradient(135deg, #0ea5e9, #2563eb);
		border-radius: 10px;
		border: none;
		padding: 0.8rem;
		font-weight: 600;
		transition: 0.5s;
		width: 60%;
	}

	button:hover {
		box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
	}

	p {
		text-align: center;
		color: #ddd;
	}
</style>
