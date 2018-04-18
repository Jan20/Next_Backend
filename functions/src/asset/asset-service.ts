import { fb } from '../config/firebase'
import { Asset } from './asset-model'
import * as request from 'request'

export class AssetService {

    ///////////////
    // Variables //
    ///////////////
    private asset: Asset
    private assets: Asset[]

    //////////////////
    // Constructors //
    //////////////////
    // public constructor() {}

	///////////////
	// Functions //
	///////////////
    public async fetchAssetsFromAlphaVantage(userId: string, marketId: string) {
  
        await this.fetchAssets(userId, marketId)
        console.log(userId)
        console.log(marketId)
        console.log(this.assets)
        this.assets.forEach(asset => this.fetchAssetFromAlphaVantage(userId, marketId, asset))
  
    }

    /*
    *
    *	Simple function to access the Alpha Vantage API, make a call and write all relevant datapoints back
    *	into a Firestore realtime database
    *
    */
    public async fetchAssetFromAlphaVantage(userId: string, marketId: string, asset: Asset): Promise<void> {
       
        await request(`https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${asset.symbol}&outputsize=compact&apikey=6404`, function (error, response, body) {
        
            if (error && response.statusCode !== 200) {
                console.log('Asset data could not have been retrieved.')
                return;
            }

            const data = JSON.parse(body)
            
            for (const key in data['Time Series (Daily)']) {
            
                if (data['Time Series (Daily)'].hasOwnProperty(key)) {
                    
                    console.log('____________________________________________________')
                    console.log(asset.name)
                    console.log(data['Meta Data']['2. Symbol'])
                    console.log(data['Time Series (Daily)'][key]['4. close'])
                    console.log(key)
                    console.log('____________________________________________________')

                    fb.firestore().collection(`/users/${userId}/markets/${marketId}/assets/${asset.assetId}/series`).doc(key).set({
                        'name': asset.name,
                        'symbol': data['Meta Data']['2. Symbol'],
                        'close': data['Time Series (Daily)'][key]['4. close'],
                        'date': key,
                    })

                }
            }
        })
    }

	public async fetchAsset(userId: string, marketId: string, assetId: string): Promise<void> {
        
        await fb.firestore().doc(`/users/${userId}/markets/${marketId}/assets/${assetId}`).get().then(asset => {
            
            this.asset = new Asset( asset.data().assetId, asset.data().name, asset.data().symbol)
        
        })
    }
    
    public async fetchAssets(userId: string, marketId: string): Promise<void> {

        this.assets = []
        
        await fb.firestore().collection(`/users/${userId}/markets/${marketId}/assets`).get().then(assets => {
            
            assets.forEach(asset => {
            
                this.assets.push( new Asset( asset.data().assetId, asset.data().name, asset.data().symbol) )
            
            })
		})
	}


	/////////////
	// Getters //
	/////////////
	public async getAsset(userId: string, marketId: string, assetId: string): Promise<Asset> {
        
        await this.fetchAsset(userId, marketId, assetId)
        return new Promise<Asset>(resolve => resolve(this.asset))
        
	}

	public async getAssets(userId: string, marketId: string): Promise<Asset[]> {
        
        await this.fetchAssets(userId, marketId)
        return new Promise<Asset[]>(resolve => resolve(this.assets))

	}

	/////////////
	// Setters //
	/////////////
	public setAsset(asset: Asset): void {
    
        this.asset = asset
    
    }

	public setAssets(assets: Asset[]): void {
    
        this.assets = assets
    
    }
}