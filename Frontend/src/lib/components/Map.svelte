<script lang="ts">
	import simplified_oceans from '$lib/data/simplified_oceans.geojson?raw';
	import { onMount, onDestroy } from 'svelte';
	import * as LeafletType from 'leaflet'; /* TODO: THIS BREAKS ON RELOAD / RESTART I KEEP IT FOR THE RECTANGLE TO UPDATE*/
	import type { LatLng, Rectangle as LeafletRectangle } from 'leaflet';
	import { RectangleEllipsis } from '@lucide/svelte';

	let L: typeof import('leaflet');
	let map: L.Map;
	let geojsonLayer: L.GeoJSON;
	let mapContainer: HTMLDivElement;
	let { selectedArea = $bindable() }: { selectedArea: string } = $props();
	let areaNames: string[] = $state([]);
	let parsedGeoJson = JSON.parse(simplified_oceans);
	let mode: 'Ocean' | 'Draw' = $state('Draw');

	const MIN_LAT = -90;
	const MAX_LAT = 90;
	const MIN_LNG = -180;
	const MAX_LNG = 180;

	let startPoint: LatLng | null;
	let rectangle: LeafletRectangle = $state(
		LeafletType.rectangle([
			[0, 0],
			[0, 0]
		])
	);
	let bounds: [L.LatLngTuple, L.LatLngTuple];
	let swLat = $state(0);
	let swLng = $state(0);
	let neLat = $state(0);
	let neLng = $state(0);
	let isSyncingFromMap = false;

	let isMoving = false;
	let moveOffset: L.LatLng | null = null;

	let checked: boolean = $state(false);
	$effect(() => {
		setMode(checked ? 'Ocean' : 'Draw');

		if (!rectangle || isSyncingFromMap) return;
		const inputBounds: [L.LatLngTuple, L.LatLngTuple] = [
			[swLat, swLng],
			[neLat, neLng]
		];

		rectangle.setBounds(inputBounds);
	});

	function enableDrawMode() {
		map.dragging.disable();
		map.getContainer().style.cursor = 'crosshair';
		map.on('mousedown', onMouseDown);
	}

	function disableDrawMode() {
		map.dragging.enable();
		map.getContainer().style.cursor = '';
		rectangle?.remove();
		map.off('mousedown', onMouseDown);
		map.off('mousemove', onMouseMove);
		map.off('mousemove', onRectangleMove);
	}

	function enableOceanMode() {
		addOceansLayer();
	}

	function disableOceanMode() {
		geojsonLayer?.remove();
	}

	function setMode(newMode: 'Ocean' | 'Draw') {
		if (mode === newMode) return;

		if (mode === 'Draw') {
			disableDrawMode();
			resetRectangle();
		}

		if (mode === 'Ocean') {
			disableOceanMode();
			resetOceanSelection();
		}
		mode = newMode;

		if (mode === 'Draw') enableDrawMode();
		if (mode === 'Ocean') enableOceanMode();
	}

	function addOceansLayer() {
		geojsonLayer = L.geoJSON(parsedGeoJson, {
			style: {
				color: 'gray',
				weight: 1,
				fillOpacity: 0.3
			},
			onEachFeature: (feature, layer) => {
				const name = feature.properties?.name || 'Unknown';
				if (!areaNames.includes(name)) {
					areaNames = [...areaNames, name];
				}

				layer.on('click', () => {
					selectedArea = name;
					highlightOcean(name);
				});
			}
		});
		geojsonLayer.addTo(map);
	}

	function highlightOcean(name: string) {
		geojsonLayer.eachLayer((layer: any) => {
			if (layer.feature?.properties?.name === name) {
				map.fitBounds(layer.getBounds());
				layer.setStyle({
					color: 'blue',
					weight: 2,
					fillOpacity: 0.5
				});
			} else {
				geojsonLayer.resetStyle(layer);
			}
		});
	}

	function resetRectangle() {
		rectangle?.remove();
		swLat = 0;
		swLng = 0;
		neLat = 0;
		neLng = 0;
	}

	function resetOceanSelection() {
		selectedArea = '';
	}

	function onMouseDown(e: L.LeafletMouseEvent) {
		startPoint = e.latlng;
		if (e.originalEvent.ctrlKey || e.originalEvent.button === 1) {
			map.dragging.enable();
			return;
		}

		map.dragging.disable();

		if (rectangle && rectangle.getBounds().contains(e.latlng)) {
			isMoving = true;

			const bounds = rectangle.getBounds();
			moveOffset = L.latLng(
				e.latlng.lat - bounds.getSouthWest().lat,
				e.latlng.lng - bounds.getSouthWest().lng
			);

			map.on('mousemove', onRectangleMove);
			map.once('mouseup', onEndMove);
			return;
		} else {
			rectangle?.remove();

			const initialBounds: [L.LatLngTuple, L.LatLngTuple] = [
				[startPoint.lat, startPoint.lng],
				[startPoint.lat, startPoint.lng]
			];

			rectangle = L.rectangle(initialBounds, {
				color: '#ff0008',
				weight: 1
			}).addTo(map);

			map.on('mousemove', onMouseMove);
			map.once('mouseup', onMouseUp);
		}
	}

	function onMouseMove(e: L.LeafletMouseEvent) {
		if (!startPoint || !rectangle) return;

		bounds = [
			[startPoint.lat, startPoint.lng],
			[e.latlng.lat, e.latlng.lng]
		];

		if (rectangle) rectangle.setBounds(bounds);
		syncBoundsFromRectangle();
	}

	function onMouseUp() {
		map.off('mousemove', onMouseMove);
		if (rectangle) {
			selectedArea = getBoundsString(rectangle);
		}
		startPoint = null;
		syncBoundsFromRectangle();
	}

	function onRectangleMove(e: L.LeafletMouseEvent) {
		if (!rectangle || !isMoving || !moveOffset) return;

		const bounds = rectangle.getBounds();
		const sw = bounds.getSouthWest();
		const ne = bounds.getNorthEast();

		let latDiff = e.latlng.lat - sw.lat - moveOffset.lat;
		let lngDiff = e.latlng.lng - sw.lng - moveOffset.lng;

		const newSwLat = sw.lat + latDiff;
		const newSwLng = sw.lng + lngDiff;
		const newNeLat = ne.lat + latDiff;
		const newNeLng = ne.lng + lngDiff;

		if (newSwLat < MIN_LAT) {
			latDiff += MIN_LAT - newSwLat;
		}
		if (newNeLat > MAX_LAT) {
			latDiff -= newNeLat - MAX_LAT;
		}

		if (newSwLng < MIN_LNG) {
			lngDiff += MIN_LNG - newSwLng;
		}
		if (newNeLng > MAX_LNG) {
			lngDiff -= newNeLng - MAX_LNG;
		}

		const finalSw = L.latLng(sw.lat + latDiff, sw.lng + lngDiff);
		const finalNe = L.latLng(ne.lat + latDiff, ne.lng + lngDiff);
		rectangle.setBounds(L.latLngBounds(finalSw, finalNe));
	}

	function onEndMove() {
		isMoving = false;
		moveOffset = null;
		map.off('mousemove', onRectangleMove);
		map.dragging.enable();

		if (rectangle) {
			selectedArea = getBoundsString(rectangle);
		}
		syncBoundsFromRectangle();
	}

	function getBoundsString(rectangle: L.Rectangle<any>) {
		const bounds = rectangle.getBounds();
		const sw = bounds.getSouthWest();
		const ne = bounds.getNorthEast();

		return [sw.lng.toFixed(2), ne.lng.toFixed(2), sw.lat.toFixed(2), ne.lat.toFixed(2)].join(',');
	}

	onMount(async () => {
		L = await import('leaflet');

		map = L.map(mapContainer, {
			maxBounds: [
				[-85, -180],
				[85, 180]
			],
			maxBoundsViscosity: 0.9,
			zoomControl: false
		}).setView([10, 0], 2);
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			noWrap: true,
			maxZoom: 5,
			minZoom: 2
		}).addTo(map);

		enableDrawMode();
		setMode(mode);
	});

	onDestroy(() => {
		map?.remove();
	});

	function syncBoundsFromRectangle() {
		if (!rectangle) return;
		isSyncingFromMap = true;

		const b = rectangle.getBounds();
		swLat = +b.getSouthWest().lat.toFixed(2);
		swLng = +b.getSouthWest().lng.toFixed(2);
		neLat = +b.getNorthEast().lat.toFixed(2);
		neLng = +b.getNorthEast().lng.toFixed(2);

		isSyncingFromMap = false;
	}

	function format(n: number, digits: number = 2, min: number = -90, max: number = 90) {
		const formated: number = Math.max(min, Math.min(max, n));
		return +formated.toFixed(digits);
	}
