import { fb } from '../config/firebase'
import { Market } from './market-model'

export class MarketService {

    ///////////////
    // Variables //
    ///////////////
    private market: Market
    private markets: Market[]

	///////////////
	// Functions //
	///////////////
	public async fetchMarkets(userId: string): Promise<void> {
        
        this.markets = []

        await fb.firestore().collection(`/users/${userId}/markets`).get().then(markets => {
        
            markets.forEach(market => this.markets.push(new Market(market.data().marketId)))
        
        })
	}

	public async fetchMarket(userId: string, marketId: string): Promise<void> {
        
        await fb.firestore().doc(`/users/${userId}/markets/${marketId}`).get().then(market => {
        
            this.market = new Market( market.data().marketId )
        
        })
	}

	/////////////
	// Getters //
	/////////////
	public async getMarket(userId: string, marketId: string): Promise<Market> {
        
        await this.fetchMarket(userId, marketId)
        return new Promise<Market>(resolve => resolve(this.market))
		
	}

	public async getMarkets(userId: string): Promise<Market[]> {
        
        await this.fetchMarkets(userId)
        return new Promise<Market[]>(resolve => resolve(this.markets))

	}

	/////////////
	// Setters //
	/////////////
	public setMarket(market: Market): void {

        this.market = market

    }

	public setMarkets(markets: Market[]): void {

        this.markets = markets

    }

}