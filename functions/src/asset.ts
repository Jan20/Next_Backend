class Asset {

	///////////////
	// Variables //
	///////////////
	private name: string
	private symbol: string
	private close: number
	private date: any

	//////////////////
	// Constructors //
	//////////////////
	public constructor(
		name: string, 
		symbol: string, 
		close: number, 
		date: any
	){
		this.name = name
		this.symbol = symbol
		this.close = close
		this.date = date
	}

	/////////////
	// Getters //
	/////////////
	public getName(): string {
		return this.name
	}

	public getSymbol(): string {
		return this.symbol
	}

	public getClose(): number {
		return this.close
	}

	public getDate(): any {
		return this.date
	}

	/////////////
	// Setters //
	/////////////
	public setName(name: string): void {
		this.name = name
	}

	public setSymbol(symbol: string): void {
		this.symbol = symbol
	}

	public setClose(close: number): void {
		this.close = close
	}

	public setDate(date: any): void {
		this.date = date
	}
}