async function start() {
	const data = await fetch('/get_clusters')
	const clusters = await data.json()
	console.log(clusters)
}

window.onload = start
