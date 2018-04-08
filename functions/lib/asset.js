class Asset {
    //////////////////
    // Constructors //
    //////////////////
    constructor(name, symbol, close, date) {
        this.name = name;
        this.symbol = symbol;
        this.close = close;
        this.date = date;
    }
    /////////////
    // Getters //
    /////////////
    getName() {
        return this.name;
    }
    getSymbol() {
        return this.symbol;
    }
    getClose() {
        return this.close;
    }
    getDate() {
        return this.date;
    }
    /////////////
    // Setters //
    /////////////
    setName(name) {
        this.name = name;
    }
    setSymbol(symbol) {
        this.symbol = symbol;
    }
    setClose(close) {
        this.close = close;
    }
    setDate(date) {
        this.date = date;
    }
}
//# sourceMappingURL=asset.js.map