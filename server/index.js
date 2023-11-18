const canvas = document.getElementById('canvas')
const name = document.getElementById('name')
const clusterName = document.getElementById('cluster-name')
const desc = document.getElementById('desc')
let rainbow
const plotlyData = data => {
	rainbow = new Rainbow()
	rainbow.setNumberRange(0, Math.max(...data.cluster))
	rainbow.setSpectrum('blue', 'green', 'yellow', 'red')
	return [{
		type: 'scatter',
		x: data.x,
		y: data.y,
		hovertext: data.name,
		mode: 'markers',
		hoverinfo: 'text',
		marker: {
			color: data.cluster.map(c => rainbow.colourAt(c)),
			size: 10,
		},
	}]
}
const plotlyLayout = data => ({
	xaxis: {
	    showgrid: false,
	    zeroline: false,
	    visible: false,
	},
	yaxis: {
	    showgrid: false,
	    zeroline: false,
	    visible: false,
	},
	showscale: false,
	showlegend: false,
	modebar: {
		orientation: 'v',
		remove: [ "autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio", "hoverCompareCartesian", "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d", "pan3d", "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup", "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault", "resetcameralastsave", "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d", "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage", "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom", "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo", "zoomOutMapbox", "zoomin", "zoomout"]
	}
})

async function start() {
	const data = await (await fetch('/get_clusters')).json()
	let plot = Plotly.newPlot(canvas, plotlyData(data), plotlyLayout(data))
	let hoverId = -1
	let selectedCluster = -1
	function selectCluster() {
		const newData = plotlyData(data)
		newData[0].marker.color = newData[0].marker.color
			.map((c, i) => data.cluster[i] == selectedCluster ? c : '#ffffff00')
		newData[0].hovertext = newData[0].hovertext
			.map((h, i) => data.cluster[i] == selectedCluster ? h : '')
		Plotly.react(canvas, newData, plotlyLayout(data))
	}

	canvas.on('plotly_hover', e => {
		if(selectedCluster != -1 &&
			data.cluster[e.points[0].pointIndex] != selectedCluster) return;
		hoverId = e.points[0].pointIndex
		desc.innerText = data.description[hoverId]
		name.innerText = data.name[hoverId]
		clusterName.innerText = data.cluster[hoverId]
	}).on('plotly_unhover', e => {
		hoverId = -1
		desc.innerText = ''
		name.innerText = ''
		clusterName.innerText = ''
	}).on('plotly_click', _ => {
		if(hoverId != -1 && selectedCluster == -1) {
			selectedCluster = data.cluster[hoverId]
			selectCluster()
		} else if(selectedCluster != -1) {
			selectedCluster = -1
			console.log(data.cluster.length)
			plot = Plotly.react(canvas, plotlyData(data), plotlyLayout(data))
		}
	})
	document.onkeydown = ({ key }) => {
		if(key == 'c') {
			selectedCluster = parseInt(prompt('Введите номер кластера'))
			selectCluster()
		}
	} 
}

window.onload = start
