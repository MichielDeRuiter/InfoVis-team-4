import Configuration from './Configuration'
import ServerAPI from './ServerAPI'
import BasicD3Visualization from './BasicD3Visualization'

export default class RadarplotIframe
{
	constructor(eventHandler)
	{
		this.eventHandler = eventHandler;
		this.eventHandler.subscribe_radarplot(this)
		

		this.ifrm = document.createElement('iframe');
		this.ifrm.setAttribute('id', 'radarplot-iframe');// assign an id
		this.ifrm.className = "iframe-radarplot";

		//document.body.appendChild(ifrm); // to place at end of document
		// to place before another page element
		this.container = document.getElementById('radarplot');
		this.container.appendChild(this.ifrm	);
		// assign url
		this.ifrm.setAttribute('src', '//localhost:5000/vis4');

		this.last_four = [];
	}

	on_node_select(node, position) {

		if (!this.last_four.includes(node)) {

			if (this.last_four.length > 3) {
				this.last_four.pop()
			}

			this.last_four.unshift(node);
		}

		var w = screen.width; var h = screen.height;
		var DPR = window.devicePixelRatio;
		w = Math.round(DPR * w);
		//h = Math.round(DPR * h);

		//console.log(node,h- (position.y).split('p')[0], (position.y).split('p')[0], h )
		this.container = document.getElementById('radarplot');
		document.body.clientHeight
		//this.container.style.left = position.x
		//this.container.style.top = position.y
		this.ifrm.contentWindow.postMessage(this.last_four + "", 'http://localhost:5000');

		this.container.className = "container-visible";


	}

	on_node_unselect(){
		this.container.className = "container-hidden";
	}
}

