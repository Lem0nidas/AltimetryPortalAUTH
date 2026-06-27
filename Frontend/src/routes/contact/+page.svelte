<script>
	const projectTitle =
		'Creation of a Web interface for the automatic archiving, processing and presentation of altimetry data';

	const author = {
		name: 'Kaladze Leon',
		email: 'leonkala@topo.auth.gr'
	};

	const institution = {
		name: 'Aristotle University of Thessaloniki',
		school: 'School of Rural and Surveying Engineering',
		department: 'Department of Geodesy and Surveying',
		email: 'info@topo.auth.gr',
		address: '54124 Thessaloniki, Greece'
	};
</script>

<svelte:head>
	<title>Contact</title>
</svelte:head>

<div class="page">
	<div class="container">
		<h1>Contact</h1>

		<p class="intro">
			This web application was developed as part of the thesis
			<strong>{projectTitle}</strong>. If you have any questions, suggestions, or would like to
			report an issue, please feel free to get in touch.
		</p>

		<section class="card">
			<h2>Author</h2>

			<p>
				<strong>Name:</strong><br />
				{author.name}
			</p>

			<p>
				<strong>Email:</strong><br />
				<a href="mailto:{author.email}">
					{author.email}
				</a>
			</p>
		</section>

		<section class="card">
			<h2>Institution</h2>

			<p>
				<strong>{institution.name}</strong><br />
				{institution.school}<br />
				{institution.department}
			</p>

			<p>
				<strong>Email:</strong><br />
				<a href="mailto:{institution.email}">
					{institution.email}
				</a>
			</p>

			<p>
				<strong>Address:</strong><br />
				{institution.address}
			</p>
		</section>

		<section class="card">
			<h2>Project Information</h2>

			<p>
				<strong>Thesis Title:</strong><br />
				Creation of a Web interface for the automatic archiving, processing and presentation of altimetry
				data
			</p>

			<p>
				<strong>Supervisor:</strong><br />
				Dr. Georgios S. Vergos
			</p>

			<p>
				<strong>Academic Year:</strong><br />
				2025–2026
			</p>

			<p>
				<strong>GitHub Repository:</strong><br />
				<a
					href="https://github.com/Lem0nidas/AltimetryPortalAUTH.git"
					target="_blank"
					rel="noopener noreferrer"
				>
					github.com/Lem0nidas/AltimetryPortalAUTH.git
				</a>
			</p>

			<p>
				<strong>Version:</strong><br />
				Version 1.0 • June 2026
			</p>
		</section>

		<section class="note">
			<p>
				This application was developed for academic and research purposes. The information presented
				is based on publicly available satellite altimetry datasets and accompanying documentation.
			</p>
		</section>
	</div>
</div>

<style>
	.page {
		padding: 1rem;
		padding-top: calc(var(--nav-height) + 1rem);
		background: url('/stardust.png'), rgba(0, 12, 34, 0.5);
		background-position: 15% 50%;
	}

	.container {
		max-width: 850px;
		margin: 0 auto;
		padding: 2rem;
	}

	h1 {
		margin-bottom: 1rem;
	}

	.intro {
		line-height: 1.7;
		margin-bottom: 2rem;
	}

	.card {
		margin-bottom: 2rem;
		padding: 1.5rem;
		border: 1px solid #ddd;
		border-radius: 10px;
	}

	h2 {
		margin-top: 0;
	}

	a {
		color: #0b66c3;
		text-decoration: none;
	}

	a:hover {
		text-decoration: underline;
	}

	.note {
		margin-top: 2rem;
		font-size: 0.95rem;
		color: #666;
		border-top: 1px solid #ddd;
		padding-top: 1rem;
	}
</style>
