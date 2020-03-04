import data from './network/reddit.json'
import ForceGraph3D from './network/assets/3d-force-graph.js';


export default class Network3D
{
  	constructor()
  	{

		const Graph = ForceGraph3D()
		(document.getElementById("network"));
		Graph.resetProps();


		Graph
			.cooldownTicks(200)
			.nodeLabel('id')
			.nodeAutoColorBy('subscriberCount')
			.nodeVal('subscriberCount')
			.nodeRelSize(0.125)
			.cooldownTime(5000000)
			.backgroundColor("#333333")
			.linkWidth((link)=>{return link.value / 10;})
			//.linkColor((link)=>{return link.sentiment > 0.5 ? "#33ff55" : "#ff3355"})
			.linkColor((link)=>{return Math.random() > 0.5 ? "#33ff55" : "#ff3355"})
			.forceEngine('ngraph')
			.d3VelocityDecay(1)
			.onNodeHover(
				(node)=>{if(node) {d3.json("http://127.0.0.1:5000/radar?=" + node.id, console.log);console.log(node.id)}
			})
			.nodeLabel(
				(node)=>{if(node) {d3.json("http://127.0.0.1:5000/radar?=" + node.id, console.log); return node.id + " : " + node.subscriberCount}
			})
			.width(document.getElementById("network").offsetWidth)
			.height(document.getElementById("network").offsetHeight)
			.graphData(data);
  	}
}
