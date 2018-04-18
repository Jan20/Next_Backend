import * as functions from 'firebase-functions'
import * as express from 'express'
import { User } from './user/user-model'
import { UserService } from './user/user-service'
import { Market } from './market/market-model'
import { MarketService } from './market/market-service'
import { AssetService } from './asset/asset-service'

const express_app = express()

class Exe {

	///////////////
	// Variables //
	///////////////
	private userId: string = 'pej3fiZSJTf4tNHfNHCKHxa7eJf2'
	private user: User
	private markets: Market[]
	private userService: UserService = new UserService()
	private marketService: MarketService = new MarketService()
	private assetService: AssetService = new AssetService()

	///////////////
	// Functions //
	///////////////
	public async callAlphaVantage() {

		this.markets = []
	
		await this.userService.getUser(this.userId).then( user => this.user = new User(user.userId))
	
		await this.marketService.getMarkets(this.user.userId).then(markets => markets.forEach(
			
			market => this.markets.push( new Market(market.marketId))
		
		))
	
		this.markets.forEach( market => this.assetService.fetchAssetsFromAlphaVantage(this.user.userId, market.marketId))
	
	}

}

function getStocks()  {

	const exe = new Exe()

	exe.callAlphaVantage()
		.then( success => console.log('AlphaVantage API has been triggerd'))
		.catch(err => console.log(err))

}

express_app.get("*", (req, res) => {
	getStocks()
	res.send('function has been executed')
})

export const stocks = functions.https.onRequest((req, res) => {

	!req.path ? req.url = `/${req.url}` : null
	return express_app(req, res)

});
