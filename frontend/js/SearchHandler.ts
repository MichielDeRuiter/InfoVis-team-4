

import Configuration from './Configuration'
import ServerAPI from './ServerAPI'
import BasicD3Visualization from './BasicD3Visualization'

export default class SearchHandler
{
	constructor(eventHandler)
	{
		this.eventHandler = eventHandler;
		this.eventHandler.subscribe_search_handler(this)
		
		this.input_text = document.getElementById('button-input');
		this.button = document.getElementById('button-search');
		this.form = document.getElementById('form-search');
		this.form.addEventListener('submit', this.search.bind(this));

	}

	search(asd){
  		event.preventDefault();
		this.eventHandler.search_node(this.input_text.value)
	}

}

