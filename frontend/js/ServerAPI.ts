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
    	d3.json(Configuration.get().fask_server_url, callback)
    }

}
