export default abstract class BasicD3Visualization {
    name: string;
    container: HTMLDivElement;

    constructor(name: string) {
        this.name = name;
        this.container = d3.select("#" + name);
        this.resize();

    	let offsetHeight = this.container.node().offsetHeight;
    	let offsetWidth = this.container.node().offsetWidth;
        var margin = {top: 0, right: 0, bottom: 0, left: 0}
    	this.width = offsetWidth;
    	this.height = offsetHeight;

    	// we get the data from the Flask server
    	// the data is return as a JSON and can be used inmediately
    	// the server has to be running

    	// append the svg object to the body of the page
    	this.svg = d3.select("#" + name)
    		.append("svg")
      		.attr("width", this.width + margin.left + margin.right)
      		.attr("height", this.height + margin.top + margin.bottom)
    		.append("g")
      		.attr("transform",
            	"translate(" + margin.left + "," + margin.top + ")");
    }

    resize(): void{
    	
    	let offsetHeight = this.container.offsetHeight;
    	let offsetWidth = this.container.offsetWidth;
    }

    on_resize(): void{
    }
}