</script>

<div class="map-input-container">
	<div class="map-type-container glass-panel">
		<fieldset id="map-type">
			<label for="map-type-switch">
				Draw
				<input id="map-type-switch" type="checkbox" role="switch" bind:checked />
				Ocean
			</label>
		</fieldset>

		<label for="area-select">Select an area: </label>
		<select
			id="area-select"
			bind:value={selectedArea}
			onchange={() => highlightOcean(selectedArea)}
			disabled={mode === 'Draw'}
		>
			<option disabled value="">-- Choose --</option>
			{#each [...new Set(areaNames)] as name}
				<option value={name}>{name}</option>
			{/each}
		</select>
	</div>

	<div class="rectangle-bounds glass-panel">
		<h3>Draw Area</h3>

		<div class="coord-row">
			<label>
				SW Latitude:
				<input
					type="text"
					bind:value={swLat}
					step="1"
					min="-90"
					max="90"
					onblur={() => {
						swLat = format(swLat);
					}}
					disabled={mode === 'Ocean'}
				/>
			</label>

			<label>
				SW Longitude:
				<input
					type="text"
					bind:value={swLng}
					step="1"
					min="-180"
					max="180"
					onblur={() => {
						swLng = format(swLng, 2, -180, 180);
					}}
					disabled={mode === 'Ocean'}
				/>
			</label>
		</div>

		<div class="coord-row">
			<label>
				NE Latitude:
				<input
					type="text"
					bind:value={neLat}
					step="1"
					min="-90"
					max="90"
					onblur={() => {
						neLat = format(neLat);
					}}
					disabled={mode === 'Ocean'}
				/>
			</label>

			<label>
				NE Longitude:
				<input
					type="text"
					bind:value={neLng}
					step="1"
					min="-180"
					max="180"
					onblur={() => {
						neLng = format(neLng, 2, -180, 180);
					}}
					disabled={mode === 'Ocean'}
				/>
			</label>
		</div>
	</div>

	<div class="map-container" bind:this={mapContainer} id="map">
		<p class="mode">Mode: {mode}</p>
	</div>
</div>

<style>
	#map {
		height: 550px;
		width: 90%;
		margin: 1rem auto 2rem;
		border: 1px solid #2a3140;
		border-radius: 20px;
		box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.2);
		position: relative;
	}

	div.map-input-container {
		display: grid;
		place-items: center;
		grid-template-columns: 1fr 2fr;
	}

	div.map-input-container > :nth-child(1) {
		grid-column: 1;
		grid-row: 2;
	}

	div.map-input-container > :nth-child(2) {
		grid-column: 1;
		grid-row: 1;
	}

	div.map-input-container > :nth-child(3) {
		grid-column: 2;
		grid-row: 1 / span 2;
	}

	div.map-container {
		position: relative;
		width: 90%;
		margin: auto;
		z-index: 0;
	}

	div.map-type-container {
		width: 70%;
	}

	div.rectangle-bounds {
		width: 70%;
	}

	div.coord-row {
		display: flex;
	}

	div.coord-row label {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	div.glass-panel {
		padding: 0.5rem;
		border-radius: 10px;
		border: 1px solid rgba(255, 255, 255, 0.05);
		background: rgba(0, 0, 0, 0.2);
		box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(5px);
		-webkit-backdrop-filter: blur(5px);
	}

	select#area-select {
		width: 90%;
		padding: 0.75rem 1rem;
		border-radius: 8px;
		border: 1px solid #2a3140;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
		background-color: rgb(26, 39, 56, 0.5);
		backdrop-filter: blur(1px);
		color: white;
	}

	input {
		width: 90%;
		border-radius: 8px;
		border: 1px solid #2a3140;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
		background-color: rgb(26, 39, 56, 0.5);
		backdrop-filter: blur(1px);
		color: white;
	}

	p.mode {
		position: absolute;
		top: 10px;
		left: 10px;
		z-index: 1000;
		padding: 6px 10px;
		background-color: rgba(0, 0, 0, 0.7);
		border-radius: 6px;
		pointer-events: none;
	}
</style>
