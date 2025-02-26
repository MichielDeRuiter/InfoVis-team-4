export default abstract class EventHandler {
    name: string;
    container: HTMLDivElement;


    constructor(network: Object, radarplot: Object, timeline: Object, timeslider: Object, search_handler : Object) {
        this.name = name;

        this.network = network;
        this.radarplot = radarplot;
        this.timeline = timeline;
        this.timeslider = timeslider;
        this.search_handler = search_handler;

        window.addEventListener("resize", this.on_resize.bind(this));
    }

    subscribe_network(network) : void {
        this.network = network;
    }

    subscribe_radarplot(radarplot) : void {
        this.radarplot = radarplot;
    }

    subscribe_timeline(timeline) : void {
        this.timeline = timeline;
    }

    subscribe_timeslider(timeslider) : void {
        this.timeslider = timeslider;
    }

    subscribe_search_handler(search_handler) : void {
        this.search_handler = search_handler;
    }

    update_radarplot(): void{
    	this.radarplot.update()
    }

    update_network(): void{
        this.radarplot.update()
    }

    update_timeline(): void{
        this.radarplot.update()
    }

    on_timeline_update(): void{

    }

    on_radarplot_update(): void{

    }

    change_dates(date0, date1): void{
        this.network.update_dates(date0, date1)
    }

    search_node(node):void{
        this.network.search_node(node);
    }

    on_network_over(node_name, position): void{
        this.radarplot.on_node_select(node_name, position);
    }

    on_network_over_ends(asd): void{
        this.radarplot.on_node_unselect()
    }


    on_resize(event):void {
    console.log('asd')
        this.network.on_resize(event)
        this.radarplot.on_resize(event)
        this.timeline.on_resize(event)
    }
}