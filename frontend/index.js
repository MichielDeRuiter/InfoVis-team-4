import Network3D from './js/network3D';
import Timeline from './js/Timeline';
import RadarplotIframe from './js/RadarplotIframe';
import EventHandler from './js/EventHandler';
import Timeslider from './js/Timeslider';
import ServerAPI from './js/ServerAPI';

import data from './js/network3D/reddit.json';








const eventHandler = new EventHandler();
const radarplot = new RadarplotIframe(eventHandler);
const timeline = new Timeline(eventHandler);
const network3D = new Network3D(eventHandler);
const timeslider = new Timeslider(eventHandler);

(ServerAPI.get()).getData(function(data2) {
	console.log(data, data2)
	network3D.update_network(data2)
});
