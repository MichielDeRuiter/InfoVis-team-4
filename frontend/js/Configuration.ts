// configuration is a singleton, a single instance of this object will be available at any time
// the instance will be shared
export default class Configuration{
    private static instance: Configuration;

    private constructor() {
        this.fask_server_url = "http://127.0.0.1:5000/search";
    }

    // get the instance of the singleton if exist, create the instance if not
    public static get(): Configuration {
        if (!Configuration.instance) {
            Configuration.instance = new Configuration();
        }

        return Configuration.instance;
    }
}
