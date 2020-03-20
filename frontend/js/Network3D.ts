//mock dataset
//the library we use for the points visualization
import ForceGraph3D from './network3D/3d-force-graph.js';
import ServerAPI from './ServerAPI';


export default class Network3D
{
	constructor(eventHandler)
	{
		this.eventHandler = eventHandler;
		this.eventHandler.subscribe_network(this)
		this.Graph = ForceGraph3D()(document.getElementById("network"));
		//Graph.resetProps();

		this.nodes = {};

		function lerpColor(a, b, amount) { 
			//amount = Math.round(amount * 10) / 10
			amount = ( amount - 0.5 ) * 2
		    var ah = parseInt(a.replace(/#/g, ''), 16),
		        ar = ah >> 16, ag = ah >> 8 & 0xff, ab = ah & 0xff,
		        bh = parseInt(b.replace(/#/g, ''), 16),
		        br = bh >> 16, bg = bh >> 8 & 0xff, bb = bh & 0xff,
		        rr = ar + amount * (br - ar),
		        rg = ag + amount * (bg - ag),
		        rb = ab + amount * (bb - ab);

		    return '#' + ((1 << 24) + (rr << 16) + (rg << 8) + rb | 0).toString(16).slice(1);
		}


		this.Graph
			.cooldownTicks(200)
			.nodeLabel('subredditName')
			.nodeId('subredditName')

			.nodeAutoColorBy('subscriberCount')
			.nodeVal('subscriberCount')

			.linkTarget('toSubredditName')
			.linkSource('fromSubredditName')

			.nodeRelSize(0.125)
			.cooldownTime(5000000)
			.forceEngine('ngraph')
			//.linkCurvature(0.1)
			.linkMaterial("MeshBasicMaterial")
			.backgroundColor("#333333")
			.linkWidth((link)=>{return link.volume / 20 + 1;})
			.linkColor((link)=>{return lerpColor( "#ff4444" , "#44ff44", link.sentiment)})
			.onNodeHover(
				(node)=>{

					let position = {
						x : document.getElementsByClassName("scene-tooltip")[0].style.left,
						y : document.getElementsByClassName("scene-tooltip")[0].style.top
					}

					if(node){
						//d3.json("http://127.0.0.1:5000/radar?=" + node.id, console.log);
						//console.log(node.id)
						this.on_hover(node.subredditName, position)
					} else {
						this.on_hover_ends()
					}
			})
			.nodeLabel(
				(node)=>{
					console.log(node)

					return node.subredditName
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
		//this.Graph.resetProps();
		this.nodes = {};
		console.log(data)
		data.nodes.map((node)=>{return this.nodes[node.subredditName] = true});
		this.Graph.graphData(data);
		this.Graph.linkVisibility((link)=>{
			return this.nodes[link.toSubredditName]// && nodes[link.fromSubredditName]
		})

		let nodes_vis = {};
		data.links.map((link)=>{
			nodes_vis[link.toSubredditName] = true
			nodes_vis[link.fromSubredditName] = true
			return;
		});

		this.all_nodes = {};
		this.Graph.nodeVisibility((node)=>{
			//return node.
			//console.log(node)
			this.all_nodes[node.subredditName] = node;

			return nodes_vis[node.subredditName]
			//return true;
		})
	}

	search_node(node_name) {
		console.log();

		let node = this.all_nodes[node_name];
		if(!node) return;

		let position = node.__threeObj.position.addScalar(350);

        this.Graph.cameraPosition(
            { x: position.x , y: position.y , z: position.z  }, // new position
            node.__threeObj.position, // lookAt ({ x, y, z })
            2000  // ms transition duration
        );

        let nodes_to_see = {};

        this.Graph.linkVisibility((link)=>{

        	let visible = undefined != this.nodes[link.toSubredditName] && (link.toSubredditName == node_name || link.fromSubredditName == node_name)// && nodes[link.fromSubredditName]
			if (visible) {
				nodes_to_see[link.toSubredditName] = true;
				nodes_to_see[link.fromSubredditName] = true;
			}
			return visible;
		})

        setTimeout(()=>{
        	this.Graph.nodeVisibility((node)=>{
        		return nodes_to_see[node.subredditName]
        	})
    	}, 100)
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

    update_dates(date0, date1) {
    	let ctx = this;
		(ServerAPI.get()).getDataBetweenDates(date0, date1, function(data2) {
    	    ctx.update_network(data2)
    	});
    }
}
