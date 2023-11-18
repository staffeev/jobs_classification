canvas = document.getElementById('canvas');

async function start() {
	const data = await fetch('/get_clusters')
	const clusters = await data.json()

	Plotly.newPlot(canvas,
		[{x: [1, 2, 3, 4, 5], y: [1, 2, 4, 8, 16]}],
		{margin: {t: 0}}
	)
}

window.onload = start
