export class Asset {

    ///////////////
    // Variables //
    ///////////////
    public assetId: string
    public name: string
    public symbol: string

    //////////////////
    // Constructors //
    //////////////////
    public constructor(
        assetId: string,
        name: string,
        symbol: string
    ){
        this.assetId = assetId
        this.name = name
        this.symbol = symbol
    }
    

}