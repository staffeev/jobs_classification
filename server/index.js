canvas = document.getElementById('canvas');

async function start() {
	const data = await fetch('/get_clusters')
	const clusters = await data.json()

	console.log(clusters.cluster)
	Plotly.newPlot(
		canvas,
		[{
			type: "scatter",
			x: clusters.x,
			y: clusters.y,
			text: clusters.name,
			mode: 'markers',
			marker: {
				color: clusters.cluster,
				size: 10,
			}
		}]
	)
}

window.onload = start
