//mock dataset
import data from './network3D/reddit.json'
//the library we use for the points visualization
import ForceGraph3D from './network3D/3d-force-graph.js';


export default class Network3D
{
	constructor(eventHandler)
	{
		this.eventHandler = eventHandler;
		this.eventHandler.subscribe_network(this)
		console.log(data)
		this.Graph = ForceGraph3D()(document.getElementById("network"));
		//Graph.resetProps();
		let nodes = {};
		data.nodes.map((node)=>{return nodes[node.id] = true});
		this.Graph
			.cooldownTicks(200)
			.nodeLabel('subredditName')
			.nodeId('subredditName')

			.nodeAutoColorBy('subscriberCount')
			.nodeVal('subscriberCount')

			.linkTarget('toSubredditName')
			.linkSource('fromSubredditName')


			.nodeRelSize(0.125)
			//.cooldownTime(5000000)
			.forceEngine('ngraph')
			.linkVisibility((link)=>{
				return  nodes[link.toSubredditName]
			})
			.backgroundColor("#333333")
			.linkWidth((link)=>{return link.volume / 20;})
			.linkColor((link)=>{return link.sentiment > 0.9 ? "#33ff55" : "#ff3355"})
			//.linkColor((link)=>{return Math.random() > 0.5 ? "#33ff55" : "#ff3355"})
			.onNodeHover(
				(node)=>{

					let position = {
						x : document.getElementsByClassName("scene-tooltip")[0].style.left,
						y : document.getElementsByClassName("scene-tooltip")[0].style.top
					}

					if(node){
						//d3.json("http://127.0.0.1:5000/radar?=" + node.id, console.log);
						//console.log(node.id)
						console.log(position)
						this.on_hover(node.id, position)
					} else {
						this.on_hover_ends()
					}
			})
			.nodeLabel(
				(node)=>{
					console.log(node)

					return node.id
					//if(node){
						//d3.json("http://127.0.0.1:5000/radar?=" + node.id, console.log);
						//return node.id + " : " + node.subscriberCount
					//}
			})
			.width(document.getElementById("network").offsetWidth)
			.height(document.getElementById("network").offsetHeight)
			//.graphData(data);
	}

	update_network(data) {
		this.Graph.graphData(data);
	}


	on_hover(node, position){
		this.eventHandler.on_network_over(node, position)
	}

	on_hover_ends(){
		this.eventHandler.on_network_over_ends()
	}

	on_resize(){

		this.Graph.width(document.getElementById("network").offsetWidth)
		this.Graph.height(document.getElementById("network").offsetHeight)
	}
}
