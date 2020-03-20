import Configuration from './Configuration'

// ServerAPI is a singleton
export default class ServerAPI{
    private static instance: ServerAPI;

    private constructor() {
    	//
    }

    // get the instance of the singleton if exist, create the instance if not
    public static get(): ServerAPI {
        if (!ServerAPI.instance) {
            ServerAPI.instance = new ServerAPI();
        }

        return ServerAPI.instance;
    }

    public getData(callback): Object {
    	d3.json("http://127.0.0.1:5000/main", callback)
    }


    public getDataBetweenDates(d0, d1, callback): Object {
        d3.json("http://127.0.0.1:5000/main?fromDate=" + d0 + "&endDate=" + d1, callback)
    }


    
}
